"""
TestAccessErrorUnplaced subclasses 'WaitAMinuteTest' and pins that
'AccessError' renders for a descriptor no class has named, as its
siblings 'ReadOnlyError' and 'ProtectedError' do, falling back to
'object' where the owner or the field name is missing. It used to read
'__name__' off a missing owner and fail inside '__str__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import AccessError

from . import WaitAMinuteTest


class TestAccessErrorUnplaced(WaitAMinuteTest):
  """
  TestAccessErrorUnplaced provides tests for rendering 'AccessError'.
  """

  def test_unplaced_renders(self) -> None:
    """A field no class holds renders with 'object' for both names."""
    text = str(AccessError(Field()))
    self.assertIn("'Field'", text)
    self.assertIn("'object.object'", text)
    self.assertEqual(text, repr(AccessError(Field())))

  def test_placed_renders_names(self) -> None:
    """A placed field renders its owner and name as before."""

    class Owner(BaseObject):
      x = Field()

    with self.assertRaises(AccessError) as context:
      _ = Owner().x
    self.assertIn("'Owner.x'", str(context.exception))
