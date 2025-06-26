"""
TestClassHash tests that classes derived from 'AbstractMetaclass' that
implement __class_hash__ are called correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.parse import maybe

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


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
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _storeItem(cls, key: Any, value: Any) -> None:
    """
    Sets an item in the inner store dictionary.
    """
    existing = cls._getInnerStore()
    existing[key] = value
    cls.__inner_store__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_iter__(cls, ) -> type:  # Self
    """
    Prepares iteration state and returns class as iterator.
    """
    keys = [k for k, v in cls._getInnerStore().items()]
    cls.__iter_contents__ = [*reversed(keys), ]
    return cls

  @classmethod
  def __class_next__(cls) -> Any:
    """
    Manually produces next item or raises StopIteration.
    """
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop()
    cls.__iter_contents__ = None
    raise StopIteration

  @classmethod
  def __class_eq__(cls, otherCls: Any) -> bool:
    """
    Returns True if the other class is also MutableEq.
    """
    otherItems = None
    try:
      otherItems = list(otherCls)
    except TypeError as typeError:
      if 'is not iterable' in str(typeError):
        return False
      raise
    else:
      if len(cls) != len(otherItems):
        return False
      for self, other in zip(cls, otherItems):
        if self != other:
          return False
      return True

  @classmethod
  def __class_len__(cls) -> int:
    """
    Returns the length of the inner store dictionary.
    """
    return len(cls._getInnerStore())

  @classmethod
  def __class_bool__(cls) -> bool:
    """
    Returns True if the inner store dictionary is not empty.
    """
    for _ in cls:
      return True
    return False

  @classmethod
  def __class_contains__(cls, key: str, ) -> bool:
    """
    Returns True if the key is in the inner store dictionary.
    """
    for k in cls:
      if k == key:
        return True
    return False


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

    otherItems = None

    try:
      otherItems = list(other)
    except TypeError as typeError:
      if 'is not iterable' in str(typeError):
        return False
      raise
    else:
      return True if all(i == j for i, j in zip(cls, otherItems)) else False


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
