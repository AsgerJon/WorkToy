"""
TestEZShadowedClassHook subclasses 'EZTest' and pins that an 'EZData'
class body refuses '__class_iter__', '__class_len__' and
'__class_contains__' with 'ShadowedClassHook', since 'EZMeta' iterates,
measures and searches the fields of its classes itself, so such a hook
would never be called. The other class hooks work as on any class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.meta import ShadowedClassHook

from . import EZTest


class TestEZShadowedClassHook(EZTest):
  """
  TestEZShadowedClassHook provides tests for the class hooks an EZData
  body refuses, and for one it keeps.
  """

  def test_len_hook_refused(self) -> None:
    """A '__class_len__' is refused, naming 'EZMeta' and '__len__'."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Point(EZData):
        x = EZField[int](0)
        y = EZField[int](0)

        @classmethod
        def __class_len__(cls) -> int:
          return 3  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Point')
    self.assertEqual(e.metaclassName, 'EZMeta')
    self.assertEqual(e.methodName, '__len__')

  def test_iter_hook_refused(self) -> None:
    """A '__class_iter__' is refused."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Point(EZData):
        x = EZField[int](0)

        @classmethod
        def __class_iter__(cls) -> object:
          return iter(())  # pragma: no cover
    self.assertEqual(context.exception.methodName, '__iter__')

  def test_contains_hook_refused(self) -> None:
    """A '__class_contains__' is refused."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Point(EZData):
        x = EZField[int](0)

        @classmethod
        def __class_contains__(cls, item: object) -> bool:
          return True  # pragma: no cover
    self.assertEqual(context.exception.methodName, '__contains__')

  def test_str_hook_accepted(self) -> None:
    """A '__class_str__' is accepted and called, and the class still
    measures its fields."""

    class Point(EZData):
      x = EZField[int](0)
      y = EZField[int](0)

      @classmethod
      def __class_str__(cls) -> str:
        return 'Point class'

    self.assertEqual(str(Point), 'Point class')
    self.assertEqual(len(Point), 2)
