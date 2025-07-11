"""TestDevNull tests that stuff exists. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import BaseTest
from tests import WYD
from worktoy.utilities import ClassBodyTemplate


class TestDevNull(BaseTest):
  """TestDevNull tests that stuff exists. """

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
