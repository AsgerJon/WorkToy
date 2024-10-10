"""The loadEnv function loads the environment from the file. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.text import monoSpace

from moreworktoy import validateFile, findEnvNames


def loadEnv(fid: str) -> dict[str, str]:
  """The loadEnv function loads the environment from the file. """
  testFile = validateFile(fid)
  env = {}
  data = None

  with open(testFile, 'r') as f:
    data = f.readlines()

  if data is None:
    e = """Error reading file at: '%s'""" % testFile
    raise IOError(e)

  for line in data:
    if not line or line.startswith('#'):
      continue
    if '=' not in line:
      e = """The line: '%s' does not contain an equal sign!""" % line
      raise SyntaxError(monoSpace(e))
    entry = line.split('=')
    if len(entry) > 2:
      e = """The line: '%s' contains more than one equal sign!""" % line
      raise SyntaxError(monoSpace(e))
    key, value = entry
    for name in findEnvNames(value):
      value = value.replace('$%s' % name, os.environ.get(name, ''))
    env[key] = value.strip()
  return env
