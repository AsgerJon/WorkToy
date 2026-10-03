"""
EZMeta is the metaclass behind 'EZData'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from ..desc import Field
from ..dispatch import TypeSig
from ..mcls import BaseMeta
from . import EZSpace, EZField

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Iterator

  from . import EZMeta

  AsTypeSig: TypeAlias = Callable[..., TypeSig]
  Bases: TypeAlias = tuple[EZMeta, ...]


class EZMeta(BaseMeta):
  """
  EZMeta is the metaclass behind 'EZData'. On top of the
  construction protocol it inherits from 'BaseMeta', it hosts the
  class-level introspection accessors ('fields', 'sig',
  'isFrozen', 'isOrdered', 'kwOnly'), pins '__field_owner__' on
  every field after class creation, and provides 'isCongruent'
  for structural equality between EZData classes that declare
  the same field-type signature.

  Two classes are 'congruent' when their field-type tuples
  compare equal under 'TypeSig.__eq__'. The generated '__eq__'
  on EZData instances uses 'isCongruent' to admit cross-class
  equality, so a 'FrozenComplex(EZComplex)' instance can
  compare equal to its non-frozen parent's instances.

  Iteration, length and membership of a class run over its fields and
  are the metaclass's own, so an EZData body binding '__class_iter__',
  '__class_len__' or '__class_contains__' is refused with
  'ShadowedClassHook'; the other class hooks work as on any class.

  Attributes
  ----------
  fields : tuple[EZField, ...]
    The EZField descriptors declared on the class, in
    declaration order (own and inherited).
  sig : TypeSig
    The field-type signature used for congruence comparisons.
  isFrozen : bool
    Whether the class was declared with any of the 'frozen'
    synonyms.
  isOrdered : bool
    Whether the class was declared with any of the 'ordered'
    synonyms.
  kwOnly : bool
    Whether the class was declared with any of the 'kwOnly'
    synonyms.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    The 'fields' getter returns the tuple of EZField descriptors
    declared on the class, in declaration order. It is drawn from the
    namespace's merged own+inherited mapping so subclasses see the full
    field surface.

    Returns
    -------
    tuple[EZField, ...]
      The EZFields declared on this class, in declaration order.
    """
    space: EZSpace = getattr(cls, '__namespace__')
    fields: dict[str, EZField] = space.getFields()
    return (*(field for _, field in fields.items()),)

  @sig.GET
  def _getSig(cls, ) -> TypeSig:
    """
    The 'sig' getter returns the field-type signature of the class as a
    'TypeSig'. It is used by 'isCongruent' to decide whether two classes
    share the same field structure and so admit cross-class equality.

    Returns
    -------
    TypeSig
      The ordered tuple of field types wrapped in a 'TypeSig'.
    """
    return TypeSig(*(f.fieldType for f in cls), )

  @isFrozen.GET
  def _getIsFrozen(cls, ) -> bool:
    """
    The 'isFrozen' getter returns the resolved 'frozen' build-option
    flag set during 'EZHook.postCompilePhase'. It is truthy when the
    class was declared with any of the 'frozen', 'immutable', or
    'hashable' synonyms.

    Returns
    -------
    bool
      True if the class is frozen.
    """
    return True if getattr(cls, '__is_frozen__') else False

  @isOrdered.GET
  def _getIsOrdered(cls, ) -> bool:
    """
    The 'isOrdered' getter returns the resolved 'ordered' build-option
    flag set during 'EZHook.postCompilePhase'. It is truthy when the
    class was declared with any of the 'ordered', 'order', 'sortable',
    or 'comparable' synonyms.

    Returns
    -------
    bool
      True if the class supports ordering.
    """
    return True if getattr(cls, '__is_ordered__') else False

  @kwOnly.GET
  def _getKwOnly(cls, ) -> bool:
    """
    The 'kwOnly' getter returns the resolved 'kwOnly' build-option flag
    set during 'EZHook.postCompilePhase'. It is truthy when the class
    was declared with any of the 'kwOnly', 'keywordOnly', or 'kw_only'
    synonyms; it controls whether '__init__' accepts positional
    arguments and whether a generated '__match_args__' is the full
    field tuple or empty. A '__match_args__' set in the class body is
    kept whatever the flag.

    Returns
    -------
    bool
      True if the class is keyword-only.
    """
    return True if getattr(cls, '__kw_only__') else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(cls, ) -> Iterator[EZField]:
    """
    Iterating an 'EZData' class iterates its fields in declaration order.

    Returns
    -------
    Iterator[EZField]
      An iterator over the fields of this class, in declaration order.
    """
    yield from cls.fields

  def __len__(cls, ) -> int:
    """
    The length of an 'EZData' class is the number of its fields, own and
    inherited, which is what iterating it yields.

    Returns
    -------
    int
      The number of fields of this class.
    """
    return len(cls.fields)

  def __contains__(cls, item: Any) -> bool:
    """
    An 'EZData' class contains its fields: 'item in cls' is True when
    'item' is one of them. A field is recognised by identity, so the
    '__eq__' of 'item' is never asked.

    Returns
    -------
    bool
      True if 'item' is a field of this class.
    """
    return True if any(field is item for field in cls.fields) else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kw) -> EZSpace:
    """
    The '__prepare__' method returns the 'EZSpace' namespace object that
    collects the class body. Python calls it before executing the class
    body; the returned namespace stays in scope until the metaclass's
    '__new__' compiles it.

    Parameters
    ----------
    mcls : type
      The metaclass building the class.
    name : str
      The name of the class under construction.
    bases : Bases
      Spells out to 'tuple[EZMeta, ...]'. The base classes
      declared in the 'class Foo(...)' header.
    **kw
      Class keyword arguments forwarded to 'EZSpace'.

    Returns
    -------
    EZSpace
      A fresh namespace ready to receive the class body.
    """
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(mcls, EZMeta)
    return EZSpace(mcls, name, bases, **kw)

  def __init__(cls, name: str, bases: Bases, space: EZSpace, **kw) -> None:
    """
    The '__init__' method finalizes the class object after Python has
    built it. It walks every field on the class (own and inherited) and
    binds its '__field_owner__' to this class, so later access through
    'field.fieldOwner' returns the most-derived class that declared or
    inherited the field. The owners are bound before the inherited
    '__init__' runs, since that is what runs a '__class_init__' hook,
    which may read them.

    Parameters
    ----------
    name : str
      The name of the class.
    bases : Bases
      Spells out to 'tuple[EZMeta, ...]'. The base classes from
      the 'class Foo(...)' declaration.
    space : EZSpace
      The compiled namespace produced by 'EZSpace.compile'.
    **kw
      The class keyword arguments captured at '__prepare__' time.
    """
    for field in cls.fields:
      setattr(field, '__field_owner__', cls)
    super().__init__(name, bases, space, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def isCongruent(cls, other: Any) -> bool:
    """
    Returns True if 'other' is an 'EZData' class congruent with this
    one. Two classes are congruent when they sit in the same
    inheritance line (one is the other, a subclass of it, or a base it
    derives from) AND declare the identical field-type signature. So a
    subclass that adds or retypes a field is not congruent with its
    parent, and two unrelated classes that merely share a field-type
    layout are not congruent either. Only congruent classes may
    compare equal.

    Parameters
    ----------
    other : Any
      The object tested for congruence with this class.

    Returns
    -------
    bool
      True if 'other' is a same-line 'EZData' class whose field-type
      signature equals that of 'cls'.
    """
    mcls = type(cls)
    if not isinstance(other, mcls):
      return False
    related = issubclass(cls, other) or issubclass(other, cls)
    if not related:
      return False
    return True if cls.sig == other.sig else False
