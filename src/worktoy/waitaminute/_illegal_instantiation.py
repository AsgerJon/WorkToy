"""IllegalInstantiation is a custom exception raised to indicate than
an attempt was made to instantiate a class under illegal conditions."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Never


class IllegalInstantiation(TypeError):
  """IllegalInstantiation is a custom exception raised to indicate than
  an attempt was made to instantiate a class under illegal conditions."""

  cls = _Attribute()

  def __init__(self, cls_: type) -> None:
    """Initialize the IllegalInstantiation with the class."""
    self.cls = cls_
    infoSpec = """Illegal instantiation of class '%s'"""
    info = infoSpec % cls_.__name__
    TypeError.__init__(self, info)
