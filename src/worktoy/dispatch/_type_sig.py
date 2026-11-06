"""
TypeSig encapsulates type signatures for overloads
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from ..core import MetaType
from ..core.sentinels import SentinelMeta, THIS, OWNER, ARGS
from ..utilities import textFmt
from ..waitaminute import TypeException, UncheckableType

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Self, Iterator, Union

  RawTypes: TypeAlias = tuple[type, ...]
  HASHABLE: TypeAlias = Union[type, int]


class TypeSig:
  """
  A dispatcher must find the function an overloaded call goes to, keyed
  by the classes of the positional arguments, at the cost of one
  dictionary lookup when the classes match a declaration exactly. The key
  must therefore be hashable and compare by the classes in order, so
  '(int, str)' and '(str, int)' are different keys. A declaration may end
  in a variadic tail, 'ARGS[int]', and two declarations written alike
  must be equal although each subscript builds a new object. And a
  declaration may name 'THIS' for a class that does not exist yet, which
  must come to mean that class once it exists, and on a clone placed on
  another class, that other class.

  Implementation
  --------------

  A 'TypeSig' holds the entries dispatch matches on and, apart from
  them, the entries as declared. Equality and hash go entry by entry, by
  identity, and an 'ARGS' entry by its inner type. 'swapTHIS' replaces
  'THIS' by the class in place, which changes the hash, and
  'restoreTHIS' brings the declared entries back. 'fromArgs' builds the
  signature of a call. The constructor checks nothing: the declaring
  code reads its entries through 'starARGS' and checks them with
  'validateTypes'. A signature supports iteration, 'len' and 'in', the
  latter by identity.

  Attributes
  ----------

  __raw_types__ : tuple
    The entries dispatch matches on.

  __declared_types__ : tuple
    The entries as declared, 'THIS' included.
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
    A clone of a placed dispatcher must be able to rebuild its signatures
    as they were declared, 'THIS' included, after placement replaced
    'THIS' in the entries dispatch matches on.

    Returns
    -------

    RawTypes
      A 'tuple[type, ...]', possibly ending in an 'ARGS' instance.
    """
    return self.__declared_types__

  @staticmethod
  def _getTypeName(rawType: HASHABLE) -> str:
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
    The dispatcher needs the signature of a call to look it up among the
    declared ones.

    Implementation
    --------------

    Each entry is the exact class of the argument at that position, so a
    'bool' gives 'bool', not 'int'; matching through subclasses is the
    work of the dispatcher.

    Parameters
    ----------

    *args
      The positional arguments of the call.

    Returns
    -------

    TypeSig
      The signature of their classes.
    """
    return cls(*[type(arg) for arg in args], )

  @staticmethod
  def starARGS(*types) -> tuple:
    """
    '@overload(int, ARGS)' must declare what '@overload(int, *ARGS)'
    declares: an 'int' followed by anything.

    Implementation
    --------------

    A bare 'ARGS' entry is replaced by what '*ARGS' unpacks to,
    'ARGS[object]'; every other entry is kept. A bare 'ARGS' anywhere but
    last thus becomes an instance in the middle, which 'validateTypes'
    refuses.

    Parameters
    ----------

    *types
      The declared entries.

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
    A declared signature no call could ever match must be refused where it
    is written, not discovered at the first call. Every call is matched
    with 'isinstance', so each entry must be a class 'isinstance' accepts:
    not 'list[int]', not 'typing.Any', not a 'Protocol' that is not runtime
    checkable. A sentinel cannot be instantiated, so none can match, except
    'THIS', which stands for a class. That holds for every sentinel,
    including those of a family a project builds on 'SentinelMeta'
    directly, which are no subclasses of 'Sentinel'. The check must not
    run the class-level instance check of a worktoy class,
    '__class_instancecheck__', which may assume the shape of what it is
    asked about: nothing in the declaration passed it a value.

    Implementation
    --------------

    An entry counts as a class when its type is a metaclass, since
    'isinstance(list[int], type)' answers 'True' on Python 3.9 and 3.10.
    'None' is refused with a 'TypeError' pointing at 'type(None)', the
    class a call passing 'None' is declared with. 'THIS' passes, any other
    class built by 'SentinelMeta' or a metaclass based on it raises
    'TypeError', a class built by a 'MetaType' passes,
    since 'isinstance' always answers for it, and every other entry is
    tried with 'isinstance(None, entry)'. The last entry may be an
    'ARGS' instance, whose inner type is checked instead, unless
    'variadic=False', as the flexible declarations pass since they reorder
    their entries.

    Parameters
    ----------

    *types
      The declared entries, as 'starARGS' returns them.

    **kwargs
      variadic : bool, optional
        Whether the last entry may be an 'ARGS'. Defaults to 'True'.
      declaration : str, optional
        The subscript of a box, as 'AttriBox[Any]', when the one entry is
        the field type of that box; the refusal then names the subscript
        and no position. Without it, the entries are those of an overload
        signature.

    Raises
    ------

    TypeException
      An entry, or the inner type of a final 'ARGS', is not a class.

    TypeError
      An entry is 'None', or a sentinel other than 'THIS'.

    UncheckableType
      An entry, or the inner type of a final 'ARGS', is a class
      'isinstance' refuses; a 'TypeError' as well.
    """
    variadic = kwargs.get('variadic', True)
    last = len(types) - 1
    for index, entry in enumerate(types):
      if variadic and index == last and isinstance(entry, ARGS):
        entry = entry.__inner_type__
      if entry is None:
        infoSpec = """The entry at position %d of the signature is 'None',
        a value, where a class is expected. A call passing 'None' is
        declared with the class of 'None', 'type(None)'."""
        raise TypeError(textFmt(infoSpec % index))
      if not issubclass(type(entry), type):
        raise TypeException('types[%d]' % index, entry, type)
      if entry is THIS:
        continue
      if isinstance(entry, SentinelMeta):
        infoSpec = """The entry at position %d of the signature is the
        sentinel '%s', which has no meaning in an overload signature: a
        sentinel cannot be instantiated, so no call could match. 'THIS'
        stands for the class the overload belongs to."""
        raise TypeError(textFmt(infoSpec % (index, entry.__name__)))
      if isinstance(entry, MetaType):
        #  This branch is reached by the following:
        #  - The entry is a worktoy class, which answers 'isinstance' as a
        #    plain class does, or through a class-level instance check of
        #    its own
        continue
      try:
        isinstance(None, entry)
      except TypeError as typeError:
        exception = cls._uncheckable(
          entry,
          types,
          index,
          typeError,
          **kwargs
          )
        raise exception from typeError

  @classmethod
  def _uncheckable(
      cls,
      entry: type,
      types: tuple,
      index: int,
      refusal: TypeError,
      **kwargs,
  ) -> UncheckableType:
    """
    The refusal must name the declaration as its author wrote it: the
    signature of an overload with the position of the entry, or the
    subscript of a box, which has no positions.

    Implementation
    --------------

    The keyword 'declaration', when given, is the subscript of a box;
    otherwise the signature is rendered from the entries.
    """
    try:
      declaration = kwargs['declaration']
    except KeyError:
      #  This branch is reached by the following:
      #  - The entries are those of an overload signature
      signature = cls._renderSignature(types)
      return UncheckableType(entry, signature, index, refusal)
    #  The rest of the method is reached by the following:
    #  - The entry is the field type of a box, which gave its subscript
    return UncheckableType(entry, declaration, None, refusal)

  @staticmethod
  def _renderSignature(types: tuple) -> str:
    names = [getattr(entry, '__name__', None) or str(entry) for entry in
             types]
    return '(%s)' % ', '.join(names)

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
    'LoadSpaceHook' must keep a declared signature apart from the one an
    'overload' object holds, since placing a class rewrites 'THIS' in a
    registered signature in place, and an 'overload' bound in two class
    bodies would otherwise hand the second class what the first fixed. A
    caller may also want a copy with 'THIS' or 'OWNER' replaced.

    Implementation
    --------------

    A new signature of the same class is built with 'THIS' and 'OWNER'
    replaced where a value is given, and a trailing 'ARGS[THIS]' turned
    into 'ARGS' of 'this'. The copy is declared with the replaced entries,
    so 'restoreTHIS' on it cannot bring 'THIS' back. A signature declared
    through 'overload' never holds 'OWNER'.

    Parameters
    ----------

    this : object, optional
      The value to put in place of 'THIS'.

    owner : type, optional
      The value to put in place of 'OWNER'.

    Returns
    -------

    TypeSig
      The copy.
    """
    newTypes = []
    for rawType in self.getRawTypes():
      if rawType is THIS and this is not None:
        newTypes.append(this)
      elif rawType is OWNER and owner is not None:
        newTypes.append(owner)
      elif isinstance(rawType, ARGS) and rawType.__inner_type__ is THIS:
        newTypes.append(rawType if this is None else ARGS[this])
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
    Once the class exists, '@overload(THIS)' must match instances of it.

    Implementation
    --------------

    'THIS' is replaced in place in the entries dispatch matches on, and a
    trailing 'ARGS[THIS]' becomes 'ARGS' of the class. The declared
    entries stay. The hash changes, so a signature holding 'THIS' must not
    be a dictionary key across the swap.

    Parameters
    ----------

    thisType : type
      The class to put in place of 'THIS'.
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
    A clone of a placed dispatcher must resolve 'THIS' to the class it is
    placed on next, not to the class of the original.

    Implementation
    --------------

    The declared entries replace the current ones in place.
    """
    self.__raw_types__ = self.__declared_types__

  def getBag(self) -> frozenset:
    """
    A flexible declaration of more than three classes accepts its classes
    in any order, so a call must find it by the classes of its arguments
    without regard to their order, and two declarations of the same classes
    in different orders must be recognized as one.

    Implementation
    --------------

    The entries are counted, and the counts frozen into a set of pairs, so
    '(int, int, str)' and '(str, int, int)' give one value. It is computed
    from the entries dispatch matches on, so it changes when 'THIS' is
    swapped, as the hash does.

    Returns
    -------

    frozenset
      A 'frozenset[tuple[type, int]]' of each class and how often it
      occurs.
    """
    return frozenset(Counter(self.getRawTypes()).items())
