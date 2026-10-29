"""
TestAttriBoxSlotsOwner subclasses 'DescTest' and pins that an 'AttriBox'
refuses an owner whose instances have no '__dict__', a class declaring
'__slots__' without one, with 'MissingInstanceDict' naming the owner and
the field, as the class is created. A box installed on such a class with
'setattr' afterwards, which never receives '__set_name__', is refused the
same way at the first access. The store used to fail with the bare
'AttributeError' of 'object.__setattr__', which the attribute protocol
reads as the attribute being absent, so 'hasattr' answered 'False' and
nothing said the box could not work there.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import MissingInstanceDict

from . import DescTest


class WithDict:
  """WithDict declares slots including an instance dict."""

  __slots__ = ('a', '__dict__')

  x = AttriBox[int](1)


class TestAttriBoxSlotsOwner(DescTest):
  """
  TestAttriBoxSlotsOwner provides tests for a box on a slots-only owner.
  """

  def test_class_refused(self) -> None:
    """The class statement raises, naming the owner and the field."""
    with self.assertRaises((MissingInstanceDict, RuntimeError)) as context:
      class Slotted:
        __slots__ = ('a',)
        x = AttriBox[int](1)
    e = self._unwrapSetName(context.exception, MissingInstanceDict)
    self.assertIsInstance(e, MissingInstanceDict)
    self.assertEqual(e.ownerName, 'Slotted')
    self.assertEqual(e.fieldName, 'x')
    self.assertIn("'Slotted.x'", str(e))
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, TypeError)

  def test_installed_later_refused(self) -> None:
    """A box set on a slots-only class after it exists is refused at the
    first access, and 'hasattr' does not answer 'False'."""

    class Slotted:
      __slots__ = ('a',)

    setattr(Slotted, 'x', WithDict.__dict__['x'])
    with self.assertRaises(MissingInstanceDict):
      _ = Slotted().x
    with self.assertRaises(MissingInstanceDict):
      hasattr(Slotted(), 'x')

  def test_dict_slot_works(self) -> None:
    """An owner whose slots include '__dict__' holds the field as any
    other."""
    owner = WithDict()
    self.assertEqual(owner.x, 1)
    owner.x = 2
    self.assertEqual(owner.x, 2)
