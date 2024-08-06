#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from unittest import TestLoader, TextTestRunner


def main() -> int:
  """Main Tester Script"""
  # verbosityLevel = [*sys.argv, 2][1]
  loader = TestLoader()
  here = os.path.abspath(os.path.dirname(__file__))
  here = os.path.normpath(here)
  os.chdir(here)
  testPath = os.path.join(here, 'tests')
  suite = loader.discover(start_dir=testPath, pattern='test_*.py')
  runner = TextTestRunner(verbosity=2)
  result = runner.run(suite)
  if result.wasSuccessful():
    return 0
  return 1


if __name__ == '__main__':
  sys.exit(main())
