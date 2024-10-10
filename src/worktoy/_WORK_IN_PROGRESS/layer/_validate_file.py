"""The 'validateFile' function receives a string and returns it if it
matches an existing file. If a second argument is given and the function
cannot validate the file, it returns the second argument otherwise the
error encountered is raised. This error may be suppressed by setting
keyword argument 'strict' to False.

For example, assuming some_file.txt is a file unlike sus_file.txt:
validateFile('some_file.txt') -> 'some_file.txt':
validateFile('sus_file.txt') -> Relevant error is raised:
validateFile('sus_file.txt', 'some_file.txt') -> 'some_file.txt':
validateFile('sus_file.txt', strict=False) -> '':

Passing both a second positional argument and setting 'strict' to False is
redundant."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path

from worktoy.text import typeMsg, monoSpace


def _parseFiles(*args) -> tuple:
  """The '_parseFiles' function receives a variable number of arguments and
  returns a tuple of the arguments that are strings. If no arguments are
  strings, an empty tuple is returned. """
  testFile, altFile = None, None
  for arg in args:
    if isinstance(arg, str):
      if testFile is None:
        testFile = arg
      else:
        altFile = arg
        break
    elif arg is not None:
      e = typeMsg('arg', arg, str)
      raise TypeError(e)
  return testFile, altFile


def validateFile(*args, **kwargs) -> str:
  """The 'validateFile' function receives a string and returns it if it
  matches an existing file. If a second argument is given and the function
  cannot validate the file, it returns the second argument otherwise the
  error encountered is raised. This error may be suppressed by setting
  keyword argument 'strict' to False.

  For example, assuming some_file.txt is a file unlike sus_file.txt:
  validateFile('some_file.txt') -> 'some_file.txt':
  validateFile('sus_file.txt') -> Relevant error is raised:
  validateFile('sus_file.txt', 'some_file.txt') -> 'some_file.txt':
  validateFile('sus_file.txt', strict=False) -> '':

  Passing both a second positional argument and setting 'strict' to False is
  redundant."""

  testFile, altFile = _parseFiles(*args)
  if testFile is None:
    e = """Received no file to validate!"""
    raise ValueError(e)
  if altFile is None and not kwargs.get('strict', True):
    altFile = ''

  if not os.path.exists(testFile):
    if altFile is not None:
      return altFile
    e = """Given file: '%s' does not exist!"""
    raise FileNotFoundError(monoSpace(e % testFile))
  if os.path.isdir(testFile):
    if altFile is not None:
      return altFile
    e = """Given file: '%s' is a directory!"""
    raise IsADirectoryError(monoSpace(e % testFile))
  try:
    with open(testFile, 'r') as f:
      f.read()
  except PermissionError as permissionError:
    if altFile is not None:
      return altFile
    e = """When trying to open file: '%s' for reading, encountered: %s"""
    e2 = e % (testFile, permissionError)
    raise PermissionError(monoSpace(e2)) from permissionError
  return testFile
