"""
UncheckableMeta builds classes that refuse 'isinstance'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Never


class UncheckableMeta(type):
  """
  A 'typing.Protocol' that is not runtime checkable raises 'TypeError'
  from 'isinstance', and a signature naming such a class could never
  match a call. 'UncheckableMeta' refuses every instance check the same
  way, on every Python the library supports.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instancecheck__(cls, instance: Any) -> Never:
    raise TypeError('%s cannot be used with isinstance()' % cls.__name__)
