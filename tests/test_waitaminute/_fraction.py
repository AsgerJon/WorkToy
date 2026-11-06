"""
Fraction is the class of the 'SubclassException' docstring: a builder's
class raising the exception where a value of the wrong class arrives.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import SubclassException


class Fraction:
  """
  Nothing in worktoy raises 'SubclassException'; it is offered to the
  builder, whose own classes raise it where a value arrives whose class
  is no subclass of the one expected. 'Fraction' is the class of the
  exception's docstring: it takes a numerator and a denominator and
  raises the exception for either that is no 'int', naming the class
  received and 'int'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __slots__ = ('numerator', 'denominator')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, numerator: int, denominator: int) -> None:
    if not isinstance(numerator, int):
      raise SubclassException(type(numerator), int)
    if not isinstance(denominator, int):
      raise SubclassException(type(denominator), int)
    self.numerator = numerator
    self.denominator = denominator
