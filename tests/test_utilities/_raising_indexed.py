"""
RaisingIndexed is a class whose '__index__' raises when called.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Never


class RaisingIndexed:
  """
  'ValidSlice' checks that '__index__' can be called, not what it does
  when called. 'RaisingIndexed' passes the check and raises
  'RuntimeError' when anything calls its '__index__'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __index__(self) -> Never:
    raise RuntimeError('__index__ was called')
