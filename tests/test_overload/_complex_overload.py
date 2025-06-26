"""
ComplexOverload provides an implementation of complex numbers that makes
use of the overload functionality provided by the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import stringList
from worktoy.static import overload
from worktoy.static.zeroton import THIS
from worktoy.attr import AttriBox
from worktoy.mcls import BaseMeta
from tests import ComplexBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self

import sys
import gc


class ComplexOverload(ComplexBase, metaclass=BaseMeta):
  """Complex number representation. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables

  RE = AttriBox[float](0.0)
  IM = AttriBox[float](0.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, x: float, y: float, **kwargs) -> None:
    """Initialize the complex number."""
    self.RE = x
    self.IM = y
    if kwargs:
      self.__init__(**kwargs)

  @overload(complex)
  def __init__(self, z: complex, **kwargs) -> None:
    """Initialize the complex number."""
    self.__init__(z.real, z.imag)
    if kwargs:
      self.__init__(**kwargs)

  @overload(THIS)
  def __init__(self, z: Self, **kwargs) -> None:
    """Initialize the complex number."""
    self.__init__(z.RE, z.IM)
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize the complex number."""
    if TYPE_CHECKING:  # pragma: no cover
      assert callable(self.__init__)
    self.__init__(0.0, 0.0)
    realKeys = stringList("""real, re, x""")
    imagKeys = stringList("""imag, im, y""")
    realKwarg, kwargs = self.parseKwargs(*realKeys, float, int, **kwargs)
    if realKwarg is None:
      return
    imagKwarg, kwargs = self.parseKwargs(*imagKeys, float, int, **kwargs)
    if imagKwarg is None:
      return
    self.__init__(realKwarg, imagKwarg)
