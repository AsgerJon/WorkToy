"""
PermuterMethod is a 'Permuter' that forwards the calling instance ahead
of the reordered positional arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Permuter

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class PermuterMethod(Permuter):
  """
  PermuterMethod subclasses 'Permuter' from 'worktoy.dispatch' and provides
  a wrapper that extracts the calling 'instance' object and passes only
  remaining positional arguments through the arrangement.
  """

  def invoke(self, func, instance=None, *args, **kwargs) -> Any:
    """
    This implementation accepts an instance parameter allowing handling of
    bound methods.
    """
    return func(instance, *self.arrangement.restoreFrom(*args), **kwargs)
