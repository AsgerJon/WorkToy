"""
The 'profileTests' wraps the 'runTests' function in a profiler.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from datetime import datetime
from typing import TYPE_CHECKING

import cProfile

from yolo_dev import runTests

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Callable

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
fileSpec = """results_%s.prof"""


def profileTests() -> int:
  """Profiles the tests."""

  stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
  filePath = os.path.join(root, 'tmp', fileSpec % stamp)
  profiler = cProfile.Profile()

  try:
    profiler.enable()
  except Exception as exception:
    infoSpec = """When attempting to enable the profiler, caught %s: %s"""
    info = infoSpec % (type(exception).__name__, str(exception))
    print(info)
    raise exception
  else:
    return runTests()
  finally:
    try:
      profiler.disable()
    except Exception as exception:
      infoSpec = """When attempting to disable the profiler, caught %s: %s"""
      info = infoSpec % (type(exception).__name__, str(exception))
      print(info)
      raise exception
    else:
      profiler.dump_stats(filePath)
      infoSpec = """Profiler results saved to '%s'!"""
      info = infoSpec % (filePath,)
      print(info)
