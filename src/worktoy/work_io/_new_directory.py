"""The 'newDirectory' function creates a new directory at the specified
path. """
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from . import validateAvailablePath

if TYPE_CHECKING:  # pragma: no cover
  from typing import Union, TypeAlias, LiteralString

  Path: TypeAlias = Union[str, bytes, LiteralString]


def newDirectory(path: Path) -> str:
  """Create a new directory at 'path'.

  Parameters
  ----------
  path : str
    Absolute path at which to create the directory.

  Returns
  -------
  str
    The normalized path of the created directory.

  Raises
  ------
  PathSyntaxException
    If 'path' is not absolute.
  FileExistsError
    If 'path' already exists.
  NotADirectoryError
    If an intermediate component of 'path' exists as a file rather
    than a directory ('os.makedirs').
  """
  validateAvailablePath(path)
  os.makedirs(path, exist_ok=True)
  return os.path.normpath(path)
