"""
ComplexMetaSub provides a subclass of ComplexMeta allowing testing of the
preservation of the 'overload' decorator in subclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.utilities import maybe
from . import ComplexMeta

if TYPE_CHECKING:  # pragma: no cover
  pass


class SusComplex:  # sus
  """SusComplex allows ComplexMetaSub to have one overload to itself. """

  __inner_value__ = None

  def __complex__(self) -> complex:
    return maybe(self.__inner_value__, complex(0, 0))

  def __init__(self, *args) -> None:
    if len(args) > 1:
      x, y, *_ = args
      self.__inner_value__ = complex(x, y)
    else:
      self.__inner_value__ = complex(*args)


class ComplexMetaSub(ComplexMeta):
  """
  ComplexMetaSub provides a subclass of ComplexMeta allowing testing of the
  preservation of the 'overload' decorator in subclasses.
  """

  @overload(SusComplex)
  def __init__(self, sus: SusComplex) -> None:
    """
    Initialize with a SusComplex instance.
    """
    self.RE = sus.__inner_value__.real
    self.IM = sus.__inner_value__.imag
