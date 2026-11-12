"""
EZMeta is the metaclass behind 'EZData'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from ..dispatch import TypeSig
from ..mcls import BaseMeta
from . import EZSpace, EZField

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Iterator, Optional, TypeAlias

  from . import EZMeta

  Bases: TypeAlias = tuple[EZMeta, ...]


class EZMeta(BaseMeta):
  """
  A dataclass is asked things as a class: which fields it has, whether it
  is frozen, ordered or keyword-only, and whether an instance of another
  class may compare equal to one of its own. Its class statement must run
  in the namespace that gathers the fields, and every field must know the
  class it ended up on.

  Implementation
  --------------

  'EZMeta' is 'BaseMeta' with 'EZSpace' as its namespace. 'fields',
  'sig', 'isFrozen', 'isOrdered' and 'kwOnly' answer for a class.
  '__init__' binds every field of a class to it after the class is
  created.

  Two classes are 'congruent' when one is based on the other, their
  field names are the same in the same order, and each field is of the
  same type in both, compared by identity as 'TypeSig.__eq__' compares
  its entries; two unrelated classes of the same field types are not.
  The generated '__eq__' of an instance asks 'isCongruent', so a
  'FrozenComplex(EZComplex)' instance can compare equal to an instance
  of its non-frozen parent.

  Iterating, measuring and searching a class run over its fields and are
  the metaclass's own, so an EZData body binding '__class_iter__',
  '__class_len__' or '__class_contains__' is refused with
  'ShadowedClassHook'; the other class hooks work as on any class.

  Attributes
  ----------

  fields : tuple[EZField, ...]
    The fields of the class, own and inherited, in declaration order.

  sig : TypeSig
    The types of the fields in order, which congruence compares.

  isFrozen : bool
    Whether the class was declared with any of the spellings of 'frozen'.

  isOrdered : bool
    Whether the class, or the nearest class it is based on to say, was
    declared with any of the spellings of 'ordered'.

  kwOnly : bool
    Whether the class was declared with any of the spellings of 'kwOnly'.

  __post_init__ : Optional[Callable]
    'None' on the metaclass, a method on a class that defines the hook.
    What a dataclass without a '__post_init__' answers when the generated
    '__init__' looks the hook up on it: a class answers for the names of
    its metaclass after its own, so the lookup raises nothing. A
    '__post_init__' of the class or of any base comes first.
    'hasattr(cls, '__post_init__')' is therefore true for every
    dataclass, the class itself; an instance has the name only when a
    class defines the hook.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  #  What the lookup of '__post_init__' lands on for a dataclass that has
  #  none: a class answers for the names of its metaclass after its own.
  __post_init__: Optional[Callable] = None

  #  Annotations
  __is_frozen__: bool
  __is_ordered__: bool
  __kw_only__: bool

  #  Public Variables
  fields: Field[tuple[EZField, ...]] = Field()
  sig: Field[TypeSig] = Field()
  isFrozen: Field[bool] = Field()
  isOrdered: Field[bool] = Field()
  kwOnly: Field[bool] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fields.GET
  def _getFields(cls, ) -> tuple[EZField, ...]:
    """
    Code holding a dataclass must be able to ask for its fields, own and
    inherited, in the order the constructor takes them.

    Implementation
    --------------

    The merged mapping of the namespace of the class, as a tuple of its
    fields.

    Returns
    -------

    tuple[EZField, ...]
      The fields of the class, in declaration order.
    """
    space: EZSpace = getattr(cls, '__namespace__')
    fields: dict[str, EZField] = space.getFields()
    return (*(field for _, field in fields.items()),)

  @sig.GET
  def _getSig(cls, ) -> TypeSig:
    """
    Whether two classes hold values of the same shape is asked by comparing
    the types of their fields in order.

    Implementation
    --------------

    A 'TypeSig' of the field types of the class, built anew at every read.
    'isCongruent' asks the same of two classes without building one.

    Returns
    -------

    TypeSig
      The field types of the class, in declaration order.
    """
    return TypeSig(*(f.fieldType for f in cls), )

  @isFrozen.GET
  def _getIsFrozen(cls, ) -> bool:
    """
    Code holding a dataclass must be able to ask whether its instances are
    frozen.

    Implementation
    --------------

    The flag '__is_frozen__', which 'EZHook.postCompilePhase' resolves from
    the class keywords 'frozen', 'immutable' and 'hashable'.

    Returns
    -------

    bool
      Whether the class is frozen.
    """
    return True if getattr(cls, '__is_frozen__') else False

  @isOrdered.GET
  def _getIsOrdered(cls, ) -> bool:
    """
    Code holding a dataclass must be able to ask whether its instances
    compare with '<' and its kin.

    Implementation
    --------------

    The flag '__is_ordered__', which 'EZHook.postCompilePhase' resolves
    from the class keywords 'ordered', 'order', 'sortable' and
    'comparable', or else from the nearest class along the resolution order
    to say. It is false below an 'ordered=False'.

    Returns
    -------

    bool
      Whether the class is ordered.
    """
    return True if getattr(cls, '__is_ordered__') else False

  @kwOnly.GET
  def _getKwOnly(cls, ) -> bool:
    """
    Code holding a dataclass must be able to ask whether its constructor
    takes keywords alone.

    Implementation
    --------------

    The flag '__kw_only__', which 'EZHook.postCompilePhase' resolves from
    the class keywords 'kwOnly', 'keywordOnly' and 'kw_only'. It decides
    whether '__init__' takes positional arguments and whether a generated
    '__match_args__' names the fields or is empty; a '__match_args__' set
    in the class body is kept whatever the flag.

    Returns
    -------

    bool
      Whether the class is keyword-only.
    """
    return True if getattr(cls, '__kw_only__') else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(cls, ) -> Iterator[EZField]:
    """
    Iterating a dataclass, the class itself, goes over its fields in
    declaration order.

    Returns
    -------

    Iterator[EZField]
      The fields of the class.
    """
    yield from cls.fields

  def __len__(cls, ) -> int:
    """
    The length of a dataclass, the class itself, is the number of its
    fields, own and inherited, which is what iterating it yields.

    Returns
    -------

    int
      The number of fields of the class.
    """
    return len(cls.fields)

  def __contains__(cls, item: Any) -> bool:
    """
    A dataclass, the class itself, contains its fields, and a field is
    known by identity: an object that merely compares equal to a field is
    none.

    Implementation
    --------------

    Each field of the class is compared with 'item' by identity, so the
    '__eq__' of 'item' is never asked.

    Parameters
    ----------

    item : Any
      The object looked for.

    Returns
    -------

    bool
      Whether 'item' is a field of the class.
    """
    return True if any(field is item for field in cls.fields) else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kw) -> EZSpace:
    """
    The body of a dataclass must run in a namespace that gathers its
    fields.

    Implementation
    --------------

    A new 'EZSpace' is made for the class statement and given the class
    keywords. Python calls this method before the class body runs, and the
    namespace lives until '__new__' compiles it.

    Parameters
    ----------

    mcls : type
      The metaclass building the class.

    name : str
      The name of the class.

    bases : Bases
      A 'tuple[EZMeta, ...]' of the bases of the class statement.

    **kw
      The class keywords, passed on to 'EZSpace'.

    Returns
    -------

    EZSpace
      The namespace of the class body.
    """
    if TYPE_CHECKING:  # pragma: no cover, no mutate
      assert isinstance(mcls, EZMeta)
    return EZSpace(mcls, name, bases, **kw)

  def __init__(cls, name: str, bases: Bases, space: EZSpace, **kw) -> None:
    """
    A field must be able to say which class it belongs to, and for an
    inherited field that is the subclass holding its clone. A
    '__class_init__' hook of the class may read the owners, so they must be
    bound before it runs.

    Implementation
    --------------

    Every field of the class, own and inherited, takes the class as its
    '__field_owner__'. Then the inherited '__init__' runs, which is what
    calls '__class_init__'.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : Bases
      A 'tuple[EZMeta, ...]' of the bases of the class statement.

    space : EZSpace
      The namespace the class body ran in.

    **kw
      The class keywords.
    """
    for field in cls.fields:
      setattr(field, '__field_owner__', cls)
    super().__init__(name, bases, space, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def isCongruent(cls, other: Any) -> bool:
    """
    Equality between instances of two classes compares their values by
    position, so it may only be asked of classes whose values mean the
    same at each position. A subclass that adds or retypes a field is no
    such class for its parent, nor are two unrelated classes that merely
    hold fields of the same types. A class based on two dataclasses that
    declare the same names in opposite orders takes the order of the
    farther one, and without a look at the names it would compare equal to
    the nearer one while each name held another value.

    Implementation
    --------------

    'other' must be a class built by the metaclass of this one. The two
    must sit in one line of inheritance, one being the other, a subclass
    of it or a base of it; they must hold the same field names in the same
    order; and the type of each field must be the same class in both,
    which is what equal signatures say. The names and the types are read
    from the '__ez_fields__' of the two classes directly. 'sig' is not
    asked: it builds a 'TypeSig' through the getters of the metaclass and
    of every field, which costs many times the comparison, and equality
    between a class and its frozen subclass asks this method every time.

    Parameters
    ----------

    other : Any
      The object asked about.

    Returns
    -------

    bool
      Whether 'other' is a class congruent with this one.
    """
    mcls = type(cls)
    if not isinstance(other, mcls):
      return False
    related = issubclass(cls, other) or issubclass(other, cls)
    if not related:
      return False
    ownFields = type.__getattribute__(cls, '__ez_fields__')
    otherFields = type.__getattribute__(other, '__ez_fields__')
    if (*ownFields,) != (*otherFields,):
      return False
    for name, field in ownFields.items():
      if field.__field_type__ is not otherFields[name].__field_type__:
        return False
    return True
