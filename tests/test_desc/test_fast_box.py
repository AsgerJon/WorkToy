"""
TestFastBox tests the 'FastBox' descriptor: the lean, type-enforced
attribute that trades AttriBox's hooks, context, sentinels, and
coercion for speed. The tests pin the value contract (lazy default,
fresh per-instance defaults, strict typing, delete semantics) and the
claims that motivated the design: no context machinery, yet nested
and per-instance access stay correct.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute import TypeException, MissingVariable
from . import DescTest


class _Vec:
  """Two float FastBoxes with non-trivial defaults and no '__init__'
  assignment, so reads exercise the lazy-default path."""

  x = FastBox[float](0.0)
  y = FastBox[float](1.0)


class _Bag:
  """A mutable-default FastBox: each instance must get its own list."""

  items = FastBox[list]()


class _Base:
  pass


class _Sub(_Base):
  pass


class _Holder:
  """A class-typed FastBox, for the subclass-acceptance check."""

  item = FastBox[_Base]()


class _Inner:
  v = FastBox[int](7)


class _Outer:
  inner = FastBox[_Inner]()


class TestFastBox(DescTest):
  """Contract and design-claim tests for 'FastBox'."""

  #  Declaration and binding

  def test_class_access_returns_descriptor(self) -> None:
    """Class-level access yields the descriptor, not a value."""
    self.assertIsInstance(_Vec.x, FastBox)

  def test_set_name_records_names(self) -> None:
    """'__set_name__' records the field name and the backing key."""
    self.assertEqual(_Vec.x.__field_name__, 'x')
    self.assertEqual(_Vec.x.__private_name__, '__fast_x__')

  #  Lazy defaults

  def test_lazy_default_read(self) -> None:
    """First read builds the default from the captured arguments."""
    vec = _Vec()
    self.assertEqual(vec.x, 0.0)
    self.assertEqual(vec.y, 1.0)
    self.assertIsInstance(vec.x, float)

  def test_default_is_fresh_per_instance(self) -> None:
    """A mutable default is rebuilt per instance, never shared."""
    a, b = _Bag(), _Bag()
    self.assertIsNot(a.items, b.items)
    a.items.append(69)
    self.assertEqual(a.items, [69])
    self.assertEqual(b.items, [])

  #  Writes

  def test_write_accepts_exact_type(self) -> None:
    """A correctly typed write is stored and read back."""
    vec = _Vec()
    vec.x = 2.0
    self.assertEqual(vec.x, 2.0)

  def test_write_accepts_subclass(self) -> None:
    """'isinstance' semantics: a subclass instance is accepted."""
    holder = _Holder()
    sub = _Sub()
    holder.item = sub
    self.assertIs(holder.item, sub)

  def test_write_rejects_wrong_type(self) -> None:
    """A wrongly typed write raises 'TypeException'."""
    vec = _Vec()
    with self.assertRaises(TypeException) as context:
      vec.x = 'nope'
    e = context.exception
    self.assertEqual(e.varName, 'x')
    self.assertEqual(e.actualObject, 'nope')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_write_rejects_int_for_float(self) -> None:
    """FastBox is strict: the numeric tower is not applied, so an int
    is rejected for a float field (the deliberate no-coercion
    sacrifice)."""
    vec = _Vec()
    with self.assertRaises(TypeException):
      vec.x = 3

  #  Deletion

  def test_delete_resets_to_default(self) -> None:
    """Deleting a set value drops it; the next read rebuilds the
    default rather than raising."""
    vec = _Vec()
    vec.x = 5.0
    del vec.x
    self.assertEqual(vec.x, 0.0)

  def test_delete_unset_raises(self) -> None:
    """Deleting an attribute that was never set raises
    'MissingVariable'."""
    vec = _Vec()
    with self.assertRaises(MissingVariable) as context:
      del vec.x
    e = context.exception
    self.assertIs(e.instance, vec)
    self.assertEqual(e.varName, 'x')

  #  No-context design claims

  def test_per_instance_isolation(self) -> None:
    """The shared descriptor object never clobbers per-instance state:
    two instances keep independent values."""
    a, b = _Vec(), _Vec()
    a.x = 1.0
    b.x = 2.0
    self.assertEqual(a.x, 1.0)
    self.assertEqual(b.x, 2.0)

  def test_nested_access(self) -> None:
    """Nested FastBox access works with no context machinery, because
    every '__get__' reads its own 'instance' parameter."""
    outer = _Outer()
    self.assertIsInstance(outer.inner, _Inner)
    self.assertEqual(outer.inner.v, 7)
    inner = _Inner()
    inner.v = 9
    outer.inner = inner
    self.assertEqual(outer.inner.v, 9)

  #  Guards

  def test_missing_field_type(self) -> None:
    """A FastBox built without 'FastBox[T]' has no field type, so
    materialising its default raises 'MissingVariable'."""
    fast = FastBox()
    with self.assertRaises(MissingVariable) as context:
      fast._build()
    e = context.exception
    self.assertIs(e.instance, fast)
    self.assertEqual(e.varName, '__field_type__')
    self.assertIn(type, e.expectedTypes)
