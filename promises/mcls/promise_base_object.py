"""
PromiseBaseObject promises 'BaseObject' and 'BaseMeta' from
'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import abc
import threading
from unittest import TestCase

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject, BaseMeta


class PromiseBaseObject(TestCase):
  """
  'BaseObject' is the base of a worktoy class: it gives overloads, the
  checks of the class body and the class-level hooks at once. A class
  defining no initializer refuses constructor arguments with Python's own
  'TypeError', as a plain class does. A base listed after it, such as
  'threading.Thread', is initialized as in a plain class. A base built by
  'abc.ABCMeta', such as 'abc.ABC', beside 'BaseObject' raises Python's
  metaclass conflict, while a metaclass based on both, 'class
  ABCBaseMeta(BaseMeta, ABCMeta)', builds the class with its abstract
  methods and its overloads. Under such a metaclass 'abc' asks
  '__subclasshook__' as well, so a hook refusing subclasses returns
  'NotImplemented' when it does not refuse. Source: the docstrings of
  'BaseObject',
  'BaseMeta' and the 'mcls' package.
  """

  def test_no_initializer(self) -> None:
    class Point(BaseObject):
      pass

    with self.assertRaises(TypeError):
      Point(1)

  def test_base_after(self) -> None:
    class Worker(BaseObject, threading.Thread):
      pass

    self.assertFalse(Worker().is_alive())

  def test_abc(self) -> None:
    with self.assertRaises(TypeError):
      class Conflict(BaseObject, abc.ABC):
        pass

    class ABCBaseMeta(BaseMeta, abc.ABCMeta):
      pass

    class Shape(BaseObject, metaclass=ABCBaseMeta):
      @abc.abstractmethod
      def area(self) -> float:
        pass

      @overload(int)
      def scale(self, factor: int) -> int:
        return factor

    class Square(Shape):
      def area(self) -> float:
        return 1.0

    with self.assertRaises(TypeError):
      Shape()
    self.assertEqual(Square().area(), 1.0)
    self.assertEqual(Square().scale(2), 2)

  def test_abc_subclass_hook(self) -> None:
    class ABCBaseMeta(BaseMeta, abc.ABCMeta):
      pass

    class Gate(BaseObject, metaclass=ABCBaseMeta):
      @classmethod
      def __subclasshook__(cls, sub: type) -> object:
        if sub.__name__.startswith('Bad'):
          raise TypeError('refused')
        return NotImplemented

    class Good(Gate):
      pass

    self.assertTrue(issubclass(Good, Gate))
    self.assertFalse(issubclass(int, Gate))
    with self.assertRaises(TypeError):
      class BadChild(Gate):
        pass
