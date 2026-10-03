"""
LoadSpaceHook assembles the overload 'Dispatcher' objects for a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...dispatch import overload, Dispatcher
from ...waitaminute.dispatch import VariadicOverlap
from ...waitaminute.meta import OverloadConflict
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
    namespace; anything else is a plain definition, whose name is noted
    and which the namespace stores as usual. One class body may not give
    a name both, in either order, so the second of the two raises
    'OverloadConflict'. The hook runs ahead of the hooks of the namespace
    subclasses, so it also notes a plain value one of them then claims,
    such as an 'EZField'. The namespace records the name each 'overload'
    object is first bound to, and a later binding of the same object
    under another name in the same class body is an alias of that name.
    """
    if not isinstance(val, overload):
      if self.space.hasOverloads(key):
        raise OverloadConflict(self.space.getClassName(), key, True)
      self.space.addPlainName(key)
      return False
    if key in self.space.getPlainNames():
      raise OverloadConflict(self.space.getClassName(), key, False)
    claimedName = self.space.getClaimedName(val)
    if claimedName is None:
      self.space.addClaimedName(val, key)
    elif claimedName != key:
      #  The wrapper was already claimed under another name, so this
      #  assignment aliases that overloaded name. The wrapper alone
      #  carries only its own declaration, the last one in the body,
      #  so the alias instead copies every registration the source
      #  name holds so far, inherited ones included.
      for sig, func, _ in self.space.collectOverloads(claimedName):
        self.space.addOverload(key, sig, func)
      for sig, func, _ in self.space.collectVariadics(claimedName):
        self.space.addVariadic(key, sig, func)
      fallback = self.space.collectFallback(claimedName)
      if fallback is not None:
        self.space.addFallback(key, fallback)
      finalizer = self.space.collectFinalizer(claimedName)
      if finalizer is not None:
        self.space.addFinalizer(key, finalizer)
      return True
    #  A stack of decorators may give one 'overload' every role at once.
    if val.isFallback():
      self.space.addFallback(key, val.getFallback())
    if val.isFinalizer():
      self.space.addFinalizer(key, val.getFinalizer())
    for sig, func in val:
      self.space.addOverload(key, sig, func)
    for sig, func in val.getVariadics():
      self.space.addVariadic(key, sig, func)
    return True

  def postCompilePhase(self, compiledSpace) -> dict:
    """Assembles one 'Dispatcher' per overloaded name and writes each
    into 'compiledSpace'. The registrations come from 'collectOverloads',
    'collectVariadics', 'collectFallback', and 'collectFinalizer' on the
    namespace, which put the class body's own registrations first and
    merge in those of the classes in the method resolution order, nearest
    first. Each registration reaches the 'Dispatcher' together with its
    distance, which decides the order of the cast passes.

    Two variadic declarations of different functions that both accept
    one call by exact type, with no explicit declaration settling it,
    raise 'VariadicOverlap' here, naming the two declarations; see
    'BaseSpace.getVariadicOverlaps'.

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
    for name in self.space.getVariadics():
      for overlap in self.space.getVariadicOverlaps(name):
        raise VariadicOverlap(name, *overlap)
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
