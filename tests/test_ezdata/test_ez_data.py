"""
TestEZData subclasses 'EZTest' from the 'tests.test_ezdata' package and
provides tests for the 'EZData' class from the 'worktoy.ezdata' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField, EZMeta, fields
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ezdata import DuplicateError, \
  IncompleteFieldException, ReservedFieldError
from . import EZTest
from .examples import RichData, EZComplex, Circle, FullName, Point2D

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestEZData(EZTest):
  """
  TestEZData provides tests for the 'EZData' class from the 'worktoy.ezdata'
  package.
  """

  @classmethod
  def setUpClass(cls) -> None:
    super().setUpClass()
    cls.examples: tuple[EZMeta, ...] = (
      RichData,
      EZComplex,
      Circle,
      FullName,
      Point2D,
    )

  def test_duplicate_fields(self, ) -> None:
    """
    Test that duplicate fields are not allowed in 'EZData' classes.
    """
    with self.assertRaises(DuplicateError) as context:
      class Sus(EZData):  # noqa: F841
        name = EZField[float](0.0)
        name = EZField[float](0.0)  # noqa: F811
    e = context.exception
    self.assertEqual(e.name, 'name')
    expectedClassName = 'Sus'
    actualClassName = e.space.getClassName()
    self.assertEqual(actualClassName, expectedClassName)
    self.assertEqual(str(e), repr(e))

  def test_flags(self, ) -> None:
    """
    Test that the 'frozen' and 'slots' flags are properly set in 'EZData'
    classes.
    """

    self.assertFalse(EZComplex.isFrozen, )
    self.assertFalse(EZComplex.isOrdered, )
    self.assertFalse(EZComplex.kwOnly, )

  def test_congruency(self, ) -> None:
    """
    Test that 'EZComplex' is congruent with the 'ComplexMixin' from the
    'worktoy.work_test' package.
    """
    self.assertFalse(EZComplex.isCongruent(type('_', (), dict())))

  def test_non_fields(self, ) -> None:
    """
    This method tests that the 'EZData' classes can have other attributes
    than 'EZField' instances in their class body. It uses the 'RichData'
    class from the 'tests.test_ezdata.examples' package.
    """

    richFloat = RichData(.69)
    richInteger = RichData(420)

    self.assertEqual(float(richFloat), .69)
    self.assertEqual(int(richFloat), 1)
    self.assertEqual(float(richInteger), 420.0)
    self.assertEqual(int(richInteger), 420)
    self.assertEqual(str(richFloat), '0.69')
    self.assertEqual(str(richInteger), '420')
    floatRepr = repr(richFloat)
    self.assertIn('RichData', floatRepr)
    self.assertIn('.69', floatRepr)

  def test_bad_init_kwargs(self, ) -> None:
    """
    This method tests the 'TypeException' expected when a keyword argument
    passes a value of incorrect type.
    """

    with self.assertRaises(TypeException) as context:
      _ = RichData(value='four-twenty')
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_field_owner_name(self) -> None:
    """
    This method tests the '_getFieldOwner' and '_getFieldName' getters of
    'EZField' instances.
    """
    for example in self.examples:
      slotNames = example.__slots__
      for field in example.fields:
        self.assertIs(field.fieldOwner, example)
        self.assertIn(field.fieldName, slotNames)

  def test_incomplete_field_missing_type(self) -> None:
    """
    This method tests that an EZData class body containing an
    EZField without a type subscript ('EZField(value)' instead of
    'EZField[T](value)') fails at class-creation time with
    'IncompleteFieldException', not at first instantiation. The
    exception names the offending class, the offending field, and
    the missing piece.
    """
    with self.assertRaises(IncompleteFieldException) as context:
      class Sus(EZData):  # noqa: F841
        x = EZField(0.0)
    e = context.exception
    self.assertEqual(e.clsName, 'Sus')
    self.assertEqual(e.fieldName, 'x')
    self.assertIn('field type', e.missing)
    self.assertEqual(str(e), repr(e))

  def test_incomplete_field_missing_args(self) -> None:
    """
    This method tests that an EZData class body containing an
    EZField written as a bare subscript ('EZField[T]' instead of
    'EZField[T]()') fails at class-creation time with
    'IncompleteFieldException'. The exception names the offending
    class, the offending field, and the missing piece.
    """
    with self.assertRaises(IncompleteFieldException) as context:
      class Sus(EZData):  # noqa: F841
        x = EZField[float]
    e = context.exception
    self.assertEqual(e.clsName, 'Sus')
    self.assertEqual(e.fieldName, 'x')
    self.assertIn('construction arguments', e.missing)
    self.assertEqual(str(e), repr(e))

  def test_as_dict(self) -> None:
    """
    'asDict' returns a dict mapping each field name to its current
    value, in declaration order.
    """
    p = Point2D(3, 4)
    self.assertEqual(p.asDict(), {'x': 3.0, 'y': 4.0})

  def test_as_dict_returns_fresh_object(self) -> None:
    """
    Each 'asDict' call returns a new dict so the caller can
    mutate the result without affecting the instance.
    """
    p = Point2D(3, 4)
    d1 = p.asDict()
    d2 = p.asDict()
    self.assertIsNot(d1, d2)
    d1['x'] = 999
    self.assertEqual(p.x, 3.0)

  def test_as_tuple(self) -> None:
    """
    'asTuple' returns a tuple of the field values in declaration
    order.
    """
    p = Point2D(3, 4)
    self.assertEqual(p.asTuple(), (3.0, 4.0))

  def test_as_tuple_matches_iter(self) -> None:
    """
    'asTuple' returns the same sequence as iterating the instance
    directly through the generated '__iter__'.
    """
    p = Point2D(3, 4)
    self.assertEqual(p.asTuple(), (*p,))

  def test_replace_basic(self) -> None:
    """
    'replace' returns a new instance of the same class with the
    named field overridden and the rest copied from the original.
    """
    p = Point2D(1, 2)
    q = p.replace(x=5)
    self.assertEqual(q.x, 5.0)
    self.assertEqual(q.y, 2.0)
    self.assertEqual(p.x, 1.0)

  def test_replace_multiple_fields(self) -> None:
    """
    'replace' accepts more than one keyword override at once.
    """
    p = Point2D(1, 2)
    q = p.replace(x=5, y=10)
    self.assertEqual(q.asTuple(), (5.0, 10.0))

  def test_replace_no_changes_is_fresh_copy(self) -> None:
    """
    'replace' with no overrides returns a distinct equal instance,
    not the original object.
    """
    p = Point2D(1, 2)
    q = p.replace()
    self.assertEqual(p, q)
    self.assertIsNot(p, q)

  def test_replace_on_frozen(self) -> None:
    """
    'replace' is the canonical way to derive a modified instance
    from a frozen one: the original stays untouched and the new
    instance is the same frozen class.
    """

    class FrozenPt(EZData, frozen=True):
      x = EZField[int](0)
      y = EZField[int](0)

    p = FrozenPt(1, 2)
    q = p.replace(x=5)
    self.assertEqual(q.x, 5)
    self.assertEqual(q.y, 2)
    self.assertIsInstance(q, FrozenPt)
    with self.assertRaises(AttributeError):
      q.x = 99

  def test_replace_on_kw_only(self) -> None:
    """
    'replace' works for keyword-only classes since the underlying
    construction goes through '**kwargs'.
    """
    c = Circle(center=Point2D(1, 2), radius=3)
    c2 = c.replace(radius=10)
    self.assertEqual(c2.radius, 10.0)
    self.assertEqual(c2.center, Point2D(1, 2))

  def test_as_dict_method_override(self) -> None:
    """
    A subclass body that defines its own 'asDict' as a method
    wins over the generated default, since the generated method
    is installed in 'preCompilePhase' before the class body is
    merged in.
    """

    class Override(EZData):
      x = EZField[int](0)

      def asDict(self) -> dict:
        return {'custom': self.x}

    inst = Override(7)
    self.assertEqual(inst.asDict(), {'custom': 7})

  def test_as_dict_as_field_raises(self) -> None:
    """
    Declaring an EZField at a reserved name such as 'asDict'
    raises 'ReservedFieldError' at class-body time. Method
    overrides at the same name continue to be allowed; only
    EZField declarations are rejected.
    """
    with self.assertRaises(ReservedFieldError) as context:
      class Sus(EZData):  # noqa: F841
        asDict = EZField[int](0)
    e = context.exception
    self.assertEqual(e.name, 'asDict')
    self.assertEqual(e.space.getClassName(), 'Sus')
    self.assertEqual(str(e), repr(e))

  def test_replace_as_field_raises(self) -> None:
    """
    The 'replace' name is also reserved; declaring an EZField at
    that name raises 'ReservedFieldError'.
    """
    with self.assertRaises(ReservedFieldError):
      class Sus(EZData):  # noqa: F841
        replace = EZField[int](0)

  def test_replace_preserves_subclass(self) -> None:
    """
    'replace' returns an instance of 'type(self)', so a subclass
    instance produces a subclass instance, not the parent.
    """

    class TaggedPoint(Point2D):
      pass

    tp = TaggedPoint(1, 2)
    tp2 = tp.replace(x=9)
    self.assertIsInstance(tp2, TaggedPoint)
    self.assertEqual(tp2.x, 9.0)

  def test_replace_rejects_unknown_kwarg(self) -> None:
    """
    'replace' raises 'TypeError' when given a keyword argument
    that is not the name of a declared field, mirroring
    'dataclasses.replace' rather than the permissive behavior of
    the generated '__init__'.
    """
    p = Point2D(1, 2)
    with self.assertRaises(TypeError) as context:
      p.replace(bogus=42)
    msg = str(context.exception)
    self.assertIn('bogus', msg)
    self.assertIn('Point2D', msg)

  def test_replace_rejects_unknown_kwarg_alongside_known(self) -> None:
    """
    A mix of valid field names and an unknown one still raises;
    the valid kwargs do not mask the mistake.
    """
    p = Point2D(1, 2)
    with self.assertRaises(TypeError):
      p.replace(x=5, bogus=42)

  def test_post_init_normalizes_fields(self) -> None:
    """
    A class that defines '__post_init__' has the hook fired at
    the end of '__init__' with every field already populated,
    so the hook may mutate field values to normalize them.
    """

    class Greeter(EZData):
      name = EZField[str]('anonymous')

      def __post_init__(self) -> None:
        self.name = self.name.upper()

    g = Greeter('alice')
    self.assertEqual(g.name, 'ALICE')

  def test_post_init_can_validate(self) -> None:
    """
    '__post_init__' can raise to reject invalid field
    combinations, halting construction before the instance
    escapes.
    """

    class PositivePoint(EZData):
      x = EZField[int](0)
      y = EZField[int](0)

      def __post_init__(self) -> None:
        if self.x < 0 or self.y < 0:
          raise ValueError('coordinates must be non-negative')

    PositivePoint(1, 2)
    with self.assertRaises(ValueError):
      PositivePoint(-1, 2)

  def test_post_init_on_frozen_uses_object_setattr(self) -> None:
    """
    On a frozen class '__post_init__' must use
    'object.__setattr__' to bypass the frozen guard, since the
    generated '__setattr__' raises for every assignment.
    """

    class FrozenGreeter(EZData, frozen=True):
      name = EZField[str]('anonymous')

      def __post_init__(self) -> None:
        object.__setattr__(self, 'name', self.name.upper())

    g = FrozenGreeter('alice')
    self.assertEqual(g.name, 'ALICE')

  def test_post_init_fires_on_replace(self) -> None:
    """
    'replace' goes through '__init__' on the new instance, so
    '__post_init__' fires for the replacement as well as the
    original construction. Derived state stays consistent.
    """

    class Greeter(EZData):
      name = EZField[str]('anonymous')

      def __post_init__(self) -> None:
        self.name = self.name.upper()

    g = Greeter('alice')
    g2 = g.replace(name='bob')
    self.assertEqual(g2.name, 'BOB')

  def test_post_init_inherited_from_parent(self) -> None:
    """
    A subclass that does not define its own '__post_init__'
    still fires the parent's, since the hook lookup uses
    'getattr' on 'type(self)' which walks the MRO.
    """

    class Loud(EZData):
      name = EZField[str]('anonymous')

      def __post_init__(self) -> None:
        self.name = self.name.upper()

    class LoudChild(Loud):
      pass

    c = LoudChild('alice')
    self.assertEqual(c.name, 'ALICE')

  def test_post_init_as_field_raises(self) -> None:
    """
    Declaring an EZField at '__post_init__' raises
    'ReservedFieldError', protecting the hook contract from
    accidental shadowing.
    """
    with self.assertRaises(ReservedFieldError):
      class Sus(EZData):  # noqa: F841
        __post_init__ = EZField[int](0)

  def test_fields_on_class(self) -> None:
    """
    'fields(cls)' returns the tuple of EZField descriptors
    declared on an EZData class, matching 'cls.fields'.
    """
    self.assertEqual(fields(Point2D), Point2D.fields)
    self.assertEqual(len(fields(Point2D)), 2)

  def test_fields_on_instance(self) -> None:
    """
    'fields(instance)' returns the same tuple as
    'fields(type(instance))' so callers can pass either form.
    """
    p = Point2D(1, 2)
    self.assertEqual(fields(p), fields(Point2D))

  def test_fields_rejects_non_ezdata(self) -> None:
    """
    'fields' raises 'TypeError' when given a value that is
    neither an EZData class nor an instance of one.
    """
    with self.assertRaises(TypeError):
      fields('not an EZData')
    with self.assertRaises(TypeError):
      fields(int)

  def test_delete_rejected_on_non_frozen(self) -> None:
    """
    Deletion of a field is rejected on every EZData class, not
    just frozen ones. The EZData contract guarantees every
    declared field carries a value of its declared type;
    deletion would break that guarantee.
    """
    p = Point2D(1, 2)
    with self.assertRaises(AttributeError) as context:
      del p.x
    msg = str(context.exception)
    self.assertIn('Point2D', msg)
    self.assertIn('x', msg)
