"""The UnstupidTest repairs much stupid found in the original """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn
from unittest import TestCase


class UnstupidTest(TestCase):
  """The UnstupidTest repairs much stupid found in the original """

  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence

  def __enter__(self) -> NoReturn:
    """Context manager should set a flag, to suppress too much debug info"""
    globals()['asserting'] = True
    TestCase.__enter__(self)

  def __exit__(self, ) -> NoReturn:
    """Context manager should set a flag, to suppress too much debug info"""
    globals()['asserting'] = False
    TestCase.__exit__(self)
