"""Any is a class whose instance check always returns True"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import typing


class Any:
  """Any is a class whose instance check always returns True"""

  @classmethod
  def __instancecheck__(cls, instance: object) -> bool:
    return True


Any = typing.cast(typing.Any, Any)
