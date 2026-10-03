"""
TestFrozenCopyState subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that a copy of a frozen 'EZData' instance keeps the state
the instance holds beyond its fields. A frozen class can only derive state
by writing past its own '__setattr__', usually in '__post_init__', and a
copy that rebuilds the fields alone loses that state. An 'AttriBox' whose
default is an instance of its field type deep-copies that default for
every owner, so the loss also reaches a box default without any explicit
copy. A non-frozen instance keeps its state through a copy, and a frozen
one must copy alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject

from . import EZTest


class Frozen(EZData, frozen=True):
  """Frozen derives two attributes in '__post_init__': a value computed
  from its field, and a reference back to the instance itself."""

  x = EZField[float](3.0)

  def __post_init__(self) -> None:
    object.__setattr__(self, 'double', self.x * 2)
    object.__setattr__(self, 'me', self)


class Thawed(EZData):
  """Thawed derives the same value as 'Frozen' without being frozen."""

  x = EZField[float](3.0)

  def __post_init__(self) -> None:
    self.double = self.x * 2


class OwnCopy(EZData, frozen=True):
  """OwnCopy defines how it is copied, answering with a marker that tells
  which of its methods ran."""

  x = EZField[float](3.0)

  def __copy__(self) -> str:
    return 'own __copy__'

  def __deepcopy__(self, memo: dict) -> str:
    return 'own __deepcopy__'


class TestFrozenCopyState(EZTest):
  """
  TestFrozenCopyState provides tests for the state a copy of a frozen
  'EZData' instance keeps beyond the fields.
  """

  def test_copy_keeps_derived_state(self) -> None:
    """
    A shallow copy keeps the value 'Frozen' derived, and its reference
    back to the instance still points at the original, as a shallow copy
    of any object would.
    """
    original = Frozen(2.0)
    clone = copy(original)
    self.assertEqual(clone.double, 4.0)
    self.assertIs(clone.me, original)

  def test_deepcopy_keeps_derived_state(self) -> None:
    """
    A deep copy keeps the derived value, and its reference back to the
    instance points at the copy rather than at the original.
    """
    original = Frozen(2.0)
    clone = deepcopy(original)
    self.assertEqual(clone.double, 4.0)
    self.assertIs(clone.me, clone)

  def test_box_default_keeps_derived_state(self) -> None:
    """
    An 'AttriBox' deep-copies a default that is already an instance of its
    field type, so each owner receives a copy of its own, which keeps the
    derived value and refers to itself rather than to the instance in the
    class body. A default that could not be copied would be shared by
    every owner instead.
    """

    class Holder(BaseObject):
      point = AttriBox[Frozen](Frozen(2.0))

    first, second = Holder().point, Holder().point
    self.assertIsNot(first, second)
    for point in (first, second):
      self.assertEqual(point.double, 4.0)
      self.assertIs(point.me, point)

  def test_own_copy_methods_are_used(self) -> None:
    """
    A frozen class that defines its own '__copy__' and '__deepcopy__' is
    copied through them.
    """
    self.assertEqual(copy(OwnCopy()), 'own __copy__')
    self.assertEqual(deepcopy(OwnCopy()), 'own __deepcopy__')

  def test_thawed_copies_keep_derived_state(self) -> None:
    """
    A non-frozen instance keeps the value it derived through a shallow and
    a deep copy, which is the behaviour a frozen instance has to match.
    """
    original = Thawed(2.0)
    self.assertEqual(copy(original).double, 4.0)
    self.assertEqual(deepcopy(original).double, 4.0)
