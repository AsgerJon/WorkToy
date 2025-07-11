"""TestSentinel tests the Sentinel metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import StaticTest
from typing import TYPE_CHECKING

from worktoy.core.sentinels import Sentinel, THIS, OWNER, DESC
from worktoy.utilities import textFmt
from worktoy.waitaminute.meta import IllegalInstantiation

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSentinel(StaticTest):
  """TestSentinel tests the Sentinel metaclass. """

  def test_is_instance(self, ) -> None:
    """Test that the Sentinel metaclass is an instance of itself."""
    self.assertIsInstance(THIS, Sentinel)
    self.assertIsInstance(OWNER, Sentinel)
    self.assertIsInstance(DESC, Sentinel)

  def test_raises(self, ) -> None:
    """Test that the Sentinel metaclass raises the correct exceptions."""
    with self.assertRaises(IllegalInstantiation) as context:
      _ = THIS()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, THIS)

    with self.assertRaises(IllegalInstantiation) as context:
      _ = OWNER()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, OWNER)

    with self.assertRaises(IllegalInstantiation) as context:
      _ = DESC()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, DESC)

  def test_repr_str(self) -> None:
    """Test that the Sentinel metaclass has the correct string
    representation."""
    self.assertEqual("""<Sentinel: THIS>""", repr(THIS))
    self.assertEqual("""<Sentinel: DESC>""", repr(DESC))
    self.assertEqual("""<Sentinel: OWNER>""", repr(OWNER))

  def test_instancecheck(self) -> None:
    """Test that the Sentinel metaclass instance check works correctly."""
    self.assertFalse(isinstance(object(), THIS))
    self.assertIsInstance(THIS, OWNER)

  def test_hash_exception(self) -> None:
    """Test that Sentinel metaclass raises TypeError on hash."""
    with self.assertRaises(TypeError) as context:
      hash(THIS)
    e = context.exception
    expected = """Sentinel classes are not hashable"""
    self.assertIn(expected, str(e))
