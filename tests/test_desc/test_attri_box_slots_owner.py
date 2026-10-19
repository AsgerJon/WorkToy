"""
TestAttriBoxSlotsOwner subclasses 'DescTest' and pins that an 'AttriBox'
on an owner whose instances have no '__dict__', a class declaring
'__slots__' without one, refuses every access with 'MissingInstanceDict'
naming the owner and the field. The store used to fail with the bare
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


class Slotted:
  """Slotted declares slots and no instance dict."""

  __slots__ = ('a',)

  x = AttriBox[int](1)


class WithDict:
  """WithDict declares slots including an instance dict."""

  __slots__ = ('a', '__dict__')

  x = AttriBox[int](1)


class TestAttriBoxSlotsOwner(DescTest):
  """
  TestAttriBoxSlotsOwner provides tests for a box on a slots-only owner.
  """

  def test_read_refused(self) -> None:
    """A read raises, naming the owner and the field."""
    with self.assertRaises(MissingInstanceDict) as context:
      _ = Slotted().x
    e = context.exception
    self.assertEqual(e.ownerName, 'Slotted')
    self.assertEqual(e.fieldName, 'x')
    self.assertIn("'Slotted.x'", str(e))
    self.assertIn('__dict__', str(e))
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, TypeError)

  def test_write_and_delete_refused(self) -> None:
    """A write and a delete raise the same."""
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict):
      slotted.x = 2
    with self.assertRaises(MissingInstanceDict):
      del slotted.x

  def test_not_mistaken_for_absence(self) -> None:
    """'hasattr' no longer answers 'False'; the refusal propagates."""
    with self.assertRaises(MissingInstanceDict):
      hasattr(Slotted(), 'x')

  def test_dict_slot_works(self) -> None:
    """An owner whose slots include '__dict__' holds the field as any
    other."""
    owner = WithDict()
    self.assertEqual(owner.x, 1)
    owner.x = 2
    self.assertEqual(owner.x, 2)
