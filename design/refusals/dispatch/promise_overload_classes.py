"""
RefusedOverloadClasses holds the refusals that belong with
'design.promises.dispatch.promise_overload_classes'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException


class RefusedOverloadClasses(TestCase):
  """
  The mistakes of the tests below are refused, each with the exception its
  test names as of 1.2.3. Source: the docstrings of 'overload' and
  'Dispatcher'.
  """

  def test_static_and_bound_each_reached_one_way_1(self) -> None:
    class File(BaseObject):
      @overload()
      def exists(self) -> tuple:
        return 'bound', self

      @staticmethod
      @overload(str)
      def exists(name: str) -> tuple:
        return 'static', name

    file = File()
    with self.assertRaises(Exception) as refused:
      file.exists('notes')
    self.assertIsInstance(refused.exception, DispatchException)

  def test_static_and_bound_each_reached_one_way_2(self) -> None:
    class File(BaseObject):
      @overload()
      def exists(self) -> tuple:
        return 'bound', self

      @staticmethod
      @overload(str)
      def exists(name: str) -> tuple:
        return 'static', name

    file = File()
    with self.assertRaises(Exception) as refused:
      File.exists(file)
    self.assertIsInstance(refused.exception, DispatchException)

  def test_classmethod_and_bound(self) -> None:
    class Color(BaseObject):
      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

      @overload(int)
      def make(self, shade: int) -> tuple:
        return 'bound', self, shade

    red = Color()
    with self.assertRaises(Exception) as refused:
      Color.make(3)
    self.assertIsInstance(refused.exception, DispatchException)
