"""WorkToy - WorkToyClass - WorkToyClass
This class provides utility as static methods.
Classes in the package subclass this class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from icecream import ic

from worktoy.worktoyclass import CodecClass

ic.configureOutput(includeContext=True)


class WorkToyClass(CodecClass):
  """WorkToy - DefaultClass
  This class provides utility as static methods.
  Classes in the package subclass this class.
  """

  __attribute_instances__ = []

  def __init_subclass__(cls, **kwargs) -> None:
    existing = getattr(WorkToyClass, '__attribute_instances__')
    setattr(cls, '__attribute_instances__', existing)
    # from worktoy.descriptors import Attribute
    for field in existing:
      field.__class__.__set_name__(field, cls, field._getFieldName())
    return super().__init_subclass__()

  def __init__(self, *args, **kwargs) -> None:
    CodecClass.__init__(self, *args, **kwargs)
