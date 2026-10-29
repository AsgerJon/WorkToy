"""
TypeSig encapsulates type signatures for overloads
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import Sentinel, THIS, OWNER, ARGS
from ..utilities import textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self, Iterator, Union

  RawTypes: TypeAlias = tuple[type, ...]
  HASHABLE: TypeAlias = Union[type, int]


class TypeSig:
  """Hashable, ordered tuple of types used as a dispatch key.

  A 'TypeSig' represents the positional-argument type signature of a
  single overload. Equality and hashing are by type identity in the
  declared order, so 'TypeSig(int, str)' and 'TypeSig(str, int)' are
  distinct keys. The one exception is a trailing 'ARGS' entry, which
  compares by its inner type: every 'ARGS[int]' subscript builds a new
  instance, and two variadic signatures written the same way must still
  be equal. The signature is iterable and supports 'len' and 'in', the
  latter using identity comparison.

  A signature keeps the types it was declared with beside the types it
  dispatches on. 'swapTHIS' rewrites the latter, and 'restoreTHIS' puts
  the sentinel back from the former, which is what lets a clone of a
  placed 'Dispatcher' resolve 'THIS' to the class the clone is placed
  on.

  Use 'TypeSig.fromArgs(*args)' to derive a signature from concrete
  values (used by the dispatcher to look up a matching overload).
  Use 'swapTHIS(thisType)' to replace the 'THIS' sentinel with the
  enclosing class once the class is fully constructed; this is what
  lets '@overload(THIS)' work inside a class body.

  Hashing and the 'THIS' sentinel
  -------------------------------
  A 'TypeSig' hashes as the tuple of its raw types, wherever it is
  hashed. '@overload(THIS, ...)' registers a signature carrying the
  'THIS' sentinel while the enclosing class does not exist yet, and
  'THIS' is a class, so such a signature hashes through the sentinel,
  the same in every class body. That is harmless: the only dict keyed
  by such a signature while a class body runs is the registry of one
  'overload' object, filled as its decorators run, and within one class
  body every 'THIS' names the same class. Once the class exists,
  'swapTHIS' replaces the sentinel with the class in place, which
  changes the hash of the signature; from then on those registries are
  only ever iterated, and the dispatcher compiles fresh lookup tables
  from the swapped signatures, which hash through the class itself.

  Nothing here reads the call stack or the namespace of the class body,
  so the hashing runs alike on every interpreter, with or without
  support for inspecting frames. Equality is by identity per entry, a
  trailing 'ARGS' by its inner type, and 'ARGS' hashes by its inner
  type as well, so equal signatures hash alike.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __raw_types__ = None
  __declared_types__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getRawTypes(self) -> RawTypes:
    return self.__raw_types__

  def getDeclaredTypes(self) -> RawTypes:
    """
    The 'getDeclaredTypes' method returns the types the signature was
    declared with, which 'swapTHIS' leaves as they are.
    """
    return self.__declared_types__

  @staticmethod
  def _getTypeName(rawType: HASHABLE) -> str:
    """
    The '_getTypeName' method renders one entry of a signature as it is
    written in an '@overload' declaration: a class by its name, and a
    trailing 'ARGS' entry in its subscript form, such as 'ARGS[int]'.
    """
    if isinstance(rawType, ARGS):
      return str(rawType)
    return rawType.__name__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *rawTypes: type) -> None:
    self.__raw_types__ = rawTypes
    self.__declared_types__ = rawTypes

  @classmethod
  def fromArgs(cls, *args, ) -> Self:
    """
    The 'fromArgs' constructor builds a 'TypeSig' from concrete values by
    taking the type of each argument in order. This is how the dispatcher
    derives the lookup key for an incoming call.

    Parameters
    ----------
    *args : Any
        The concrete call arguments whose types form the signature.

    Returns
    -------
    Self
        A 'TypeSig' of the argument types, in order.
    """
    return cls(*[type(arg) for arg in args], )

  @staticmethod
  def starARGS(*types) -> tuple:
    """
    The 'starARGS' method reads a bare 'ARGS' in a declared signature as
    '*ARGS', unpacking it as the star does, so '@overload(int, ARGS)'
    declares what '@overload(int, *ARGS)' declares: an 'int' followed by
    any number of arguments of any type. Every other entry is kept as
    written. 'overload', 'overload.flex' and the 'overload' and 'flex' of
    a 'Dispatcher' read their types through it before validating them.

    Parameters
    ----------
    *types : type
        The declared entries, in order.

    Returns
    -------
    tuple
        The entries with every bare 'ARGS' unpacked.
    """
    out = []
    for entry in types:
      if entry is ARGS:
        out.extend(entry)
      else:
        out.append(entry)
    return (*out,)

  @classmethod
  def validateTypes(cls, *types, **kwargs) -> None:
    """
    The 'validateTypes' classmethod refuses every entry of a declared
    signature that is not a class, with 'TypeException' naming its
    position. Every entry is matched with 'isinstance' at dispatch, which
    raises its own 'TypeError' for anything else, such as 'list[int]' or
    a 'typing.Union'. The last entry may instead be an 'ARGS' of a class,
    marking the variadic tail, unless 'variadic=False' is passed, as the
    flexible declarations do, since they rearrange their entries. 'THIS'
    is a class and stands for the class itself, and is handled first.
    Every other sentinel, 'OWNER', 'DESC', 'DELETED', 'METACALL' and
    'Sentinel' itself, is a class too but cannot be instantiated, so a
    signature holding one could never match a call, and raises
    'TypeError'. The class test is that the type of the entry is a
    metaclass, since
    'isinstance(entry, type)' answers 'True' for 'list[int]' on Python
    3.9 and 3.10. An entry that 'isinstance' refuses, such as
    'typing.Any' or a 'Protocol' that is not runtime checkable, is a
    class by that test and raises 'TypeError' here instead of from inside
    the first call.

    Parameters
    ----------
    *types : type
        The declared entries, in order.
    **kwargs
        variadic : bool, optional
            Whether the last entry may be an 'ARGS'. Defaults to 'True'.

    Raises
    ------
    TypeException
        If an entry, or the inner type of a final 'ARGS', is not a class.
    TypeError
        If an entry, or the inner type of a final 'ARGS', is a sentinel
        other than 'THIS', or cannot be used with 'isinstance'.
    """
    variadic = kwargs.get('variadic', True)
    last = len(types) - 1
    for index, entry in enumerate(types):
      if variadic and index == last and isinstance(entry, ARGS):
        entry = entry.__inner_type__
      if not issubclass(type(entry), type):
        raise TypeException('types[%d]' % index, entry, type)
      if entry is THIS:
        continue
      if issubclass(entry, Sentinel):
        infoSpec = """The entry at position %d of the signature is the
        sentinel '%s', which has no meaning in an overload signature: a
        sentinel cannot be instantiated, so no call could match. 'THIS'
        stands for the class the overload belongs to."""
        raise TypeError(textFmt(infoSpec % (index, entry.__name__)))
      try:
        isinstance(None, entry)
      except TypeError as typeError:
        infoSpec = """The entry at position %d of the signature, '%s',
        cannot be used with 'isinstance', which every call is matched
        by."""
        name = getattr(entry, '__name__', None) or str(entry)
        raise TypeError(textFmt(infoSpec % (index, name))) from typeError

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[type]:
    yield from self.getRawTypes()

  def __hash__(self, ) -> int:
    return hash(self.getRawTypes())

  def __len__(self, ) -> int:
    return len(self.getRawTypes())

  def __contains__(self, type_: HASHABLE) -> bool:
    for rawType in self.getRawTypes():
      if rawType is type_:
        return True
    return False

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, type(self)):
      return NotImplemented
    if len(self) != len(other):
      return False
    for this, that in zip(self, other):
      if this is that:
        continue
      if isinstance(this, ARGS) and this == that:
        continue
      return False
    return True

  def __str__(self) -> str:
    infoSpec = """<%s: %s>"""
    typeStr = '[%s]' % ', '.join(self._getTypeName(t) for t in self)
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, typeStr))

  def __repr__(self) -> str:
    infoSpec = """%s(%s)"""
    typeStr = ', '.join(self._getTypeName(t) for t in self)
    return textFmt(infoSpec % (type(self).__name__, typeStr))

  def __call__(self, this: object = None, owner: type = None) -> Self:
    """
    Calling a 'TypeSig' returns a new 'TypeSig' with 'THIS' replaced by
    'this' and 'OWNER' replaced by 'owner'. Either argument can be
    omitted to leave the corresponding sentinel in place, and a call
    with neither copies the signature, which 'LoadSpaceHook' relies on
    to record a declared signature apart from the one the 'overload'
    object keeps, since placement rewrites 'THIS' in place. It serves any
    caller wanting a substituted copy while the original keeps its
    sentinel for 'swapTHIS' to rewrite in place.

    Parameters
    ----------
    this : object, optional
        The value to substitute for the THIS sentinel.
    owner : type, optional
        The value to substitute for the OWNER sentinel.

    Returns
    -------
    Self
        A new 'TypeSig' with the requested substitutions applied.
    """
    newTypes = []
    for rawType in self.getRawTypes():
      if rawType is THIS and this is not None:
        newTypes.append(this)
      elif rawType is OWNER and owner is not None:
        newTypes.append(owner)
      else:
        newTypes.append(rawType)
    new = type(self)(*newTypes)
    # noinspection PyTypeChecker
    return new

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def swapTHIS(self, thisType: type) -> None:
    """
    The 'swapTHIS' method replaces the THIS sentinel in the raw types
    with 'thisType' in place, called once the enclosing class exists so
    that '@overload(THIS)' resolves to the finished class. A trailing
    'ARGS[THIS]' is rebuilt as 'ARGS' of the class, so a variadic
    signature over the class matches calls of any length.

    Parameters
    ----------
    thisType : type
        The class to substitute for the THIS sentinel.
    """
    newTypes = []
    for rawType in self.getRawTypes():
      if rawType is THIS:
        newTypes.append(thisType)
      elif isinstance(rawType, ARGS) and rawType.__inner_type__ is THIS:
        newTypes.append(ARGS[thisType])
      else:
        newTypes.append(rawType)
    self.__raw_types__ = (*newTypes,)

  def restoreTHIS(self) -> None:
    """
    The 'restoreTHIS' method puts the types back as they were declared,
    'THIS' included, in place, undoing 'swapTHIS'. A signature never
    swapped is left as it is.
    """
    self.__raw_types__ = self.__declared_types__
