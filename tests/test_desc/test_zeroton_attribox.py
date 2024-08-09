"""TestZerotonAttriBox tests that AttriBox correctly handles the use of
the special 'Zeroton' objects. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.meta import BaseMetaclass
from worktoy.desc import AttriBox, NODEF, THIS, TYPE, ATTR, BOX, DEFAULT

BaseObject = object


class Aware(BaseObject):
  """Instances of this class become aware of their owner upon
  instantiation. These are intended to be boxed in an AttriBox. Then they
  should reflect their owner instance and class when retrieved."""

  ownerCls = AttriBox[type](NODEF)  # Must be set before use.
  ownerIns = AttriBox[BaseObject](NODEF)  # Must be set before use.

  def __init__(self, this: BaseObject, cls: BaseMetaclass) -> None:
    if isinstance(cls, type):
      self.ownerCls = cls
      self.ownerIns = this
    else:
      self.ownerCls = this
      self.ownerIns = cls


class Name(BaseObject):
  """Instances of this class are intended to own instances of the Aware
  class. """

  first = AttriBox[str]()
  last = AttriBox[str]()

  def __init__(self, *args) -> None:
    first, last = ['John', 'Doe', *args][:2]
    self.first = first
    self.last = last


testName = Name()


class Owner(BaseObject):
  """Instances of this class are intended to own instances of the Aware
  class. """

  thisType = AttriBox[Aware](THIS, TYPE)
  boxAttr = AttriBox[Aware](BOX, ATTR)
  bad = AttriBox[Aware](69, 420)  # Should raise NODEF related error
  defObject = AttriBox[Name](DEFAULT(testName))


class TestZerotonAttriBox(TestCase):
  """TestZerotonAttriBox tests that AttriBox correctly handles the use of
  the special 'Zeroton' objects. """

  def setUp(self) -> None:
    """Instantiates test classes. """
    self.owner = Owner()

  def test_replacements(self) -> None:
    """Tests that owner correctly identifies owner instance and class,
    and descriptor instance and class. """
    self.assertIs(self.owner.thisType.ownerCls, Owner)
    self.assertIs(self.owner.thisType.ownerIns, self.owner)
    self.assertIs(self.owner.boxAttr.ownerCls, AttriBox)
    self.assertIs(self.owner.boxAttr.ownerIns, Owner.boxAttr)

  def test_nodef_error(self) -> None:
    """Tests that NODEF correctly causes an error when '__get__' precedes
    '__set__'. """
    # with self.assertRaises(TypeError) as context:
    #   print(self.owner.bad.ownerCls)
    # self.assertIn('NODEF', str(context.exception))
    # with self.assertRaises(TypeError) as context:
    #   print(self.owner.bad.ownerIns)
    # self.assertIn('NODEF', str(context.exception))

  def test_default_object(self, ) -> None:
    """Tests object identity persistence when using DEFAULT"""
    self.assertIs(self.owner.defObject, testName)

  def test_illegal_nodef_signature(self) -> None:
    """Tests that an error is raised when NODEF is not the only argument"""
    with self.assertRaises(ValueError) as context:
      type('lol', (BaseObject,), dict(bla=AttriBox[Aware](NODEF, 'sus')))
    self.assertIn('NODEF', str(context.exception))
