"""TestDevNull tests that stuff exists. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase


class TestDevNull(TestCase):
  """TestDevNull tests that stuff exists. """

  def setUp(self, ) -> None:
    """Set up the test case."""
    print("""$RUNNING_TESTS: %s""" % os.environ.get('RUNNING_TESTS', ''))

  def test_dev_null(self) -> None:
    """Tests that stuff exists."""
    self.assertTrue(True)
