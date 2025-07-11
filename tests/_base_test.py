"""
BaseTest subclasses unittest.TestCase to provide a base class shared by
testclasses across the 'tests' package. It implements module unloading in
the 'tearDownClass' method and adds 'assertIsSubclass' (and negation).
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase


class BaseTest(TestCase):
  """BaseTest provides a base class shared by the testing classes in the
  tests package. It implements module unloading in the 'tearDownClass'
  method and adds 'assertIsSubclass' (and negation)."""

  @classmethod
  def tearDownClass(cls) -> None:
    """Remove the test class from sys.modules and run the garbage
    collector."""
    import sys
    import gc
    sys.modules.pop(cls.__module__, None)
    gc.collect()

  def assertIsSubclass(self, subClass: type, superClass: type, ) -> None:
    """Assert that 'subClass' is a subclass of 'superClass'."""
    self.assertTrue(issubclass(subClass, superClass))

  def assertIsNotSubclass(self, subClass: type, superClass: type, ) -> None:
    """Assert that 'subClass' is not a subclass of 'superClass'."""
    self.assertFalse(issubclass(subClass, superClass))
