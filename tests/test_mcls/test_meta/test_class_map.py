"""
TestClassMap tests that classes derived from 'BaseMeta' that implement
'__class_setitem__' and '__class_getitem__' are called correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.utilities import maybe

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ClassMap(metaclass=AbstractMetaclass):
  """
  Testing ClassMap that uses __class_setitem__ and __class_getitem__
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __inner_store__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getStore(cls, ) -> dict:
    """
    Returns the inner store dictionary.
    """
    return maybe(cls.__inner_store__, dict())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def _setStoreItem(cls, key: Any, value: Any) -> None:
    """
    Sets an item in the inner store dictionary.
    """
    existing = cls._getStore()
    existing[key] = value
    cls.__inner_store__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DELETERS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _delStoreItem(cls, key: Any) -> None:
    """
    Deletes an item from the inner store dictionary.
    """
    existing = cls._getStore()
    if key in existing:
      del existing[key]
      cls.__inner_store__ = existing
    else:
      raise KeyError(key)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def __class_getitem__(cls, key: Any) -> Any:
    """
    Retrieves item from the inner store dictionary. Raises KeyError if
    given key is not found in the store.
    """
    existing = cls._getStore()
    if key in existing:
      return existing[key]
    raise KeyError(key)

  @classmethod
  def __class_setitem__(cls, key: Any, value: Any) -> None:
    """
    Sets an item in the inner store dictionary.
    """
    cls._setStoreItem(key, value)

  @classmethod
  def __class_delitem__(cls, key: Any) -> None:
    """
    Removes an item from the inner store dictionary. Raises KeyError if
    given key is not found in the store.
    """
    cls._delStoreItem(key)


class NoDictSupport(metaclass=AbstractMetaclass):
  """Used to verify fallback error behavior."""


class TestClassMap(TestCase):
  """
  Verifies dict-like behavior at the class level.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def testSetAndGetItem(self) -> None:
    """
    Tests setting and retrieving an item via ClassMap.
    """
    ClassMap['foo'] = 123
    self.assertEqual(ClassMap['foo'], 123)

  def testOverwriteItem(self) -> None:
    """
    Tests overwriting an existing key.
    """
    ClassMap['key'] = 'initial'
    ClassMap['key'] = 'updated'
    self.assertEqual(ClassMap['key'], 'updated')

  def testDeleteItem(self) -> None:
    """
    Tests deleting an item.
    """
    ClassMap['to_delete'] = 69
    self.assertEqual(ClassMap['to_delete'], 69)
    del ClassMap['to_delete']
    with self.assertRaises(KeyError):
      _ = ClassMap['to_delete']
    with self.assertRaises(KeyError):
      _ = ClassMap['missing lol']
    with self.assertRaises(KeyError):
      del ClassMap['missing lol']

  def testGetMissingKey(self) -> None:
    """
    Getting a non-existent key should raise KeyError.
    """
    with self.assertRaises(KeyError):
      _ = ClassMap['missing']

  def testDelMissingKey(self) -> None:
    """
    Deleting a non-existent key should raise KeyError.
    """
    with self.assertRaises(KeyError):
      del ClassMap['void']

  def testSetFallback(self) -> None:
    """
    Class without __class_setitem__ should raise AttributeError.
    """
    with self.assertRaises(AttributeError):
      NoDictSupport['fail'] = 1

  def testDelFallback(self) -> None:
    """
    Class without __class_delitem__ should raise AttributeError.
    """
    with self.assertRaises(AttributeError):
      del NoDictSupport['fail']
