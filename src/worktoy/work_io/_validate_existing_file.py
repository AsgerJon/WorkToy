"""The 'validateExistingFile' function validates the existence of a file. """
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import PathSyntaxException

if TYPE_CHECKING:  # pragma: no cover
  pass


def validateExistingFile(file: str, **kwargs) -> str:
  """Validate that 'file' is an absolute path to an existing file.

  Parameters
  ----------
  file : str
      Absolute path to the file to validate.
  **kwargs
      Pass 'strict=False' to return '' instead of raising when the
      file is missing or is not a regular file.

  Returns
  -------
  str
      The normalized path, or '' when a failure is suppressed by
      'strict=False'.

  Raises
  ------
  PathSyntaxException
      If 'file' is not an absolute path. Raised regardless of
      'strict'.
  FileNotFoundError
      If the file does not exist and 'strict' is True (the default).
  IsADirectoryError
      If the path exists but is not a regular file and 'strict' is
      True.
  """
  if not os.path.isabs(file):
    raise PathSyntaxException(file)
  if not os.path.exists(file):
    if not kwargs.get('strict', True):
      return ''
    infoSpec = """No file exists at: '%s'!"""
    info = textFmt(infoSpec % file)
    raise FileNotFoundError(info)
  if not os.path.isfile(file):
    if not kwargs.get('strict', True):
      return ''
    infoSpec = """The path '%s' is not a file!"""
    info = textFmt(infoSpec % file)
    raise IsADirectoryError(info)
  return str(os.path.normpath(file))
