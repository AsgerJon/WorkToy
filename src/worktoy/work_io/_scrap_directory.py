"""The 'scrapDirectory' function removes empty directories."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import validateExistingDirectory

if TYPE_CHECKING:  # pragma: no cover
  pass


def scrapDirectory(dirPath: str, **kwargs) -> None:
  """Remove the empty directory at 'dirPath'.

  Parameters
  ----------
  dirPath : str
      Absolute path to the directory to remove.
  **kwargs
      Pass 'strict=False' to return silently (instead of raising
      'FileNotFoundError') when the directory does not exist.

  Raises
  ------
  PathSyntaxException
      If 'dirPath' is not an absolute path.
  FileNotFoundError
      If the directory does not exist and 'strict' is True (the
      default).
  NotADirectoryError
      If 'dirPath' exists but is not a directory (raised regardless
      of 'strict').
  OSError
      If the directory exists but is not empty (from 'os.rmdir').
  """
  try:
    validateExistingDirectory(dirPath)
  except FileNotFoundError as fileNotFoundError:
    if kwargs.get('strict', True):
      raise fileNotFoundError
  except NotADirectoryError as notADirectoryError:
    infoSpec = """The path received by 'scrapDirectory': '%s' is not a 
    directory!"""
    info = textFmt(infoSpec % dirPath)
    raise NotADirectoryError(info) from notADirectoryError
  else:
    os.rmdir(dirPath)
