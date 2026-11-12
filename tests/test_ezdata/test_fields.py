"""
TestFields tests the 'fields' function from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import fields, EZField
from worktoy.mcls import BaseObject
from . import EzdataTest, Point2D, Vector3, Circle


class TestFields(EzdataTest):
  """
  'fields' gives the field descriptors of a dataclass, from the class
  or from an instance, in declaration order with the inherited ones
  first, and refuses anything else with 'TypeError'. The tests pin the
  three.
  """

  def test_from_class_and_instance(self) -> None:
    self.assertEqual(fields(Point2D), Point2D.fields)
    self.assertEqual(fields(Point2D(1.0, 2.0)), Point2D.fields)
    names = [field.fieldName for field in fields(Point2D)]
    self.assertEqual(names, ['x', 'y'])
    for field in fields(Circle(radius=2.0)):
      with self.subTest(field=field.fieldName):
        self.assertIsInstance(field, EZField)
        self.assertIs(field.fieldOwner, Circle)

  def test_inherited_first(self) -> None:
    names = [field.fieldName for field in fields(Vector3)]
    self.assertEqual(names, ['x', 'y', 'z'])

  def test_refuses_other_objects(self) -> None:
    class Plain(BaseObject):
      pass

    for other in (Plain, Plain(), 5, 'text', EZField[int](1)):
      with self.subTest(other=str(other)):
        with self.assertRaises(TypeError) as context:
          fields(other)
        self.assertIn("'fields()' expects an 'EZData' class or instance, "
                      "but received", str(context.exception))
        self.assertIn("of type '%s'." % type(other).__name__,
                      str(context.exception))

  def test_refusal_shows_the_value_by_its_repr(self) -> None:
    with self.assertRaises(TypeError) as context:
      fields(5)
    self.assertIn("but received: 5 of type 'int'.", str(context.exception))
    with self.assertRaises(TypeError) as context:
      fields('5')
    self.assertIn("but received: '5' of type 'str'.",
                  str(context.exception))
    with self.assertRaises(TypeError) as context:
      fields('x' * 60)
    self.assertIn("but received: '%s... of type 'str'." % ('x' * 46),
                  str(context.exception))
