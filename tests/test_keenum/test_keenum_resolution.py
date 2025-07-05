"""
Tests how well KeeNum classes resolve their members.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import auto, KeeNum
from worktoy.utilities import maybe
from worktoy.waitaminute import TypeException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Speed(KeeNum):
  """
  Speed wrapper for integer values used for indexing.
  """
  FAST = auto(1)
  SLOW = auto(2)


# Test enum class
class Mode(KeeNum):
  FAST_MODE = auto('fast')
  SLOW_MODE = auto('slow')
  TURBO = auto('fast')  # duplicate value


class TestKeeNumLookup(TestCase):

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_nameLookupFlexible(self) -> None:
    self.assertIsInstance(Mode['FAST_MODE'], Mode)
    self.assertIs(Mode['fast_mode'], Mode.FAST_MODE)

  def test_indexLookup(self) -> None:
    self.assertIs(Mode[0], Mode.FAST_MODE)
    self.assertIs(Mode[1], Mode.SLOW_MODE)
    self.assertIs(Mode[2], Mode.TURBO)
    self.assertIs(Mode[-3], Mode.FAST_MODE)
    self.assertIs(Mode[-2], Mode.SLOW_MODE)
    self.assertIs(Mode[-1], Mode.TURBO)
