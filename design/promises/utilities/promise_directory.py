"""
PromiseDirectory promises 'Directory' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.utilities import Directory


class PromiseDirectory(TestCase):
  """
  'Directory()' is a read-only attribute giving the absolute directory of the
  file that defines the class of the instance, so a class finds the resources
  beside its own source. Source: the 'Directory' docstring.
  """

  def test_directory_of_source(self) -> None:
    class Resource:
      home = Directory()

    here = os.path.dirname(os.path.abspath(__file__))
    self.assertEqual(Resource().home, here)
