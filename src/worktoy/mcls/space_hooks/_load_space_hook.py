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

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class LoadSpaceHook(AbstractSpaceHook):
  """
  Python keeps only the last function bound to a name in a class body,
  yet a 'BaseObject' class declares one function per signature at one
  name with '@overload'. Every declaration must therefore be taken from
  the body as it is bound, and once the body ends, the declarations of
  each name, with those the class inherits, must become one dispatcher
  at that name. A name may not be both overloaded and defined plainly in
  one body, since one of the two would be lost.

  Implementation
  --------------

  'setItemPhase' claims every 'overload' object, so the namespace never
  stores one, and records its signatures, as copies, its fallback and its
  finalizer on the namespace. A record under '@classmethod' or
  '@staticmethod' is taken out and claimed the same way, and the kind of
  method each binding declares is recorded; a second kind at one name, or
  both kinds in one stack, raises 'MixedMethodKind'. A plain binding at
  an overloaded name, or an overload at a plainly bound one, raises
  'OverloadConflict'; binding one 'overload' object twice in a body, as
  '__radd__ = __add__', raises 'ReboundOverload'. 'postCompilePhase'
  builds a 'Dispatcher' for every
  overloaded name of the body or of a base, unless the body defines the
  name plainly, and writes it into the dictionary, of the kind of method
  the nearest class declaring the name made it. Every class thus has
  dispatchers of its own.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    Each 'overload' object must be recorded as it is bound, and a mixed or
    repeated binding refused at its line.

    Implementation
    --------------

    The signatures are copied with 'sig()', since placing a class rewrites
    'THIS' in a registered signature in place and the 'overload' object
    may be bound in another class body. A plain value one of the later
    hooks claims, such as an 'EZField', is still noted as plain, since this
    hook runs before any hook a namespace subclass adds.

    Parameters
    ----------

    key : str
      The name bound.

    val : Any
      The value bound.

    old : Any, optional
      The value the name held, or 'None'.

    Returns
    -------

    bool
      'True' for an 'overload', claiming it.

    Raises
    ------

    OverloadConflict
      The name is bound both plainly and to overloads.

    ReboundOverload
      The 'overload' object is bound a second time in the body.

    MixedMethodKind
      The body declared the name as another kind of method already, or the
      binding is decorated as both a classmethod and a staticmethod.
    """
    kinds, record = overload.peelMethodKinds(val)
    if not isinstance(record, overload):
      if self.space.hasOverloads(key):
        raise OverloadConflict(self.space.getClassName(), key, True)
      self.space.addPlainName(key)
      return False
    val = record
    if key in self.space.getPlainNames():
      raise OverloadConflict(self.space.getClassName(), key, False)
    claimedName = self.space.getClaimedName(val)
    if claimedName is not None:
      raise ReboundOverload(self.space.getClassName(), claimedName, key)
    self.space.addMethodKind(key, self._getMethodKind(key, kinds, val))
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
    for sig, func in val.getFlexes():
      self.space.addFlex(key, sig(), func)
    for sig, func in val.getVariadics():
      self.space.addVariadic(key, sig(), func)
    return True

  def _getMethodKind(self, key: str, kinds: tuple, record: overload) -> Any:
    """
    The kind of method a binding declares comes from the layers written
    above the record and from those its decorators were given, and both
    must name one kind.

    Parameters
    ----------

    key : str
      The name bound.

    kinds : tuple
      The kinds of the layers above the record, outermost first.

    record : overload
      The record under them.

    Returns
    -------

    Any
      'classmethod', 'staticmethod', or 'None' for an instance method.
    """
    recordKind = record.getMethodKind()
    if recordKind is None:
      stack = kinds
    else:
      stack = (*kinds, recordKind)
    className = self.space.getClassName()
    return overload.agreeMethodKind(stack, key, className)

  def delItemPhase(self, key: str, val: Any = None, ) -> bool:
    """
    A plain definition deleted from the body no longer conflicts with
    overloads at its name.

    Implementation
    --------------

    The name is forgotten as plain. A deleted overloaded name is left to
    the namespace, which refuses it as the class is created.
    """
    self.space.removePlainName(key)
    return False

  def postCompilePhase(self, compiledSpace) -> dict:
    """
    Once the body has ended, each overloaded name must hold its
    dispatcher, built from the declarations of the body and of the bases.

    Implementation
    --------------

    A name the body defines plainly gets none, since that definition
    overrides the inherited overloads, and so does a name whose every
    registration a plain definition in a base hides.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary being assembled.

    Returns
    -------

    dict
      The dictionary with the dispatchers.
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
    sigFuncs = self.space.collectOverloads(name)
    flexes = self.space.collectFlexes(name)
    variadics = self.space.collectVariadics(name)
    fallback = self.space.collectFallback(name)
    finalizer = self.space.collectFinalizer(name)
    if not (sigFuncs or flexes or variadics or fallback or finalizer):
      return None
    dispatcher = Dispatcher()
    dispatcher.setMethodKind(self.space.collectMethodKind(name))
    for sig, func, distance in sigFuncs:
      dispatcher.addSigFunc(sig, func, distance)
    for sig, func, distance in flexes:
      dispatcher.addFlexSigFunc(sig, func, distance)
    for sig, func, distance in variadics:
      dispatcher.addVariadicSigFunc(sig, func, distance)
    if fallback is not None:
      dispatcher.setFallbackFunction(fallback)
    if finalizer is not None:
      dispatcher.setFinalizerFunction(finalizer)
    return dispatcher
