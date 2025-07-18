"""
ComplexSubclass provides a subclass of ComplexNumber for testing that
inheritance works as expected with the overload system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import WYD
from worktoy.core.sentinels import FALLBACK, WILDCARD
from ._complex_number import ComplexNumber

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Optional, TypeAlias, Self


class ComplexSubclass(ComplexNumber):
  """
  ComplexSubclass provides a subclass of ComplexNumber for testing that
  inheritance works as expected with the overload system.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __test_notes__ = None

  #  Public Variables

  #  Virtual Variables

  #  Overloaded Functions
  __init__ = ComplexNumber.__init__.clone()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @__init__.overload(str)  # addition to overloads
  def __init__(self, z: str) -> None:
    zStr = complex(z.replace(' ', '').lower().replace('i', 'j'))
    ComplexNumber.__init__(self, zStr)

  @__init__.overload(complex, WILDCARD, WILDCARD)
  def __init__(self, z: complex, *args) -> None:
    """
    Constructor for ComplexSubclass that accepts a complex number.
    """
    self.RE = z.real
    self.IM = z.imag
    self.__test_notes__ = args

  @__init__.overload(FALLBACK)
  def __init__(self, *args) -> None:
    """
    Fallback constructor for ComplexSubclass.
    """
    raise WYD('imagine falling back')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
