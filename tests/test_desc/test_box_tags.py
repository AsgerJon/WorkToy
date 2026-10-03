"""
TestBoxTags subclasses 'DescTest' from the 'tests.test_desc' package and
pins the tags a box writes onto an object it creates: '__field_name__',
'__field_owner__' and '__field_box__' name the box that created the
object. They are written past the object's own '__setattr__', and left
off an object the box did not create, a class, an object whose class
declares '__no_box_tag__', an enumeration member and an object without an
instance dict.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag
from worktoy.mcls import BaseObject

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _isTagged(value: Any) -> bool:
  """Reports whether 'value' holds a box tag in its instance dict."""
  return True if '__field_box__' in getattr(value, '__dict__', {}) else False


class TestBoxTags(DescTest):
  """
  TestBoxTags provides tests for the box tags: which objects receive them,
  and which are left as their class made them.
  """

  def test_plain_value_tagged(self) -> None:
    """
    Testing that an object the box creates names the box, the field and
    the owner.
    """

    class Plain:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      plain = AttriBox[Plain](1)

    value = Owner().plain
    self.assertIs(value.__field_box__, Owner.plain)
    self.assertEqual(value.__field_name__, 'plain')
    self.assertIs(value.__field_owner__, Owner)

  def test_strict_setattr_held_and_tagged(self) -> None:
    """
    Testing that an object whose '__setattr__' refuses every write is
    still held, and tagged past that '__setattr__'.
    """

    class Strict:
      def __init__(self, x: int = 0) -> None:
        object.__setattr__(self, 'x', x)

      def __setattr__(self, key: str, value: Any) -> None:
        raise TypeError('immutable')

    class Owner(BaseObject):
      strict = AttriBox[Strict](1)

    value = Owner().strict
    self.assertEqual(value.x, 1)
    self.assertIs(value.__field_box__, Owner.strict)
    with self.assertRaises(TypeError):
      value.x = 2

  def test_frozen_dataclass_tagged(self) -> None:
    """
    Testing that a frozen dataclass instance created by the box is tagged.
    """

    @dataclass(frozen=True)
    class FrozenPoint:
      x: int = 0

    class Owner(BaseObject):
      point = AttriBox[FrozenPoint](1)

    value = Owner().point
    self.assertEqual(value.x, 1)
    self.assertIs(value.__field_box__, Owner.point)

  def test_frozen_ezdata_tagged(self) -> None:
    """
    Testing that a frozen 'EZData' instance created by the box is tagged,
    and still compares by its fields.
    """

    class FrozenPoint(EZData, frozen=True):
      x = EZField[int](0)

    class Owner(BaseObject):
      point = AttriBox[FrozenPoint](1)

    value = Owner().point
    self.assertIs(value.__field_box__, Owner.point)
    self.assertEqual(value, FrozenPoint(1))

  def test_slotted_value_untagged(self) -> None:
    """
    Testing that an object without an instance dict is held untagged.
    """

    class Slotted:
      __slots__ = ('x',)

      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      slotted = AttriBox[Slotted](1)

    value = Owner().slotted
    self.assertEqual(value.x, 1)
    self.assertFalse(hasattr(value, '__dict__'))

  def test_no_box_tag_class_untagged(self) -> None:
    """
    Testing that an object whose class declares '__no_box_tag__' is left
    untagged.
    """

    class Refusing:
      __no_box_tag__ = True

      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      refusing = AttriBox[Refusing](1)

    value = Owner().refusing
    self.assertEqual(value.x, 1)
    self.assertFalse(_isTagged(value))

  def test_enum_member_untagged(self) -> None:
    """
    Testing that an 'Enum' member the box looks up through its class is
    left untagged.
    """

    class Color(Enum):
      RED = 1

    class Owner(BaseObject):
      color = AttriBox[Color](1)

    self.assertIs(Owner().color, Color.RED)
    self.assertFalse(_isTagged(Color.RED))

  def test_keenum_member_untagged(self) -> None:
    """
    Testing that a 'KeeNum' member the box looks up through its class is
    left untagged.
    """

    class Day(KeeNum):
      MON = Kee[int](1)

    class Owner(BaseObject):
      day = AttriBox[Day]('MON')

    self.assertIs(Owner().day, Day.MON)
    self.assertFalse(_isTagged(Day.MON))

  def test_keeflags_member_untagged(self) -> None:
    """
    Testing that a 'KeeFlags' member the box looks up through its class is
    left untagged and keeps its own owner.
    """

    class Perm(KeeFlags):
      READ = KeeFlag()

    class Owner(BaseObject):
      perm = AttriBox[Perm]('READ')

    self.assertIs(Owner().perm, Perm.READ)
    self.assertFalse(_isTagged(Perm.READ))
    self.assertIs(Perm.READ.__field_owner__, Perm)

  def test_uncopyable_default_untagged(self) -> None:
    """
    Testing that a default the box shares because it refuses to be copied
    is left untagged, since the box did not create it.
    """

    class Uncopyable:
      def __init__(self, x: int = 0) -> None:
        self.x = x

      def __deepcopy__(self, memo: dict) -> Any:
        raise TypeError('no copies')

    shared = Uncopyable(1)

    class Owner(BaseObject):
      item = AttriBox[Uncopyable](shared)

    self.assertIs(Owner().item, shared)
    self.assertFalse(_isTagged(shared))

  def test_self_copying_default_untagged(self) -> None:
    """
    Testing that a default whose copy is the object itself is left
    untagged, since the box did not create it.
    """

    class Lonely:
      def __deepcopy__(self, memo: dict) -> Any:
        return self

    single = Lonely()

    class Owner(BaseObject):
      item = AttriBox[Lonely](single)

    self.assertIs(Owner().item, single)
    self.assertFalse(_isTagged(single))

  def test_created_class_untagged(self) -> None:
    """
    Testing that a class the box creates is left untagged, since tags on
    a class would be inherited by its instances and subclasses.
    """

    class Owner(BaseObject):
      dyn = AttriBox[type]('Dyn', (), {})

    value = Owner().dyn
    self.assertIsInstance(value, type)
    self.assertNotIn('__field_box__', vars(value))

  def test_assigned_value_untagged(self) -> None:
    """
    Testing that an object assigned already of the field type is stored as
    it is, untagged, since the box did not create it.
    """

    class Plain:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      plain = AttriBox[Plain](1)

    owner = Owner()
    given = Plain(2)
    owner.plain = given
    self.assertIs(owner.plain, given)
    self.assertFalse(_isTagged(given))
