"""TestDevNull tests that stuff exists. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

Func = type('_', (type,), dict(__instancecheck__=callable))('_', (), {})


class TestDevNull(TestCase):
  """TestDevNull tests that stuff exists. """

  def setUp(self, ) -> None:
    """Set up the test case."""

  def test_dev_null(self) -> None:
    """Tests that stuff exists."""
    self.assertTrue(True)

    # print('This is a test for dev null.')
    # print(callable(print))  # True
    # print(isinstance(print, Func))  # True
    # print(Func.__instancecheck__(print))  # True
    # print(isinstance('urmom', Func))  # False
    # print(isinstance('fat', Func))  # False
    # print(isinstance(69420, Func))  # False
    # print(isinstance(Func, type))  # True
