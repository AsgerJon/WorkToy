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
    e = """The pyproject.toml file at the specified directory: %s is not a
    file!"""
    raise IsADirectoryError(' '.join(e.split()) % here)
  e = """Unable to find the pyproject.toml file at the specified 
  directory: %s!"""
  if kwargs.get('strict', True):
    raise FileNotFoundError(' '.join(e.split()) % here)
  return file


def _updateTag() -> None:
  """Retrieves the version of the worktoy package. """
  with open(_loadFile('worktoy_version.json'), 'r') as file:
    v = json.load(file)
  patch = v['patch']
  minor = v['minor']
  major = v['major']
  dev = v['dev']
  if 'dev' in sys.argv:
    major, minor, patch, dev = major, minor, patch, dev + 1
  elif 'patch' in sys.argv:
    major, minor, patch, dev = major, minor, patch + 1, 0
  elif 'minor' in sys.argv:
    major, minor, patch, dev = major, minor + 1, 0, 0
  elif 'major' in sys.argv:
    major, minor, patch, dev = major + 1, 0, 0, 0
  else:
    major, minor, patch, dev = major, minor, patch + 1, 0
  if 'dev' in sys.argv:
    tag = '%d.%d.%d.dev%d' % (major, minor, patch, dev)
  else:
    tag = '%d.%d.%d' % (major, minor, patch)
  tagFile = _loadFile('worktoy.tag', strict=False)
  with open(tagFile, 'w', encoding='utf-8') as file:
    file.write(tag)
  version = {'major': major, 'minor': minor, 'patch': patch, 'dev': dev}
  with open(_loadFile('worktoy_version.json'), 'w') as file:
    json.dump(version, file, indent=2)
  projectFile = _loadFile('pyproject.toml')
  with open(projectFile, 'r', encoding='utf-8') as file:
    lines = file.readlines()
  newLines = []
  while lines:
    line = lines.pop(0)
    if 'version' in line:
      line = 'version = "%s"\n' % tag
      newLines.append(line)
      newLines = [*newLines, *lines]
      break
  else:
    e = """Unable to find the 'version' key in the 'tool.poetry' section of
    the pyproject.toml file!"""
    raise KeyError(' '.join(e.split()))
  with open(projectFile, 'w', encoding='utf-8') as file:
    file.writelines(newLines)


if __name__ == '__main__':
  try:
    _updateTag()
    sys.exit(0)
  except Exception as exception:
    print(exception)
    sys.exit(1)
