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
  method each binding declares is recorded, for the name and for each
  function; one stack declaring both a classmethod and a staticmethod
  raises 'MixedMethodKind'. A plain binding at
  an overloaded name, or an overload at a plainly bound one, raises
  'OverloadConflict'; binding one 'overload' object twice in a body, as
  '__radd__ = __add__', raises 'ReboundOverload'. 'postCompilePhase'
  builds a 'Dispatcher' for every
  overloaded name of the body or of a base, unless the body defines the
  name plainly, and writes it into the dictionary. Every class thus has
  dispatchers of its own. A name holding bound methods beside
  classmethods or staticmethods takes two: one of the bound methods and
  the classmethods, reached through an instance, which keeps one of the
  classmethods and the staticmethods, reached through the class. A bound
  method is thus not considered through the class, nor a staticmethod
  through an instance. Any other name takes one dispatcher holding every
  function.
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
      The binding is decorated as both a classmethod and a staticmethod.
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
    kind = self._getMethodKind(key, kinds, val)
    self.space.addMethodKind(key, kind)
    #  Before the registrations below, which ask for the kind of a function
    #  to tell whether two of one signature can meet.
    self.space.addFunctionKind(key, kind, *self._getFunctions(val))
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

  @staticmethod
  def _getFunctions(record: overload) -> list:
    """
    A record hands its function to the namespace under every role it
    declares, and the namespace keeps the kind of each.

    Parameters
    ----------

    record : overload
      The record.

    Returns
    -------

    list
      Every function the record hands over: those of its concrete,
      flexible and variadic signatures, a 'PermuterMethod' of a flexible
      declaration included, its fallback and its finalizer.
    """
    out = [func for _, func in record]
    out += [func for _, func in record.getFlexes()]
    out += [func for _, func in record.getVariadics()]
    if record.isFallback():
      out.append(record.getFallback())
    if record.isFinalizer():
      out.append(record.getFinalizer())
    return out

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
    """
    One name may hold bound methods, classmethods and staticmethods. A
    bound method needs an instance, so it is not considered through the
    class, and where a name has bound methods its staticmethods are not
    considered through an instance. A classmethod is reached both ways.

    Implementation
    --------------

    A name holding bound methods beside another kind takes two
    dispatchers, each built by '_buildSide': one of the bound methods and
    the classmethods, which is returned and reached through an instance,
    and one of the classmethods and the staticmethods, which the first
    keeps for a read through the class. Any other name takes one
    dispatcher of every function.

    Parameters
    ----------

    name : str
      The overloaded name.

    Returns
    -------

    Dispatcher or None
      The dispatcher for the class dictionary, or 'None' when nothing is
      declared at the name that the class inherits.
    """
    gathered = (
      self.space.collectOverloads(name),
      self.space.collectFlexes(name),
      self.space.collectVariadics(name),
      self.space.collectFallback(name),
      self.space.collectFinalizer(name),
    )
    members = self._getMembers(*gathered)
    if not members:
      return None
    kinds = self.space.collectFunctionKinds(name)
    memberKinds = [self.space._kindIn(kinds, func) for func in members]
    bound = any(kind is None for kind in memberKinds)
    other = any(kind is not None for kind in memberKinds)
    if bound and other:
      #  This branch is reached by the following:
      #  - The name holds bound methods beside classmethods or
      #    staticmethods
      onInstance = self._buildSide(gathered, kinds, (None, classmethod))
      onClass = self._buildSide(gathered, kinds, (classmethod, staticmethod))
      onInstance.setClassDispatcher(onClass)
      return onInstance
    every = (None, classmethod, staticmethod)
    return self._buildSide(gathered, kinds, every)

  @staticmethod
  def _getMembers(*gathered) -> list:
    sigFuncs, flexes, variadics, fallback, finalizer = gathered
    out = [func for _, func, __ in (*sigFuncs, *flexes, *variadics)]
    for role in (fallback, finalizer):
      if role is not None:
        out.append(role)
    return out

  def _buildSide(
      self,
      gathered: tuple,
      kinds: list,
      accepted: tuple,
  ) -> Dispatcher:
    """
    A dispatcher holds the functions of a name that one way of reaching
    it considers, and binds one receiver for them all: the instance when
    a bound method is among them, else the class.

    Implementation
    --------------

    The dispatcher stands for an instance method when it holds a bound
    method, else for a classmethod when it holds one, else for a
    staticmethod. The functions of another kind than that are named to it
    by 'setFunctionKind' before any is registered, and the functions of
    the accepted kinds are registered with their distances, the fallback
    and the finalizer included.

    Parameters
    ----------

    gathered : tuple
      What the namespace gathered at the name: the concrete, the flexible
      and the variadic registrations, each a list of signature, function
      and distance, then the fallback and the finalizer, each a function
      or 'None'.

    kinds : list
      A 'list[tuple[Callable, Any]]' of each function at the name with
      its kind.

    accepted : tuple
      The kinds the dispatcher holds, each 'classmethod', 'staticmethod',
      or 'None' for an instance method.

    Returns
    -------

    Dispatcher
      The dispatcher, unplaced.
    """

    def kindOf(func: Any) -> Any:
      return self.space._kindIn(kinds, func)

    def taken(func: Any) -> bool:
      own = kindOf(func)
      return True if any(own is kind for kind in accepted) else False

    sigFuncs = [entry for entry in gathered[0] if taken(entry[1])]
    flexes = [entry for entry in gathered[1] if taken(entry[1])]
    variadics = [entry for entry in gathered[2] if taken(entry[1])]
    #  A fallback or a finalizer the name does not have is 'None' here,
    #  and stays 'None' whichever way the test falls.
    fallback = gathered[3] if taken(gathered[3]) else None
    finalizer = gathered[4] if taken(gathered[4]) else None
    members = self._getMembers(
        sigFuncs, flexes, variadics, fallback, finalizer,
    )
    memberKinds = [kindOf(func) for func in members]
    if any(kind is None for kind in memberKinds):
      binding = None
    elif any(kind is classmethod for kind in memberKinds):
      binding = classmethod
    else:
      binding = staticmethod
    dispatcher = Dispatcher()
    dispatcher.setMethodKind(binding)
    for kind in (classmethod, staticmethod):
      if kind is binding:
        continue
      named = [func for func in members if kindOf(func) is kind]
      dispatcher.setFunctionKind(kind, *named)
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
