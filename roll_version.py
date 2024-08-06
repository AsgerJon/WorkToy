#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import json
import os.path
import sys


def _loadFile(file: str, **kwargs) -> str:
  """Loads the content of the specified file."""
  here = os.path.abspath(os.path.dirname(__file__))
  file = os.path.join(here, file)
  if os.path.exists(file):
    if os.path.isfile(file):
      return file
    e = """The file at the specified directory: %s is not a
    file!"""
    raise IsADirectoryError(' '.join(e.split()) % here)
  e = """Unable to find file at the specified directory: %s!"""
  if kwargs.get('strict', True):
    raise FileNotFoundError(' '.join(e.split()) % here)
  return file


def incrementVersion() -> None:
  """Loads the content of the specified JSON file."""
  with open(_loadFile('worktoy_version.json'), 'r') as file:
    existingVersion = json.load(file)
  oldMajor = existingVersion['major']
  oldMinor = existingVersion['minor']
  oldPatch = existingVersion['patch']
  oldDev = existingVersion['dev']
  updateLevel = None
  tag = None
  for arg in sys.argv:
    if arg.lower() in ['major', 'minor', 'patch', 'dev']:
      updateLevel = arg
      break
  else:
    updateLevel = 'dev'
  existingVersion[updateLevel] += 1
  if updateLevel in ['major', 'minor', 'patch']:
    existingVersion['dev'] = 0
  if updateLevel in ['major', 'minor']:
    existingVersion['patch'] = 0
  if updateLevel == 'major':
    existingVersion['minor'] = 0
  with open(_loadFile('worktoy_version.json', strict=False), 'w') as file:
    json.dump(existingVersion, file, indent=2)
  major = existingVersion['major']
  minor = existingVersion['minor']
  patch = existingVersion['patch']
  dev = existingVersion['dev']
  if updateLevel == 'dev':
    tag = f'{major}.{minor}.{patch}.dev{dev}'
  else:
    tag = f'{major}.{minor}.{patch}'
  with open(_loadFile('worktoy-tag.txt', strict=False), 'w') as file:
    file.write(tag)
  with open(_loadFile('pyproject.toml'), 'r', encoding='utf-8') as file:
    lines = file.readlines()
  newLines = []
  while lines:
    line = lines.pop(0)
    if 'version' in line:
      line = f'version = "{tag}"\n'
      newLines.append(line)
      newLines = [*newLines, *lines]
      break
    newLines.append(line)
  else:
    e = """Unable to find the 'version' pyproject.toml file!"""
    raise KeyError(' '.join(e.split()))
  with open(_loadFile('pyproject.toml'), 'w', encoding='utf-8') as file:
    file.writelines(newLines)


if __name__ == '__main__':
  try:
    incrementVersion()
    sys.exit(0)
  except Exception as exception:
    print(exception)
    sys.exit(1)
