"""
Directory is a read-only descriptor exposing the owner's source directory.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
from typing import TYPE_CHECKING

from . import NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never, Optional


class Directory(NoPickle):
  """Read-only descriptor returning the owner's source directory.

  On instance access, resolves the module of the instance's class
  via 'sys.modules' and returns the absolute directory of that
  module's '__file__'. Useful for classes that need to locate
  resources beside their own source file. A class defined where no
  file stands behind its module, as in the REPL or under 'exec', has
  no source directory, and reading the attribute raises
  'MissingVariable' naming it.
  """

  #  Private Variables
  __field_name__: Optional[str] = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Records the name of the attribute, which the refusals report."""
    self.__field_name__ = name

  def __get__(self, instance: Any, owner: type) -> Any:
    """Return the absolute directory of the instance's module."""
    if instance is None:
      return self
    module = sys.modules.get(instance.__class__.__module__)
    try:
      filePath = getattr(module, '__file__')
    except AttributeError as attributeError:
      from worktoy.waitaminute import MissingVariable
      name = self.__field_name__ or 'directory'
      raise MissingVariable(instance, name, str) from attributeError
    return os.path.abspath(os.path.dirname(filePath))

  def __set__(self, instance: Any, value: Any) -> Never:
    from worktoy.waitaminute.desc import ReadOnlyError
    raise ReadOnlyError(instance, self, value, )

  def __delete__(self, instance: Any) -> Never:
    from worktoy.waitaminute.desc import ProtectedError
    raise ProtectedError(instance, self, )
