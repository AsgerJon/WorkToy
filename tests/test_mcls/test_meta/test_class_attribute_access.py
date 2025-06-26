"""
TestClassAttributeAccess tests that classes derived from 'AbstractMetaclass'
can implement attribute access hooks:
  - __class_getattr__
  - __class_setattr__
  - __class_delattr__
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass

from unittest import TestCase
from typing import Any
from worktoy.mcls import AbstractMetaclass


class ClassAccessor(metaclass=AbstractMetaclass):
  """
  Implements all three class-level accessor hooks.
  """
  __class_dict__ = {}

  @classmethod
  def __class_getattr__(cls, key: str) -> Any:
    return f"GET<{key}>"

  @classmethod
  def __class_setattr__(cls, key: str, value: Any) -> None:
    cls.__class_dict__[key] = f"SET<{key}>={value!r}"

  @classmethod
  def __class_delattr__(cls, key: str) -> None:
    cls.__class_dict__[key] = f"DEL<{key}>"


class NoAccessors(metaclass=AbstractMetaclass):
  """Class with no custom accessor hooks."""
  foo = 42


class TestClassAttributeHooks(TestCase):
  """
  Verifies functionality and fallback behavior of accessor hooks.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self) -> None:
    """
    Clear the class dictionary before each test to ensure isolation.
    """
    ClassAccessor.__class_dict__.clear()

  def testClassGetattrHook(self) -> None:
    """
    __class_getattr__ should return string for undefined attribute.
    """
    self.assertEqual(ClassAccessor.someMissing, 'GET<someMissing>')

  def testClassSetattrHook(self) -> None:
    """
    __class_setattr__ should store the action in __class_dict__.
    """
    ClassAccessor.testKey = 123
    expected = "SET<testKey>=123"
    self.assertEqual(ClassAccessor.__class_dict__['testKey'], expected)

  def testClassDelattrHook(self) -> None:
    """
    __class_delattr__ should record deletion marker.
    """
    del ClassAccessor.deleteMe
    actual = ClassAccessor.__class_dict__.get('deleteMe', None)
    expected = 'DEL<deleteMe>'
    self.assertEqual(actual, expected)

  def testGetattrFallbackRaises(self) -> None:
    """
    Classes without __class_getattr__ should raise AttributeError.
    """
    with self.assertRaises(AttributeError):
      _ = NoAccessors.unknown

  def testSetattrFallback(self) -> None:
    """
    Classes without __class_setattr__ should still assign normally.
    """
    NoAccessors.newAttr = 'ok'
    self.assertEqual(NoAccessors.newAttr, 'ok')

  def testDelattrFallback(self) -> None:
    """
    Classes without __class_delattr__ should delete normally.
    """
    NoAccessors.temp = 'to be deleted'
    self.assertEqual(NoAccessors.temp, 'to be deleted')
    del NoAccessors.temp
    with self.assertRaises(AttributeError):
      _ = NoAccessors.temp

  def testFallbackOnlyRunsForMissingAttr(self) -> None:
    """
    '__class_getattr__' only triggers for unknown attributes.
    """

    class FallbackOnly(metaclass=AbstractMetaclass):
      knownAttr = 123

      @classmethod
      def __class_getattr__(cls, name: str) -> Any:
        return f"<{name}>"

    self.assertEqual(FallbackOnly.knownAttr, 123)
    self.assertEqual(FallbackOnly.foo, '<foo>')
    self.assertEqual(FallbackOnly.bar, '<bar>')

  def testFallbackRaisesManually(self) -> None:
    """
    '__class_getattr__' may explicitly raise AttributeError.
    """

    class StrictFallback(metaclass=AbstractMetaclass):
      @classmethod
      def __class_getattr__(cls, name: str) -> Any:
        raise AttributeError(f"{cls.__name__} has no '{name}'")

    with self.assertRaisesRegex(AttributeError, "no 'wut'"):
      _ = StrictFallback.wut

  def testOverrideBlocksFallback(self) -> None:
    """
    Real attributes block '__class_getattr__' from running.
    """

    class OverrideTest(metaclass=AbstractMetaclass):
      realAttr = 999

      @classmethod
      def __class_getattr__(cls, name: str) -> Any:
        return '<fallback>'

    self.assertEqual(OverrideTest.realAttr, 999)
    self.assertEqual(OverrideTest.missing, '<fallback>')

  def testCanReturnCallable(self) -> None:
    """
    Returned attribute can be any value, even a function.
    """

    class FunProvider(metaclass=AbstractMetaclass):
      @classmethod
      def __class_getattr__(cls, name: str) -> Any:
        return lambda *a: f"{name} was called"

    self.assertEqual(FunProvider.spam(), "spam was called")
    self.assertEqual(FunProvider.eggs(), "eggs was called")
