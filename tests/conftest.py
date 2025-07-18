"""Configuration for pytest."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def cleanGlobals():
  # Reset or clear any shared registries here
  pass
