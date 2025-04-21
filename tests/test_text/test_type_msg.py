"""TestTypeMsg tests the typeMsg function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from math import sin, cos, atan2

from types import FunctionType

from worktoy.mcls import BaseObject
from worktoy.parse import maybe
from worktoy.static import overload
from worktoy.text import typeMsg
from worktoy.attr import AttriBox, Field

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from types import MethodType
  from typing import Any, Callable, Self


class Complex(BaseObject):
  """Complex number representation. """

  __fallback_real_part__ = 0.0
  __fallback_imag_part__ = 0.0

  __real_part__ = None
  __imag_part__ = None

  REAL = Field()
  IMAG = Field()
  r = Field()  # polar
  t = Field()  # polar

  @REAL.GET
  def _getReal(self, ) -> float:
    """Get the real part."""
    return maybe(self.__real_part__, self.__fallback_real_part__)

  @IMAG.GET
  def _getImaginary(self, ) -> float:
    """Get the imaginary part."""
    return maybe(self.__imag_part__, self.__fallback_imag_part__)

  @REAL.SET
  def _setReal(self, value: float) -> None:
    """Set the real part."""
    if not isinstance(value, (int, float, complex)):
      raise TypeError(typeMsg('value', value, (int, float, complex)))
    if isinstance(value, complex):
      self.__real_part__ = value.real
    else:
      self.__real_part__ = float(value)

  @IMAG.SET
  def _setImaginary(self, value: float) -> None:
    """Set the imaginary part."""
    if not isinstance(value, (int, float, complex)):
      raise TypeError(typeMsg('value', value, (int, float, complex)))
    if isinstance(value, complex):
      self.__imag_part__ = value.imag
    else:
      self.__imag_part__ = float(value)

  @r.GET
  def _getR(self, ) -> float:
    """Get the polar radius."""
    return abs(self)

  @r.SET
  def _setR(self, value: float) -> None:
    """Set the polar radius."""
    if isinstance(value, int):
      return self._setR(float(value))
    if not isinstance(value, float):
      raise TypeError(typeMsg('value', value, float))
    self.__real_part__ *= value / abs(self)
    self.__imag_part__ *= value / abs(self)

  @t.GET
  def _getT(self, ) -> float:
    """Get the polar angle."""
    return atan2(self.__imag_part__, self.__real_part__)

  @t.SET
  def _setT(self, value: float) -> None:
    """Set the polar angle."""
    if isinstance(value, int):
      return self._setT(float(value))
    if not isinstance(value, float):
      raise TypeError(typeMsg('value', value, float))
    r = abs(self)
    self.__real_part__ = r * cos(value)
    self.__imag_part__ = r * sin(value)

  def __abs__(self, ) -> float:
    return (self.REAL ** 2 + self.IMAG ** 2) ** 0.5

  def __init__(self, *args) -> None:
    """Constructor for Complex."""
    x, y = [*args, None, None][:2]
    if y is not None:
      self.__real_part__ = x
      self.__imag_part__ = y
    elif x is not None:
      self.__real_part__ = x

  def __getattr__(self, key: str) -> Any:
    """Get the attribute."""
    if key in ['__add__', '__sub__', '__mul__', '__truediv__']:
      func = getattr(float, key)
      cls = type(self)

      def out(self_, other: Any) -> Any:
        if isinstance(other, type(self_)):
          return cls(
              func(self.__real_part__, other),
              func(self.__imag_part__, other)
          )
        return NotImplemented

      return out
    try:
      return object.__getattribute__(self, key)
    except AttributeError as attributeError:
      raise AttributeError


class TestTypeMsg(TestCase):
  """TestTypeMsg tests the typeMsg function."""

  def setUp(self, ) -> None:
    """Sets up the test case."""
    self.z1 = Complex(69, 420)
    self.z2 = Complex(0.1337, 0.80085)

  def test_single_type(self, ) -> None:
    """Test that typeMsg correctly creates a type message for a single
    type."""
    with self.assertRaises(TypeError) as context:
      self.z1.r = 'trololololo....'
    self.assertEqual(
        str(context.exception),
        typeMsg('value', 'trololololo....', float)
    )

    with self.assertRaises(TypeError) as context:
      self.z2.t = 'half a pie'
    self.assertEqual(
        str(context.exception),
        typeMsg('value', 'half a pie', float)
    )

  def test_multiple_types(self, ) -> None:
    """Tests that typeMsg correctly creates an error message appropriate
    for multiple types."""
    troll = '69.420'
    with self.assertRaises(TypeError) as context:
      self.z1.REAL = troll
    self.assertEqual(
        str(context.exception),
        typeMsg('value', troll, (int, float, complex))
    )
    troll = ['69', 420]
    with self.assertRaises(TypeError) as context:
      self.z1.IMAG = troll
    self.assertEqual(
        str(context.exception),
        typeMsg('value', troll, (int, float, complex))
    )

  def test_attribox_error(self, ) -> None:
    """Tests that typeMsg correctly creates an error message for
    AttriBox."""
    troll = '69.420'
    testSubject = AttriBox[float]()
    setattr(testSubject, '__pos_args__', troll)
    with self.assertRaises(TypeError) as context:
      testSubject._getPosArgs()
    self.assertEqual(
        str(context.exception),
        typeMsg('__pos_args__', troll, tuple)
    )

  def test_field_error(self, ) -> None:
    """Tests that typeMsg correctly creates an error message for
    Field."""
    troll = 69.420  # A string is expected
    Troll = type('Troll', (), {'__name__': troll})
    testSubject = Field()
    with self.assertRaises(TypeError) as context:
      testSubject.GET(Troll())
    self.assertEqual(
        str(context.exception),
        typeMsg('getterKey', troll, str)
    )

    with self.assertRaises(TypeError) as context:
      testSubject.SET(Troll())
    self.assertEqual(
        str(context.exception),
        typeMsg('setterKey', troll, str)
    )
