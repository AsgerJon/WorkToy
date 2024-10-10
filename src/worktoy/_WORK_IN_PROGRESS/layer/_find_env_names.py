"""This method finds environment variable names in a given string. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from string import ascii_letters, digits

from moreworktoy import DoubleDollarException


def findEnvNames(source: str) -> list[str]:
  """This method finds environment variable names in a given string. """
  if '$' not in source:
    return []
  if '$$' in source:
    raise DoubleDollarException(source)
  n = len(source)
  nameChars = ascii_letters + digits + '_'
  names = []
  for (i, char) in enumerate(source):
    if char == '$':
      j = 0
      while i + j + 1 < n and source[i + j + 1] in nameChars:
        j += 1
      if j > 0:
        name = source[i + 1:i + j + 1]
        if name[0] in digits:
          continue
        return [name, *findEnvNames(source[i + j + 1:])]
  return []
