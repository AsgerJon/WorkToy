"""
TestBox tests the forwarding of '__set_name__' to field objects created by
instances 'AttriBox'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException
from . import DescTest, BoxOwner, BoxedFloat, BoxedObject


class TestBox(DescTest):
  """
  TestBox tests the forwarding of '__set_name__' to field objects created by
  instances 'AttriBox'.
  """

  def testBoxedFloat(self, ) -> None:
    """
    Tests the BoxedFloat class itself.
    """
    boxedFloat = BoxedFloat(420.)
    defaultFloat = BoxedFloat()
    with self.assertRaises(RecursionError):
      _ = defaultFloat._getValue(_recursion=True)
    self.assertIsInstance(boxedFloat, BoxedFloat)
    self.assertIsInstance(defaultFloat, BoxedFloat)
    self.assertEqual(boxedFloat.value, 420.)
    self.assertEqual(defaultFloat.value, 0.0)
    self.assertEqual(str(boxedFloat), '%f' % 420.)
    self.assertIn('BoxedFloat', repr(boxedFloat))
    self.assertFalse(complex(boxedFloat).imag)
    self.assertEqual(complex(boxedFloat).real, 420.)
    self.assertEqual(int(boxedFloat), 420)
    self.assertEqual(float(boxedFloat), 420.)

    setattr(defaultFloat, '__private_value__', '1337.')
    with self.assertRaises(TypeException):
      _ = defaultFloat.value

    boxOwner = BoxOwner()
    self.assertEqual(boxOwner.value.name, 'value')
    self.assertIs(boxOwner.value.owner, BoxOwner)
    self.assertEqual(boxOwner.value.value, 69.0)

  def testInit(self, ) -> None:
    """
    Tests that classes used here correctly initialize.
    """
    boxOwner = BoxOwner()
    boxObject = BoxedObject()
    boxFloat = BoxedFloat(420.)
    self.assertIsInstance(boxOwner, BoxOwner)
    self.assertIsInstance(boxObject, BoxedObject)
    self.assertIsInstance(boxFloat, BoxedFloat)

  def testDescriptor(self, ) -> None:
    """
    Tests that the AttriBox descriptors correctly retrieve expected objects.
    """
    boxOwner = BoxOwner()
    self.assertIsInstance(boxOwner.name, BoxedObject)
    self.assertIsInstance(boxOwner.value, BoxedFloat)
    self.assertEqual(boxOwner.value.value, 69.0)

  def testSetName(self) -> None:
    """
    Tests that the field objects created by the AttriBox descriptors
    correctly received the forwarded '__set_name__' information.
    """
    boxOwner = BoxOwner()
    self.assertEqual(boxOwner.name.__field_name__, 'name')
    self.assertIs(boxOwner.name.__field_owner__, BoxOwner)
    self.assertEqual(boxOwner.value.__field_name__, 'value')
    self.assertIs(boxOwner.value.__field_owner__, BoxOwner)
    self.assertIs(boxOwner.name.__field_box__, BoxOwner.name)
