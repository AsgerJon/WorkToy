"""
ABCSpace is the namespace class of 'ABCMeta'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..core.sentinels import ARGS
from ..dispatch import overload, abstract, CallMeMaybe
from ..waitaminute.meta import WrongImplementation
from . import AbstractNamespace, BaseSpace
from .space_hooks import ABCHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Optional, TypeAlias

  from ..dispatch import TypeSig

  Requirement: TypeAlias = tuple[str, str, Optional[TypeSig], abstract, Any]
  Requirements: TypeAlias = list[Requirement]


class ABCSpace(BaseSpace):
  """
  A class built by 'ABCMeta' declares methods with '@abstract', and the
  classes based on it have to write them. Such a class and its
  subclasses answer to each other: the class says what is to be written,
  and each subclass is asked, as it is created, what it wrote and
  whether it wrote it rightly. A subclass may write any of the abstract
  methods or none, and may declare abstract methods of its own, so what
  a class still lacks has to be worked out for every class anew, from
  what the classes along its resolution order declared and wrote. An
  overloaded name is abstract one signature at a time, and is written
  by a plain function at the name or by each of its signatures.

  Implementation
  --------------

  What a class body declares abstract is a requirement: the name, how it
  is declared ('plain', or as an 'overload', 'flex' or 'variadic'
  signature), the signature, the 'abstract' record and the kind of
  method. 'getDeclaredAbstract' gives those of the body, and
  'getInheritedAbstract' those of the classes along the resolution
  order that no nearer class along it answers, by binding the name or
  registering the signature. 'ABCHook' holds a function bound at an
  abstract name to its requirements through 'screenPlain', and the
  registration methods 'LoadSpaceHook' calls are reimplemented here to
  hold each overload to the requirement of its signature, both at the
  line that writes it. 'settleAbstract' gives what is left once the
  body has ended: the inherited requirements the body did not answer,
  and its own.

  Attributes
  ----------

  __inherited_abstract__ : list or None
    The requirements the class inherits, kept at the first asking.

  __declared_abstract__ : list or None
    The requirements the body declared, kept once the body has ended.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __inherited_abstract__: Optional[Requirements] = None
  __declared_abstract__: Optional[Requirements] = None

  #  Public Variables
  abcHook = ABCHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _getBodySpace(cls: type) -> Optional[AbstractNamespace]:
    if '__namespace__' not in cls.__dict__:
      #  This branch is reached by the following:
      #  - The class was built by no worktoy metaclass, as a plain mixin
      #    or 'object'
      return None
    space = cls.__dict__['__namespace__']
    if isinstance(space, AbstractNamespace):
      return space
    #  The rest of the method is reached by the following:
    #  - The class was built by 'MetaType' alone, as 'Object' is, whose
    #    namespace is a plain dictionary
    return None

  @staticmethod
  def _getRegistry(space: BaseSpace, role: str) -> dict:
    if role == 'overload':
      return space.getOverloads()
    if role == 'flex':
      return space.getFlexes()
    return space.getVariadics()

  @classmethod
  def _registeredIn(cls, space: BaseSpace, role: str, name: str) -> list:
    try:
      return cls._getRegistry(space, role)[name]
    except KeyError:
      #  This branch is reached by the following:
      #  - The body registered nothing of that sort at the name
      return []

  @staticmethod
  def _sameSignature(role: str, first: TypeSig, second: TypeSig) -> bool:
    if role == 'flex':
      #  This branch is reached by the following:
      #  - A flexible declaration of more than three classes, which is
      #    the same declaration in any order of its classes
      return True if first.getBag() == second.getBag() else False
    return True if first == second else False

  @staticmethod
  def _signatureShape(
      role: str,
      sig: TypeSig,
      func: Any,
      kind: Any,
  ) -> tuple:
    """
    A function registered under a signature is called with as many
    arguments by position as the signature has entries, and with any
    number more where the signature ends in an 'ARGS'. What it takes by
    keyword is not in the signature, and is read off the function, which
    is a Python function: the blank function of a declaration, or one a
    body wrote.

    Returns
    -------

    tuple
      A shape as 'abstract.shapeOf' gives one: the count and whether any
      number more from the signature, the keywords from the function.
    """
    inner = func
    if isinstance(func, (abstract, CallMeMaybe)):
      inner = func.__wrapped__
    _, __, keyed, doubled = abstract.shapeOf(inner, kind)
    if role == 'variadic':
      return len(sig) - 1, True, keyed, doubled
    return len(sig), False, keyed, doubled

  @classmethod
  def _declaredShape(cls, requirement: Requirement) -> tuple:
    """
    What an implementation has to be able to receive: for a method
    declared plainly what its blank function takes, and for a signature
    of an overloaded name what the signature takes.
    """
    name, role, sig, func, kind = requirement
    if role == 'plain':
      return func.getShape(kind)
    return cls._signatureShape(role, sig, func, kind)

  @staticmethod
  def _label(requirement: Requirement) -> str:
    """
    A requirement is named to the reader as it was declared: the name of
    a method declared plainly, the name with the signature for an
    abstract overload, as 'data(str, int)', and a classmethod or a
    staticmethod named as such, since an implementation has to be of
    the same kind.
    """
    name, role, sig, func, kind = requirement
    if kind is classmethod:
      head = 'classmethod '
    elif kind is staticmethod:
      head = 'staticmethod '
    else:
      head = ''
    if role == 'plain':
      return '%s%s' % (head, name)
    names = []
    for entry in sig:
      if isinstance(entry, ARGS):
        names.append(str(entry))
      else:
        names.append(entry.__name__)
    text = '%s%s(%s)' % (head, name, ', '.join(names))
    if role == 'flex':
      return '%s in any order' % text
    return text

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getDeclaredAbstract(self, ) -> Requirements:
    """
    Each class says what its own body declares abstract, and every class
    based on it asks as it is created.

    Implementation
    --------------

    A record of '@abstract' the body left at a name, under any
    'classmethod' or 'staticmethod' layer, is a method declared plainly.
    A record registered under a signature of an overloaded name is an
    abstract overload. The answer is kept once the body has ended.

    Returns
    -------

    Requirements
      A 'list[tuple[str, str, Optional[TypeSig], abstract, Any]]': for
      each declaration the name, 'plain', 'overload', 'flex' or
      'variadic', the signature or 'None', the record, and the kind of
      method. The methods declared plainly come first, then the
      concrete, the flexible and the variadic signatures.
    """
    if self.__declared_abstract__ is not None:
      #  This branch is reached by the following:
      #  - The namespace is compiled, so its body has ended
      return self.__declared_abstract__
    className = self.getClassName()
    out = []
    for name, value in dict.items(self):
      kinds, inner = overload.peelMethodKinds(value)
      if isinstance(inner, abstract):
        kind = overload.agreeMethodKind(kinds, name, className)
        out.append((name, 'plain', None, inner, kind))
    for role in ('overload', 'flex', 'variadic'):
      for name, sigFuncs in self._getRegistry(self, role).items():
        kinds = self._gatherFunctionKinds((self,), name)
        for sig, func in sigFuncs:
          if isinstance(func, abstract):
            out.append((name, role, sig, func, self._kindIn(kinds, func)))
    return out

  def _spaceBinds(
      self,
      space: AbstractNamespace,
      requirement: Requirement,
  ) -> bool:
    """
    A class answers a requirement when its body binds what the
    requirement is about: for a method declared plainly, anything at the
    name; for a signature of an overloaded name, a plain binding at the
    name, or a registration of that signature as the same kind of
    method. Whether the answer writes the method or declares it anew is
    the same here: either way the requirement is no longer the one in
    force.
    """
    name, role, sig, func, kind = requirement
    if role == 'plain':
      return True if name in space.getShadowSpace() else False
    if dict.__contains__(space, name):
      return True
    if not isinstance(space, BaseSpace):
      return False
    kinds = space._gatherFunctionKinds((space,), name)
    for other, held in self._registeredIn(space, role, name):
      if not self._sameSignature(role, sig, other):
        continue
      if space._kindIn(kinds, held) is kind:
        return True
    return False

  def _classBinds(self, cls: type, requirement: Requirement) -> bool:
    space = self._getBodySpace(cls)
    if space is None:
      return True if requirement[0] in cls.__dict__ else False
    return self._spaceBinds(space, requirement)

  def getInheritedAbstract(self, ) -> Requirements:
    """
    A class inherits the requirements of the classes it is based on,
    except those a class nearer along its resolution order has answered.
    In a diamond, a method one branch wrote is written for the class
    listing that branch before the declaration is reached, as Python
    finds that method first.

    Implementation
    --------------

    Each class along the order built in an 'ABCSpace' gives what its body
    declared. A requirement is inherited unless a class before its
    declaring class answers it; see '_spaceBinds'. The answer rests on
    the bases alone, and is kept at the first asking.

    Returns
    -------

    Requirements
      The inherited requirements, those of the farthest class first.
    """
    if self.__inherited_abstract__ is None:
      order = self._getLookupOrder()
      out = []
      for index in reversed(range(len(order))):
        space = self._getBodySpace(order[index])
        if not isinstance(space, ABCSpace):
          continue
        nearer = order[:index]
        for requirement in space.getDeclaredAbstract():
          if not any(self._classBinds(cls, requirement) for cls in nearer):
            out.append(requirement)
      self.__inherited_abstract__ = out
    return self.__inherited_abstract__

  def _getInheritedAt(self, name: str) -> Requirements:
    return [r for r in self.getInheritedAbstract() if r[0] == name]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _hold(self, requirement: Requirement, kind: Any, func: Any) -> None:
    """
    A method left unwritten leaves its class abstract, but a method
    written wrongly must fail where it is written. An implementation is
    right when it is the same kind of method as the abstract one and can
    receive everything that one declares.

    Parameters
    ----------

    requirement : Requirement
      What is declared.

    kind : Any
      The kind of method the body wrote: 'classmethod', 'staticmethod',
      or 'None' for a bound method.

    func : Any
      What the body wrote.

    Raises
    ------

    WrongImplementation
      'func' is no function, is another kind of method, or cannot take
      what is declared.
    """
    className = self.getClassName()
    label = self._label(requirement)
    declared = self._declaredShape(requirement)
    declaredText = abstract.describe(requirement[4], declared)
    if not isinstance(func, FunctionType):
      writtenText = 'no function'
      raise WrongImplementation(className, label, declaredText, writtenText)
    written = abstract.shapeOf(func, kind)
    if kind is requirement[4] and abstract.fits(declared, written):
      return
    writtenText = abstract.describe(kind, written)
    raise WrongImplementation(className, label, declaredText, writtenText)

  def screenPlain(self, name: str, kinds: tuple, value: Any) -> None:
    """
    A plain binding at a name a base declares abstract implements the
    method, and for an overloaded name every one of its signatures at
    once, since a plain definition takes the place of all the inherited
    overloads. It is held to each requirement at the name.

    Parameters
    ----------

    name : str
      The name bound.

    kinds : tuple
      The 'classmethod' and 'staticmethod' layers around the value,
      outermost first.

    value : Any
      What lies under them.

    Raises
    ------

    WrongImplementation
      The value does not implement a requirement at the name.
    """
    requirements = self._getInheritedAt(name)
    if not requirements:
      return
    kind = overload.agreeMethodKind(kinds, name, self.getClassName())
    for requirement in requirements:
      self._hold(requirement, kind, value)

  def _screenRegistration(
      self,
      name: str,
      role: str,
      sig: TypeSig,
      func: Callable,
  ) -> None:
    """
    Each function a body registers under a signature is either an
    abstract declaration or something written. The blank function of a
    declaration must itself be able to take the signature stacked on
    it. A written function at a signature a base declares abstract
    implements that signature and is held to it. A bound method and a
    staticmethod may share a signature, so the requirement of the same
    kind is the one implemented where there is one.

    Raises
    ------

    WrongImplementation
      The blank function cannot take its signature, or the function
      written does not implement the requirement of its signature.
    """
    kind = self._kindIn(self._gatherFunctionKinds((self,), name), func)
    if isinstance(func, abstract):
      #  'LoadSpaceHook' claims the record of '@overload' before 'ABCHook'
      #  sees it, so the flag of an abstract overload is set here.
      func.__abc_only__ = True
      self._hold((name, role, sig, func, kind), kind, func.__wrapped__)
      return
    inner = func
    if isinstance(func, CallMeMaybe):
      #  This branch is reached by the following:
      #  - One order of a flexible declaration, which holds its function
      inner = func.__wrapped__
    matching = []
    for requirement in self._getInheritedAt(name):
      if requirement[1] != role:
        continue
      if self._sameSignature(role, requirement[2], sig):
        matching.append(requirement)
    sameKind = [r for r in matching if r[4] is kind]
    if sameKind:
      chosen = sameKind
    else:
      chosen = matching[:1]
    for requirement in chosen:
      self._hold(requirement, kind, inner)

  def addOverload(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    As 'BaseSpace.addOverload', once the function is held to what is
    declared abstract at its signature; see '_screenRegistration'.
    """
    self._screenRegistration(name, 'overload', sig, func)
    BaseSpace.addOverload(self, name, sig, func)

  def addFlex(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    As 'BaseSpace.addFlex', once the function is held to what is
    declared abstract at its classes; see '_screenRegistration'.
    """
    self._screenRegistration(name, 'flex', sig, func)
    BaseSpace.addFlex(self, name, sig, func)

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    As 'BaseSpace.addVariadic', once the function is held to what is
    declared abstract at its signature; see '_screenRegistration'.
    """
    self._screenRegistration(name, 'variadic', sig, func)
    BaseSpace.addVariadic(self, name, sig, func)

  def _holdOverloads(self, requirement: Requirement) -> None:
    """
    A method declared plainly may be written as overloads of its name.
    Whether they implement it shows only once the body has ended: one of
    them, of the same kind of method, must take what is declared.
    Overloads that are all abstract declare the name anew and implement
    nothing. An overload registering something that is no Python
    function, as a builtin, shows nothing of what it takes and
    implements nothing either, as such a value bound plainly at the name
    is refused.

    Raises
    ------

    WrongImplementation
      The body wrote overloads at the name, and none takes what is
      declared.
    """
    name, kind = requirement[0], requirement[4]
    declared = self._declaredShape(requirement)
    kinds = self._gatherFunctionKinds((self,), name)
    written = False
    for role in ('overload', 'flex', 'variadic'):
      for sig, func in self._registeredIn(self, role, name):
        if isinstance(func, abstract):
          continue
        written = True
        inner = func
        if isinstance(func, CallMeMaybe):
          #  This branch is reached by the following:
          #  - One order of a flexible declaration, which holds its
          #    function
          inner = func.__wrapped__
        if not isinstance(inner, FunctionType):
          #  This branch is reached by the following:
          #  - The overload registers a builtin or another callable that
          #    is no Python function, which implements nothing
          continue
        own = self._kindIn(kinds, func)
        shape = self._signatureShape(role, sig, func, own)
        if own is kind and abstract.fits(declared, shape):
          return
    if not written:
      return
    className = self.getClassName()
    label = self._label(requirement)
    declaredText = abstract.describe(kind, declared)
    writtenText = 'no overload that takes it'
    raise WrongImplementation(className, label, declaredText, writtenText)

  def settleAbstract(self, ) -> tuple[str, ...]:
    """
    Once the body has ended, the class must know what it still lacks,
    since making an object of it is refused for as long as anything is
    left.

    Implementation
    --------------

    An inherited requirement the body did not answer is left. One it
    answered was held to the declaration at the line that wrote it,
    except a method declared plainly and written as overloads, which is
    held here. What the body itself declared is left as well, and is
    kept for the classes based on this one.

    Returns
    -------

    tuple[str, ...]
      What is not implemented, each named as '_label' names it: first
      what is inherited, then what the body declared.

    Raises
    ------

    WrongImplementation
      The body overloads a name a base declares plainly, and none of the
      overloads can take what is declared.
    """
    missing = []
    for requirement in self.getInheritedAbstract():
      if not self._spaceBinds(self, requirement):
        missing.append(requirement)
      elif requirement[1] == 'plain':
        if not dict.__contains__(self, requirement[0]):
          self._holdOverloads(requirement)
    declared = self.getDeclaredAbstract()
    self.__declared_abstract__ = declared
    missing.extend(declared)
    return (*(self._label(requirement) for requirement in missing),)
