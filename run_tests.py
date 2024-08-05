#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from unittest import TestLoader, TextTestRunner


def main(*args) -> int:
  """Main Tester Script"""
  loader = TestLoader()
  here = os.path.abspath(os.path.dirname(__file__))
  testPath = os.path.join(here, 'tests')
  suite = loader.discover(start_dir=testPath, pattern='test_*.py')
  runner = TextTestRunner(verbosity=0)
  result = runner.run(suite)
  if result.wasSuccessful():
    return 0
  return 1


if __name__ == '__main__':
  sys.exit(main())
