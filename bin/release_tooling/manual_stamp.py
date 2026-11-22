"""
This script keeps the copy of 'README.md' at the top of
'design/manual.md' up to date. The manual begins with the README, word
for word, and goes on from the line '# The Manual'. A release stamps its
version into the heading of the README, and a release candidate or a
release stamps the token badge as well, so 'version_stamp.py' and
'token_stamp.py' each call 'stampManual' once they have written the
README, and the manual follows in the same step.

Usage from the command line, anywhere in the repository:

  python bin/release_tooling/manual_stamp.py
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import os

MARKER = '# The Manual'


def _here() -> str:
  """
  This function resolves the path to the present directory containing this
  script.

  Returns
  -------
  str
    The absolute path to the present directory containing this script.
  """
  filePath: str = os.path.abspath(__file__)
  return os.path.dirname(filePath)


def _root() -> str:
  """
  This function resolves the repository root by walking up from this
  script's directory until it finds the directory holding 'pyproject.toml',
  so the script works regardless of how deeply it is nested under the root.

  Returns
  -------
  str
    The absolute path to the repository root.

  Raises
  ------
  RuntimeError
    If no ancestor directory holds 'pyproject.toml'.
  """
  current = _here()
  while current != os.path.dirname(current):
    if os.path.isfile(os.path.join(current, 'pyproject.toml')):
      return current
    current = os.path.dirname(current)
  infoSpec = """Found no 'pyproject.toml' above: '%s'!"""
  raise RuntimeError(infoSpec % _here())


def _readLines(path: str) -> list[str]:
  """
  This function reads the file at 'path' and returns its lines without
  trailing newline characters.

  Parameters
  ----------
  path : str
    The absolute path to the file to read.

  Returns
  -------
  list[str]
    The lines of the file.
  """
  f = None
  try:
    f = open(path, 'r', encoding='utf-8')
  except Exception as exception:
    raise exception
  else:
    return str.split(f.read(), '\n')
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def _writeLines(path: str, lines: list[str]) -> None:
  """
  This function writes 'lines' to the file at 'path', joined by newline
  characters.

  Parameters
  ----------
  path : str
    The absolute path to the file to write.
  lines : list[str]
    The lines to write.
  """
  f = None
  try:
    f = open(path, 'w', encoding='utf-8')
  except Exception as exception:
    raise exception
  else:
    f.write(str.join('\n', lines))
  finally:
    try:
      f.close()  # noqa: F821
    except AttributeError:
      pass


def stampManual(root: str) -> None:
  """
  This function replaces the copy of the README at the top of
  'design/manual.md' with 'README.md' as it now reads. Everything from
  the line '# The Manual' on is kept as it is. A manual without that line
  is an error, since nothing would say where the copy ends, and the file
  is then left untouched.

  Parameters
  ----------
  root : str
    The absolute path to the repository root.

  Raises
  ------
  RuntimeError
    If 'design/manual.md' holds no line '# The Manual'.
  """
  readmePath = os.path.join(root, 'README.md')
  manualPath = os.path.join(root, 'design', 'manual.md')
  manualLines = _readLines(manualPath)
  for i, line in enumerate(manualLines):
    if line == MARKER:
      rest = manualLines[i:]
      break
  else:
    infoSpec = """Found no line '%s' in file: '%s'!"""
    raise RuntimeError(infoSpec % (MARKER, manualPath))
  readmeLines = _readLines(readmePath)
  while readmeLines and not readmeLines[-1]:
    readmeLines = readmeLines[:-1]
  _writeLines(manualPath, [*readmeLines, '', *rest])


def main(*args: str) -> int:
  """
  This function is the entry point of the script: it refreshes the copy
  of the README at the top of 'design/manual.md' of this repository.

  Parameters
  ----------
  *args : str
    Command line arguments; none is expected.

  Returns
  -------
  int
    0 on success and 1 on failure, as the exit code of the process.
  """
  if args:
    print("""Usage: python manual_stamp.py""")
    return 1
  try:
    stampManual(_root())
  except Exception as exception:
    print("""Failed to refresh 'design/manual.md': %s""" % exception)
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main(*sys.argv[1:]))
