"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
import unittest
from typing import Never, Any, Callable

from icecream import ic

ic.configureOutput(includeContext=True)


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world', os, sys, Never, Any, ]
  stuff = [*stuff, time, ]
  for item in stuff:
    ic(item)
  return 0


def tester01() -> int:
  """Testing metaclass stuff"""
  print(type.__subclasses__)
  for item in type.__subclasses__(type):
    print(item)
  print(type.__mro__)
  lmao = type('lmao', (object,), {})
  print(lmao.__mro__)
  return 0


def runTests() -> int:
  """Runs the tests"""
  results = []
  loader = unittest.TestLoader()
  res = None
  for item in os.listdir('tests'):
    if not item.startswith('test'):
      continue
    testPath = os.path.join('tests', item)
    suite = loader.discover(start_dir=testPath, pattern='test*.py')
    runner = unittest.TextTestRunner(verbosity=0)
    res = runner.run(suite)
    if res.wasSuccessful():
      results.append('Tests passed in: %s' % testPath)
    else:
      results.append('Tests failed in: %s' % testPath)
  for result in results:
    print(result)
  if res is None:
    return -1
  return 0


def main(*args: Callable) -> None:
  """Main Tester Script"""
  tic = time.perf_counter_ns()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  for callMeMaybe in args:
    print('\nRunning: %s\n' % callMeMaybe.__name__)
    try:
      retCode = callMeMaybe()
    except BaseException as exception:
      print('Exception: %s' % exception)
      retCode = -1
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  toc = time.perf_counter_ns() - tic
  if toc < 1000:
    print('Runtime: %d nanoseconds' % (int(toc),))
  elif toc < 1000000:
    print('Runtime: %d microseconds' % (int(toc * 1e-03),))
  elif toc < 1000000000:
    print('Runtime: %d milliseconds' % (int(toc * 1e-06),))


if __name__ == '__main__':
  main(runTests, )
