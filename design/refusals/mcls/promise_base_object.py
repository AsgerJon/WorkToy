"""
RefusedBaseObject holds the refusals that belong with
'design.promises.mcls.promise_base_object'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import abc
from unittest import TestCase

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject, BaseMeta


class RefusedBaseObject(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A class defining no initializer refuses constructor arguments
  with Python's own 'TypeError', as a plain class does. Source: the
  docstrings of 'BaseObject', 'BaseMeta' and the 'mcls' package.
  """

  def test_no_initializer(self) -> None:
    class Point(BaseObject):
      pass

    with self.assertRaises(Exception) as refused:
      Point(1)
    self.assertIsInstance(refused.exception, TypeError)

  def test_abc_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Conflict(BaseObject, abc.ABC):
        pass
    self.assertIsInstance(refused.exception, TypeError)

  def test_abc_2(self) -> None:
    class ABCBaseMeta(BaseMeta, abc.ABCMeta):
      pass

    class Shape(BaseObject, metaclass=ABCBaseMeta):
      @abc.abstractmethod
      def area(self) -> float:
        pass

      @overload(int)
      def scale(self, factor: int) -> int:
        return factor

    with self.assertRaises(Exception) as refused:
      Shape()
    self.assertIsInstance(refused.exception, TypeError)
