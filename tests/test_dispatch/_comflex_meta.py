"""
ComflexMeta provides a poorly named complex number implementation
featuring the 'flex' decorator allowing flexible overloading. In contrast
to 'ComFlex', this implementation uses the metaclass to expose the
'Dispatcher' overloading functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ComplexMeta
from worktoy.dispatch import overload

if TYPE_CHECKING:  # pragma: no cover
  pass


class ComflexMeta(ComplexMeta):
  """
  ComplexMeta provides a complex number implementation derived from the
  'BaseMeta' metaclass allowing it to test the 'overload' decorator. Please
  note, that use of the 'overload' decorator is reserved for classes
  derived from 'BaseMeta' or a subclass of 'BaseMeta'. This provides a
  syntactically cleaner overloading implementation, but requires
  customization of the metaclass, in particular customization of the
  namespace object.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload.flex(complex, float)
  def __init__(self, *args) -> None:
    z, x = None, None
    for arg in args:
      if isinstance(arg, complex):
        z = arg
      elif isinstance(arg, float):
        x = arg
    self.RE = x + z.real
    self.IM = z.imag
