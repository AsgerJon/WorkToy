"""
TestInstanceKeyArgs subclasses 'EZTest' and pins that 'getKeyArgs' on an
'EZData' instance gives no class keywords. 'EZHook' stored the class
keywords on the class at '__key_args__', the name under which 'Object'
keeps the keyword arguments of its constructor, so an instance, which
the generated '__init__' builds without 'Object.__init__', read the
class keywords from there. The class keywords stay readable at
'__keyword_arguments__', as on every worktoy class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class Point(EZData, frozen=True):
  """Point is frozen by class keyword."""

  x = EZField[int](0)


class TestInstanceKeyArgs(EZTest):
  """
  TestInstanceKeyArgs provides tests for 'getKeyArgs' on an EZData
  instance.
  """

  def test_no_class_keywords(self) -> None:
    """An instance gives no constructor keywords."""
    self.assertEqual(Point(1).getKeyArgs(), {})
    self.assertEqual(Point(1).getPosArgs(), ())

  def test_class_keywords_kept(self) -> None:
    """The class keywords stay with the class, and the option holds."""
    self.assertEqual(Point.__keyword_arguments__, {'frozen': True})
    self.assertTrue(Point.isFrozen)
