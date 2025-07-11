"""
DescTest subclasses the tests.BaseTest class to provide a shared base
class for the test classes in the tests.test_desc package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class DescTest(BaseTest):
  """
  DescTest subclasses the tests.BaseTest class to provide a shared base
  class for the test classes in the tests.test_desc package.
  """
