"""
Refusing is an iterable by declaration that refuses to iterate.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Never


class Refusing:
  """
  Every worktoy class passes 'isinstance(cls, Iterable)', since its
  metaclass defines '__iter__', and still raises 'TypeError' when
  iterated without a '__class_iter__' hook. 'unpack' must keep such an
  object whole. 'Refusing' is a plain class with the same two faces: it
  defines '__iter__' and raises 'TypeError' from it.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self) -> Never:
    raise TypeError('%s refuses to iterate' % type(self).__name__)
