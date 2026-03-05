"""
The 'profileTests' wraps the 'runTests' function in a profiler.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import cProfile

from yolo_dev import runTests

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable

here = os.path.dirname(__file__)
fileName = """results.prof"""
filePath = os.path.join(here, fileName)


def profileTests() -> int:
  """Profiles the tests."""

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
