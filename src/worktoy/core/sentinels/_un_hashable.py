"""
UN_HASHABLE is a sentinel placed where a hashable value might be
expected, but where such a value is not possible. Certain base classes
may be implemented with or without hashable values. In case of the
unhashable situation, that class may still be entirely reasonable. This
sentinel can then be used to indicate that a particular subclass is
unhashable without raising at creation time.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Sentinel, _Sentinel

if TYPE_CHECKING:  # pragma: no cover
  from typing import Never, Any


class _UN_HASHABLE_META(_Sentinel):  # noqa N801
  """
  Custom metaclass defining '__getitem__' with specific error and message.
  """

  def __getitem__(cls, key: Any) -> Never:
    raise TypeError("""A 'dict' lookup attempted on UN_HASHABLE object!""")


class UN_HASHABLE(Sentinel, metaclass=_UN_HASHABLE_META):
  """
  UN_HASHABLE is a sentinel placed where a hashable value might be
  expected, but where such a value is not possible. Certain base classes
  may be implemented with or without hashable values. In case of the
  unhashable situation, that class may still be entirely reasonable. This
  sentinel can then be used to indicate that a particular subclass is
  unhashable without raising at creation time.
  """
