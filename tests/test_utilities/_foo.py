"""
Test module used by the TestRuntimeResolveType class
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import Bar


class Foo:
  """Has a reference to Bar"""
  bar = Bar
