"""
LoadSpaceHook assembles the overload 'Dispatcher' objects for a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, Dispatcher
from ...waitaminute.meta import OverloadConflict, ReboundOverload
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional


class LoadSpaceHook(AbstractSpaceHook):
  """
  LoadSpaceHook collects the 'overload' instances declared in the class
  body. During 'setItemPhase' it records each overload's signatures,
  variadics, fallback, and finalizer on the namespace; during
  'postCompilePhase' it assembles one 'Dispatcher' per overloaded name
  from the registrations the namespace merges across the method
  resolution order, and writes it into the compiled namespace.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    The 'setItemPhase' method records each binding of the class body. An
    'overload' is claimed and its registrations are stored on the
    namespace, each signature as a copy, so that the 'overload' object
    keeps 'THIS' and may be bound in another class body; anything else
    is a plain definition, whose name is noted and which the namespace
    stores as usual. One class body may not give
    a name both, in either order, so the second of the two raises
    'OverloadConflict'. The hook runs ahead of the hooks of the namespace
    subclasses, so it also notes a plain value one of them then claims,
    such as an 'EZField'. One class body binds an 'overload' object once:
    a second binding of it, under another name as in '__radd__ =
    __add__' or under the same one, raises 'ReboundOverload', and the
    second name takes a method of its own. Another class body may bind
    the same object again.
    """
    if not isinstance(val, overload):
      if self.space.hasOverloads(key):
        raise OverloadConflict(self.space.getClassName(), key, True)
      self.space.addPlainName(key)
      return False
    if key in self.space.getPlainNames():
      raise OverloadConflict(self.space.getClassName(), key, False)
    claimedName = self.space.getClaimedName(val)
    if claimedName is not None:
      raise ReboundOverload(self.space.getClassName(), claimedName, key)
    self.space.addClaimedName(val, key)
    #  A stack of decorators may give one 'overload' every role at once.
    if val.isFallback():
      self.space.addFallback(key, val.getFallback())
    if val.isFinalizer():
      self.space.addFinalizer(key, val.getFinalizer())
    #  Copies, since naming the class rewrites 'THIS' in a registered
    #  signature in place: an 'overload' bound in two class bodies would
    #  otherwise hand the second class the signatures the first fixed.
    for sig, func in val:
      self.space.addOverload(key, sig(), func)
    for sig, func in val.getVariadics():
      self.space.addVariadic(key, sig(), func)
    return True

  def delItemPhase(self, key: str, val: Any = None, ) -> bool:
    """
    The 'delItemPhase' method forgets a plain name the class body
    deletes, so the name may be overloaded afterwards; the record exists
    so that one body does not give a name both a plain definition and
    overloads, and a deleted definition is no longer one. A deleted
    overloaded name is left to the namespace, which records the deletion
    and refuses it as the class is created.
    """
    self.space.removePlainName(key)
    return False

  def postCompilePhase(self, compiledSpace) -> dict:
    """Assembles one 'Dispatcher' per overloaded name and writes each
    into 'compiledSpace'. The registrations come from 'collectOverloads',
    'collectVariadics', 'collectFallback', and 'collectFinalizer' on the
    namespace, which put the class body's own registrations first and
    merge in those of the classes in the method resolution order, nearest
    first. Each registration reaches the 'Dispatcher' together with its
    distance, which decides the order of the cast passes.

    Two different variadic declarations that both accept one call by
    exact type, such as 'ARGS[int]' and '(int, ARGS[int])', are no
    conflict: the most recent declaration of the nearest class takes the
    call, as 'Dispatcher' documents. Two equal ones in one class body
    with different functions are refused at the second of them by
    'addVariadic', as two equal concrete signatures are by
    'addOverload'.

    A name that the class body bound to a plain (non-'overload')
    definition gets no 'Dispatcher': that explicit definition overrides
    any overloads inherited from a base class, and it also stops
    subclasses from collecting registrations beyond it. The class body
    itself cannot have overloaded the name as well, which 'setItemPhase'
    refuses. The signal is the namespace's own storage: '@overload'
    declarations are claimed by 'setItemPhase' and never reach it,
    whereas a plain definition is stored there under its name. A name for
    which a plain definition in a base class shadows every registration
    gets no 'Dispatcher' either, leaving that plain definition to be
    found through the method resolution order.
    """
    for name in self.space.getOverloadNames():
      if dict.__contains__(self.space, name):
        continue
      dispatcher = self._buildDispatcher(name)
      if dispatcher is not None:
        compiledSpace[name] = dispatcher
    return compiledSpace

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _buildDispatcher(self, name: str) -> Optional[Dispatcher]:
    """
    The '_buildDispatcher' method builds the 'Dispatcher' for 'name' from
    the registrations the namespace collects, or returns None when a
    plain definition in a base class shadows all of them.
    """
    sigFuncs = self.space.collectOverloads(name)
    variadics = self.space.collectVariadics(name)
    fallback = self.space.collectFallback(name)
    finalizer = self.space.collectFinalizer(name)
    if not (sigFuncs or variadics or fallback or finalizer):
      return None
    dispatcher = Dispatcher()
    for sig, func, distance in sigFuncs:
      dispatcher.addSigFunc(sig, func, distance)
    for sig, func, distance in variadics:
      dispatcher.addVariadicSigFunc(sig, func, distance)
    if fallback is not None:
      dispatcher.setFallbackFunction(fallback)
    if finalizer is not None:
      dispatcher.setFinalizerFunction(finalizer)
    return dispatcher
