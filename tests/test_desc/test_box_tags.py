"""
TestBoxTags subclasses 'DescTest' from the 'tests.test_desc' package and
pins the tags a box writes onto an object it creates: '__field_name__',
'__field_owner__' and '__field_box__' name the box that created the
object. They are written past the object's own '__setattr__', and left
off an object the box did not create, a class, an object whose class
declares '__no_box_tag__', an enumeration member and an object without an
instance dict. The opt-out is read past any '__getattr__',
'__class_getattr__' or reimplemented '__getattribute__' of the class, so
only a class that declares it, or inherits it, is left untagged.
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

  def test_class_getattr_hook_tagged(self) -> None:
    """
    Testing that an object whose class answers every name through
    '__class_getattr__' is still tagged.
    """

    class Lenient(BaseObject):
      @classmethod
      def __class_getattr__(cls, name: str) -> Any:
        return 'default'

    class Owner(BaseObject):
      lenient = AttriBox[Lenient]()

    self.assertTrue(_isTagged(Owner().lenient))

  def test_metaclass_getattr_tagged(self) -> None:
    """
    Testing that an object whose metaclass answers every missing name in
    '__getattr__' is still tagged.
    """

    class Answering(type):
      def __getattr__(cls, name: str) -> Any:
        return True

    class Plain(metaclass=Answering):
      pass

    class Owner(BaseObject):
      plain = AttriBox[Plain]()

    self.assertTrue(_isTagged(Owner().plain))

  def test_metaclass_getattribute_tagged(self) -> None:
    """
    Testing that an object whose metaclass reimplements '__getattribute__'
    to claim the opt-out is still tagged.
    """

    class Claiming(type):
      def __getattribute__(cls, name: str) -> Any:
        if name == '__no_box_tag__':
          return True
        return type.__getattribute__(cls, name)

    class Plain(metaclass=Claiming):
      pass

    class Owner(BaseObject):
      plain = AttriBox[Plain]()

    self.assertTrue(_isTagged(Owner().plain))

