"""
TestFastBoxSlotsOwner subclasses 'DescTest' and pins that a 'FastBox'
refuses an owner whose instances have no '__dict__', a class declaring
'__slots__' without one, with 'MissingInstanceDict' as the class is
created, as 'AttriBox' does. A box installed on such a class with
'setattr' afterwards is refused the same way at the first access. It used
to fail with the bare 'AttributeError' of the missing '__dict__', which
'hasattr' read as the attribute being absent.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute.desc import MissingInstanceDict

from . import DescTest


class WithDict:
  """WithDict declares slots including an instance dict."""

  __slots__ = ('a', '__dict__')

  x = FastBox[int](1)


class TestFastBoxSlotsOwner(DescTest):
  """
  TestFastBoxSlotsOwner provides tests for a 'FastBox' on a slots-only
  owner.
  """

  def test_class_refused(self) -> None:
    """The class statement raises, naming the owner and the field."""
    with self.assertRaises((MissingInstanceDict, RuntimeError)) as context:
      class Slotted:
        __slots__ = ('a',)
        x = FastBox[int](1)
    e = self._unwrapSetName(context.exception, MissingInstanceDict)
    self.assertIsInstance(e, MissingInstanceDict)
    self.assertEqual(e.ownerName, 'Slotted')
    self.assertEqual(e.fieldName, 'x')

  def test_installed_later_refused(self) -> None:
    """A box set on a slots-only class after it exists is refused at a
    read, a write and a deletion, and 'hasattr' does not answer 'False'."""

    class Slotted:
      __slots__ = ('a',)

    setattr(Slotted, 'x', WithDict.__dict__['x'])
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict):
      _ = slotted.x
    with self.assertRaises(MissingInstanceDict):
      slotted.x = 2
    with self.assertRaises(MissingInstanceDict):
      del slotted.x
    with self.assertRaises(MissingInstanceDict):
      hasattr(slotted, 'x')

  def test_dict_slot_works(self) -> None:
    """An owner whose slots include '__dict__' works as any other."""
    withDict = WithDict()
    self.assertEqual(withDict.x, 1)
    withDict.x = 2
    self.assertEqual(withDict.x, 2)
