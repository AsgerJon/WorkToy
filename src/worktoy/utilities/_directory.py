"""Descriptor exposing the directory of the owner's source file.

'Directory' is a read-only descriptor. When accessed through an
instance, it returns the absolute path of the directory holding
the module file in which the owner class is defined. When
accessed through the class itself, it returns the descriptor."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never


class Directory:
  """Read-only descriptor returning the owner's source directory.

  On instance access, resolves the module of the instance's class
  via 'sys.modules' and returns the absolute directory of that
  module's '__file__'. Useful for classes that need to locate
  resources beside their own source file.
  """

  def __get__(self, instance: Any, owner: type) -> Any:
    """Return the absolute directory of the instance's module."""
    if instance is None:
      return self
    module = sys.modules.get(instance.__class__.__module__)
    filePath = getattr(module, '__file__')
    return os.path.abspath(os.path.dirname(filePath))

  def __set__(self, instance: Any, value: Any) -> Never:
    from worktoy.waitaminute.desc import ReadOnlyError
    raise ReadOnlyError(instance, self, value, )

  def __delete__(self, instance: Any) -> Never:
    from worktoy.waitaminute.desc import ProtectedError
    raise ProtectedError(self, instance, )
