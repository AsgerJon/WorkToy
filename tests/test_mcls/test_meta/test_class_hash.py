"""
TestClassHash tests that classes derived from 'AbstractMetaclass' that
implement __class_hash__ are called correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass

if TYPE_CHECKING:  # pragma: no cover
  pass


class Christiania(metaclass=AbstractMetaclass):
  """
  Implements __class_hash__ but not __class_eq__
  """

  @classmethod
  def __class_hash__(cls) -> int:
    """
    Returns a fixed hash value.
    """
    return 69


class TupleEq(metaclass=AbstractMetaclass):
  """
  Implements both __class_hash__ and __class_eq__
  """

  @classmethod
  def __class_hash__(cls) -> int:
    """
    Returns a fixed hash value.
    """
    return 420


class TestClassHash(TestCase):
  """
  TestClassHash tests that classes derived from 'AbstractMetaclass' that
  implement __class_hash__ are called correctly.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_class_hash(self):
    """
    Tests that the class hash is called correctly.
    """
    self.assertEqual(Christiania.__class_hash__(), 69)
    self.assertEqual(TupleEq.__class_hash__(), 420)
