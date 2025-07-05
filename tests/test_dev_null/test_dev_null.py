"""TestDevNull tests that stuff exists. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from tests import WYD
from worktoy.utilities import ClassBodyTemplate

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

  def test_wyd(self) -> None:
    """Tests that WYD exists."""
    with self.assertRaises(WYD):
      try:
        raise OSError("""breh""")
      except OSError as e:
        raise WYD(e)

    with self.assertRaises(WYD):
      raise WYD("""lmao""")

  def test_class_body_template(self) -> None:
    """Tests that the class body template exists."""
    self.assertIsInstance(ClassBodyTemplate, str)
