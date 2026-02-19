"""BaseTest provides a base class shared by the testing classes in the
tests.test_ezdata package. It implements the shared teardown that removes
the test class from sys.modules and runs the garbage collector.
Additionally, it implements assertIsSubclass which is oddly missing from
the unittest.TestCase class."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest
from . import RegularClass, Mid1, Mid2, Mid3, SubClass

if TYPE_CHECKING:  # pragma: no cover
  pass


class EZTest(BaseTest):
  """BaseTest provides a base class shared by the testing classes in the
  tests.test_ezdata package. It implements the shared teardown that removes
  the test class from sys.modules and runs the garbage collector.
  Additionally, it implements assertIsSubclass which is oddly missing from
  the unittest.TestCase class."""

  @classmethod
  def setUpClass(cls) -> None:
    """Sets up the collection of classes and objects on which to perform
    the tests. """
    cls.sampleClasses = [
      RegularClass,
      Mid1,
      Mid2,
      Mid3,
      SubClass,
    ]
