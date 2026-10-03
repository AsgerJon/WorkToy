"""
TestMatchArgsClassBody subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that an 'EZData' class body setting '__match_args__'
keeps its own tuple, that a subclass whose body sets none uses the one
its parent set, and that a class with none along its bases receives the
generated one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class TestMatchArgsClassBody(EZTest):
  """
  TestMatchArgsClassBody provides tests for a '__match_args__' set in the
  class body of an 'EZData' class, which is kept as written, as
  'dataclasses' keeps one, and generated only where neither the class
  body nor a base sets one.
  """

  def test_subset_kept(self) -> None:
    """
    Testing that a class-body tuple naming some of the fields is kept.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)
      __match_args__ = ('y',)

    self.assertEqual(Point.__match_args__, ('y',))

  def test_order_kept(self) -> None:
    """
    Testing that a class-body tuple naming the fields in another order is
    kept in that order.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)
      __match_args__ = ('y', 'x')

    self.assertEqual(Point.__match_args__, ('y', 'x'))

  def test_empty_kept(self) -> None:
    """
    Testing that an empty class-body tuple is kept on a class that is not
    keyword-only.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      __match_args__ = ()

    self.assertEqual(Point.__match_args__, ())

  def test_keyword_only_kept(self) -> None:
    """
    Testing that a keyword-only class keeps a class-body tuple rather than
    the empty tuple it would receive.
    """

    class Circle(EZData, kwOnly=True):
      radius = EZField[float](1.0)
      __match_args__ = ('radius',)

    self.assertEqual(Circle.__match_args__, ('radius',))

  def test_generated_without_class_body(self) -> None:
    """
    Testing that a class body setting no '__match_args__' receives the
    field names in declaration order.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    self.assertEqual(Point.__match_args__, ('x', 'y'))

  def test_subclass_inherits(self) -> None:
    """
    Testing that a subclass whose body sets no '__match_args__' uses the
    tuple its parent set, as every optional name defers to a base.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)
      __match_args__ = ('y',)

    class Point3D(Point):
      z = EZField[float](0.0)

    self.assertEqual(Point3D.__match_args__, ('y',))
