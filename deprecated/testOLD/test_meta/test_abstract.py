"""TestAbstract tests that the 'abstract' decorator correctly sets a
method as being abstract and that this is correctly understood by the
metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.abstract import abstract
from worktoy.waitaminute import AbstractInstantiationException
from worktoy.ezdata import EZData


class AbstractColor(EZData):
  """This color class has three attributes, red, green, and blue,
  but leaves an abstract method for subclasses: 'asHex'. """

  red = 0
  green = 0
  blue = 0

  @abstract
  def asHex(self) -> str:
    """This method should be implemented by subclasses. """


class RGBA(AbstractColor):
  """This class does not implement the 'asHex' method, but adds an alpha
  attribute. """

  alpha = 255


class Color(RGBA):
  """This class does not implement the 'asHex' method, but adds an alpha
  attribute. """

  def asHex(self) -> str:
    """This method should be implemented by subclasses. """
    return """%02x%02x%02x%02x""" % (
        self.red, self.green, self.blue, self.alpha)


class LMAO(EZData):
  """This color class has three attributes, red, green, and blue,
  but leaves an abstract method for subclasses: 'asHex'. """


class TestAbstract(TestCase):
  """TestAbstract tests that the 'abstract' decorator correctly sets a
  method as being abstract and that this is correctly understood by the
  metaclass. """

  def test_is_abstract(self) -> None:
    """Test that the 'asHex' method is abstract. """
    self.assertEqual(AbstractColor.isAbstract, True)
    self.assertEqual(RGBA.isAbstract, True)
    self.assertEqual(Color.isAbstract, False)
    self.assertEqual(LMAO.isAbstract, False)

  def test_instantiation(self) -> None:
    """Test that we can instantiate the RGB class. """
    orange = Color(255, 165, 0)
    self.assertEqual(orange.red, 255)
    self.assertEqual(orange.green, 165)
    self.assertEqual(orange.blue, 0)
    self.assertEqual(orange.alpha, 255)
    self.assertEqual(orange.asHex(), "ffa500ff")

  def test_diff_pos(self) -> None:
    """Test that the RGB class can be instantiated with different
    positional arguments. """
    color0 = Color()
    color1 = Color(255)
    color2 = Color(255, 165)
    color3 = Color(255, 165, 0)
    color4 = Color(255, 165, 0, 255)
    self.assertEqual(color0.red, 0)
    self.assertEqual(color0.green, 0)
    self.assertEqual(color0.blue, 0)
    self.assertEqual(color0.alpha, 255)

    self.assertEqual(color1.red, 255)
    self.assertEqual(color1.green, 0)
    self.assertEqual(color1.blue, 0)
    self.assertEqual(color1.alpha, 255)

    self.assertEqual(color2.red, 255)
    self.assertEqual(color2.green, 165)
    self.assertEqual(color2.blue, 0)
    self.assertEqual(color2.alpha, 255)

    self.assertEqual(color3.red, 255)
    self.assertEqual(color3.green, 165)
    self.assertEqual(color3.blue, 0)
    self.assertEqual(color3.alpha, 255)

  def test_error(self) -> None:
    """Test that the 'asHex' method is not implemented in the RGBA class. """
    with self.assertRaises(AbstractInstantiationException) as context:
      AbstractColor(255, 165, 0)
    with self.assertRaises(AbstractInstantiationException) as context:
      RGBA(255, 165, 0)
    with self.assertRaises(AbstractInstantiationException) as context:
      RGBA(255, 165)
    with self.assertRaises(AbstractInstantiationException) as context:
      RGBA(255)
    with self.assertRaises(AbstractInstantiationException) as context:
      RGBA()
