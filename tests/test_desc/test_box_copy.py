"""
TestBoxCopy subclasses 'DescTest' from the 'tests.test_desc' package and
pins that a box is its own copy, so that a copy of an object a box
created, or of the object owning the field, still names the box declared
on the class through '__field_box__', rather than a detached copy of it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject

from . import DescTest


class TestBoxCopy(DescTest):
  """
  TestBoxCopy provides tests for copies of boxes and of the objects they
  create.
  """

  def test_deepcopy_of_created_object(self) -> None:
    """
    Testing that a deep copy of an object an 'AttriBox' created is a new
    object that names the box declared on the class.
    """

    class Config:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      config = AttriBox[Config](1)

    original = Owner().config
    copied = copy.deepcopy(original)
    self.assertIsNot(copied, original)
    self.assertEqual(copied.x, 1)
    self.assertIs(copied.__field_box__, Owner.config)

  def test_shallow_copy_of_created_object(self) -> None:
    """
    Testing that a shallow copy of an object an 'AttriBox' created names
    the box declared on the class.
    """

    class Config:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      config = AttriBox[Config](1)

    copied = copy.copy(Owner().config)
    self.assertIs(copied.__field_box__, Owner.config)

  def test_deepcopy_of_owner(self) -> None:
    """
    Testing that a deep copy of the object owning the field holds a copy
    of the created object, which names the box declared on the class.
    """

    class Config:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      config = AttriBox[Config](1)

    owner = Owner()
    original = owner.config
    copiedOwner = copy.deepcopy(owner)
    self.assertIsNot(copiedOwner.config, original)
    self.assertIs(copiedOwner.config.__field_box__, Owner.config)

  def test_deepcopy_keeps_box_defaults(self) -> None:
    """
    Testing that a deep copy of a created object leaves the default
    arguments of its box alone, since the box is not copied.
    """

    class Seed:
      def __init__(self, n: int = 0) -> None:
        self.n = n

    seed = Seed(3)

    class Owner(BaseObject):
      seeded = AttriBox[Seed](seed)

    copied = copy.deepcopy(Owner().seeded)
    self.assertIs(copied.__field_box__.getPosArgs()[0], seed)

  def test_deepcopy_of_fix_box_object(self) -> None:
    """
    Testing that a deep copy of an object a 'FixBox' created names the box
    declared on the class.
    """

    class Config:
      def __init__(self, x: int = 0) -> None:
        self.x = x

    class Owner(BaseObject):
      config = FixBox[Config](1)

    copied = copy.deepcopy(Owner().config)
    self.assertIs(copied.__field_box__, Owner.config)

  def test_deepcopy_of_member_value(self) -> None:
    """
    Testing that a deep copy of the value of an enumeration member names
    the 'Kee' that created it.
    """

    class Rgb:
      def __init__(self, r: int = 0, g: int = 0, b: int = 0) -> None:
        self.r, self.g, self.b = r, g, b

    class Color(KeeNum):
      RED = Kee[Rgb](255, 0, 0)

    value = Color.RED.value
    copied = copy.deepcopy(value)
    self.assertIsNot(copied, value)
    self.assertIs(copied.__field_box__, value.__field_box__)
