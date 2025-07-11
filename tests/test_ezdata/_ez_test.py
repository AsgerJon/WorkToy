"""BaseTest provides a base class shared by the testing classes in the
tests.test_ezdata package. It implements the shared teardown that removes
the test class from sys.modules and runs the garbage collector.
Additionally, it implements assertIsSubclass which is oddly missing from
the unittest.TestCase class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import BaseTest

from . import baseValues
from . import RegularClass, Mid1, Mid2, Mid3, SubClass
from . import AnnotatedClass, MidNote1, MidNote2, MidNote3, SubNotated

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, Any, Iterator


class EZTest(BaseTest):
  """BaseTest provides a base class shared by the testing classes in the
  tests.test_ezdata package. It implements the shared teardown that removes
  the test class from sys.modules and runs the garbage collector.
  Additionally, it implements assertIsSubclass which is oddly missing from
  the unittest.TestCase class."""

  @staticmethod
  def getBaseValues(n: int = None) -> Iterator[int]:
    """Returns the base values for the test classes. If n is provided,
    returns a tuple of the first n base values."""
    if n is None:
      for item in baseValues:
        yield item
    else:
      for i in range(n):
        yield baseValues[i % len(baseValues)]

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
        AnnotatedClass,
        MidNote1,
        MidNote2,
        MidNote3,
        SubNotated,
    ]
    cls.sampleInstances = []
    for sampleClass in cls.sampleClasses:
      sample = sampleClass(*cls.getBaseValues(len(sampleClass)), )
      cls.sampleInstances.append(sample)
