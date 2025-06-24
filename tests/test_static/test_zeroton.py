"""TestZeroton tests the Zeroton metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static.zeroton import Zeroton, THIS, OWNER, DESC
from worktoy.text import monoSpace
from worktoy.waitaminute import IllegalInstantiation, ZerotonCaseException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestZeroton(TestCase):
  """TestZeroton tests the Zeroton metaclass. """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_is_instance(self, ) -> None:
    """Test that the Zeroton metaclass is an instance of itself."""
    self.assertIsInstance(THIS, Zeroton)
    self.assertIsInstance(OWNER, Zeroton)
    self.assertIsInstance(DESC, Zeroton)

  def test_raises(self, ) -> None:
    """Test that the Zeroton metaclass raises the correct exceptions."""
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
    """Test that the Zeroton metaclass has the correct string
    representation."""
    expected = """indicates a placeholder for a class not yet created 
    allowing it to be referenced before creation"""
    self.assertIn(monoSpace(expected), str(THIS))
    self.assertEqual("""<Zeroton: THIS>""", repr(THIS))
    expected = """Zeroton is a placeholder for the descriptor 
    object of the surrounding scope"""
    self.assertIn(monoSpace(expected), str(DESC))
    self.assertEqual("""<Zeroton: DESC>""", repr(DESC))
    expected = """is a placeholder for the class object 
    of the surrounding"""
    self.assertIn(monoSpace(expected), str(OWNER))
    self.assertEqual("""<Zeroton: OWNER>""", repr(OWNER))

  def test_instancecheck(self) -> None:
    """Test that the Zeroton metaclass instance check works correctly."""
    self.assertFalse(isinstance(object(), THIS))
    self.assertIsInstance(THIS, OWNER)

  def test_zeroton_case_exception(self) -> None:
    """Test that ZerotonCaseException is raised correctly."""
    with self.assertRaises(ZerotonCaseException) as context:
      class Sus(metaclass=Zeroton):
        """A class with Zeroton metaclass."""
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'Sus')
    with self.assertRaises(ZerotonCaseException) as context:
      raise ZerotonCaseException(None)
    e = context.exception
    self.assertEqual(str(e), ValueError.__str__(e))

  def test_hash_exception(self) -> None:
    """Test that Zeroton metaclass raises TypeError on hash."""
    with self.assertRaises(TypeError) as context:
      hash(THIS)
    e = context.exception
    expected = """Zeroton classes are not hashable"""
    self.assertIn(expected, str(e))
