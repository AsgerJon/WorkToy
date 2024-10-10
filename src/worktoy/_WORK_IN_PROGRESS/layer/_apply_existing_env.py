"""The 'applyExistingEnv' function applies the existing environment to a
string containing references to environment variables. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os


def applyExistingEnv(s: str) -> str:
  """The 'applyExistingEnv' function applies the existing environment to a
  string containing references to environment variables. """
  for k, v in os.environ.items():
    s = s.replace(f"${k}", v)
  return s
