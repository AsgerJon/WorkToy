"""
TestClassHash tests that classes derived from 'AbstractMetaclass' that
implement __class_hash__ are called correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.utilities import maybe

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


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


class MutableEq(metaclass=AbstractMetaclass):
  """
  Implements __class_eq__ but not __class_hash__
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __inner_store__ = None
  __iter_contents__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getInnerStore(cls) -> dict:
    """
    Returns the inner store dictionary.
    """
    return maybe(cls.__inner_store__, dict())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_iter__(cls, ) -> Iterator[str]:  # Self
    """
    Prepares iteration state and returns class as iterator.
    """
    yield from cls._getInnerStore().keys()

  @classmethod
  def __class_len__(cls) -> int:
    """
    Returns the length of the inner store dictionary.
    """
    return len(cls._getInnerStore())


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

  @classmethod
  def __class_eq__(cls, other: Any) -> bool:
    """
    Returns True if the other class is also TupleEq.
    """
    if other is None:
      return False
    try:
      out = None
      for selfItem, otherItem in zip(cls, other):
        if selfItem != otherItem:
          out = False
      else:
        out = True
    except TypeError as typeError:
      if 'is not iterable' in str(typeError):
        return NotImplemented
      raise
    else:
      return maybe(out, NotImplemented)  # NOQA


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

  def test_class_eq(self):
    """
    Tests that the class equality is called correctly.
    """
    self.assertTrue(MutableEq == MutableEq)
    self.assertTrue(TupleEq == TupleEq)
    self.assertFalse(MutableEq == TupleEq)
