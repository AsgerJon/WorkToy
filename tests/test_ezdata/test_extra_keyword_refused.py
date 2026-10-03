"""
TestExtraKeywordRefused tests that an 'EZData' class refuses a keyword
argument that names none of its fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ExtraKeywordException
from . import EZTest
from .examples import Point2D, Circle


class TestExtraKeywordRefused(EZTest):
  """
  TestExtraKeywordRefused tests the keyword arguments of the generated
  '__init__'. A keyword naming a field sets that field, own or inherited,
  and a keyword naming none of the fields raises 'ExtraKeywordException'
  before '__post_init__' runs, on keyword-only classes as on the others.
  """

  def test_misspelled_field(self) -> None:
    """
    Testing that a misspelled field name is refused with
    'ExtraKeywordException' naming the class, the keyword and the fields.
    """
    with self.assertRaises(ExtraKeywordException) as context:
      Point2D(z=1.0)
    exception = context.exception
    self.assertIs(exception.cls, Point2D)
    self.assertEqual(exception.keyword, 'z')
    self.assertEqual(exception.fieldNames, ('x', 'y'))
    self.assertIn("'z'", str(exception))
    self.assertIn("'x', 'y'", str(exception))

  def test_is_type_error(self) -> None:
    """
    Testing that 'ExtraKeywordException' is a 'TypeError', as Python's own
    refusal of an unexpected keyword argument is.
    """
    with self.assertRaises(TypeError):
      Point2D(1.0, 2.0, z=3.0)

  def test_keyword_only_class(self) -> None:
    """
    Testing that a keyword-only class refuses a keyword naming none of its
    fields.
    """
    with self.assertRaises(ExtraKeywordException) as context:
      Circle(radius=2.0, radious=3.0)
    self.assertEqual(context.exception.keyword, 'radious')

  def test_field_keywords_accepted(self) -> None:
    """
    Testing that keywords naming fields are accepted and set them.
    """
    point = Point2D(y=2.0, x=1.0)
    self.assertEqual(point.x, 1.0)
    self.assertEqual(point.y, 2.0)

  def test_inherited_field_keyword(self) -> None:
    """
    Testing that a keyword naming an inherited field is accepted.
    """

    class Point3D(Point2D):
      z = EZField[float](0.0)

    point = Point3D(x=1.0, z=3.0)
    self.assertEqual(point.asTuple(), (1.0, 0.0, 3.0))

  def test_refused_before_post_init(self) -> None:
    """
    Testing that the refusal comes before '__post_init__' runs.
    """
    ran = []

    class Logged(EZData):
      x = EZField[int](0)
      __post_init__ = lambda self: ran.append('post')

    with self.assertRaises(ExtraKeywordException):
      Logged(y=1)
    self.assertEqual(ran, [])
