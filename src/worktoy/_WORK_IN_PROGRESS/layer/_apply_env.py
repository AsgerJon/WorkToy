"""The 'applyEnv' function updates the environment with the variables in the
the given file."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from moreworktoy import loadEnv


def applyEnv(envFile: str) -> None:
  """The 'applyEnv' function updates the environment with the variables in
  the given file."""

  envData = loadEnv(envFile)

  for (key, value) in envData.items():
    os.environ[key] = value
