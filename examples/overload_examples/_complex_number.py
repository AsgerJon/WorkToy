"""ComplexNumber example. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject
from worktoy.static import overload, THIS
from worktoy.attr import AttriBox


class ComplexNumber(BaseObject):
  """ComplexNumber is a class that represents a complex number."""

  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)

  @overload(int, int)
  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.RE = float(x)
    self.IM = float(y)

  @overload(complex)
  def __init__(self, z: complex) -> None:
    self.RE = z.real
    self.IM = z.imag

  @overload(THIS)
  def __init__(self, other: ComplexNumber) -> None:
    self.RE = other.RE
    self.IM = other.IM

  @overload()
  def __init__(self) -> None:
    self.RE = 0.0
    self.IM = 0.0

  def __str__(self, ) -> str:
    """String representation"""
    infoSpec = """%.3f+%.3fI"""
    return infoSpec % (self.RE, self.IM)


def main02() -> int:
  """Main function to test the ComplexNumber class."""
  print(type(ComplexNumber.__str__).__name__)
  print(type(ComplexNumber.__init__).__name__)
  return 0


def main() -> int:
  """Main function to test the ComplexNumber class."""
  num0 = ComplexNumber()
  print(num0.RE)
  print(ComplexNumber.RE)
  return 0
