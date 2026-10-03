"""
TestKeeWrongRootMessage subclasses 'KeeTest' and pins the message for an
enumeration of a custom 'KeeMeta' based on the wrong root. Such a class,
'class Font(KeeNum, metaclass=FontMeta)', was told it must have exactly
one base but received none, though it has one; the message now says the
base must be the root of the metaclass or an enumeration based on it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeMeta, KeeNum, Kee

from . import KeeTest


class FontMeta(KeeMeta):
  """FontMeta is a custom 'KeeMeta'."""


class TestKeeWrongRootMessage(KeeTest):
  """
  TestKeeWrongRootMessage provides tests for the message of an
  enumeration based on the wrong root.
  """

  def test_message_names_root(self) -> None:
    """The message names the metaclass, its root and the base given."""
    with self.assertRaises(ValueError) as context:
      class Font(KeeNum, metaclass=FontMeta):
        A = Kee[int](1)
    info = str(context.exception)
    self.assertIn('FontMeta', info)
    self.assertIn('FontMeta.keeNum', info)
    self.assertIn('KeeNum', info)
    self.assertNotIn('received none', info)
