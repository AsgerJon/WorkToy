"""The 'validateExistingDirectory' function validates that a given 'str'
object points to an existing directory. """
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import PathSyntaxException

if TYPE_CHECKING:  # pragma: no cover
  pass


def validateExistingDirectory(directory: str, **kwargs) -> str:
  """Validate that 'directory' is an absolute path to an existing
  directory.

  Parameters
  ----------
  directory : str
      Absolute path to the directory to validate.
  **kwargs
      Pass 'strict=False' to return '' instead of raising when the
      directory is missing or is not a directory.

  Returns
  -------
  str
      The normalized path, or '' when a failure is suppressed by
      'strict=False'.

  Raises
  ------
  PathSyntaxException
      If 'directory' is not an absolute path. Raised regardless of
      'strict'.
  FileNotFoundError
      If the directory does not exist and 'strict' is True (the
      default).
  NotADirectoryError
      If the path exists but is not a directory and 'strict' is True.
  """
  if not os.path.isabs(directory):
    raise PathSyntaxException(directory)
  if not os.path.exists(directory):
    if not kwargs.get('strict', True):
      return ''
    infoSpec = """No directory exists at: '%s'!"""
    info = textFmt(infoSpec % directory)
    raise FileNotFoundError(info)
  if not os.path.isdir(directory):
    if not kwargs.get('strict', True):
      return ''
    infoSpec = """The path '%s' is not a directory!"""
    info = textFmt(infoSpec % directory)
    raise NotADirectoryError(info)
  return os.path.normpath(directory)
