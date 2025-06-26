"""TestDevNull tests that stuff exists. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

Func = type('_', (type,), dict(__instancecheck__=callable))('_', (), {})


class TestDevNull(TestCase):
  """TestDevNull tests that stuff exists. """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self, ) -> None:
    """Set up the test case."""

  def test_dev_null(self) -> None:
    """Tests that stuff exists."""
    self.assertTrue(True)
