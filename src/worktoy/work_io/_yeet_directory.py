"""The 'yeetDirectory' function removes a directory with all contents.
Effectively the same as: 'rm -rf <directory>'."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

from ..text import monoSpace

from ..waitaminute import PathSyntaxException

from . import validateExistingDirectory

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


def yeetDirectory(dirPath: str, **kwargs) -> None:
  """
  Removes a directory with all contents. Effectively the same as: 'rm -rf
  <directory>'.

  Args:
    dirPath (str): The path to the directory to remove.

  Returns:
    str: The path of the removed directory.

  Raises:
    FileNotFoundError: If the directory does not exist.
    NotADirectoryError: If the path is not a directory.
    PathSyntaxException: If the path is not absolute.
  """
  try:
    validateExistingDirectory(dirPath)
  except FileNotFoundError as fileNotFoundError:
    if kwargs.get('strict', True):
      raise fileNotFoundError
  except NotADirectoryError as notADirectoryError:
    infoSpec = """The path received by 'yeetDirectory': '%s' is not a 
    directory!"""
    info = monoSpace(infoSpec % dirPath)
    raise NotADirectoryError(info) from notADirectoryError
  else:
    os.rmdir(dirPath)
