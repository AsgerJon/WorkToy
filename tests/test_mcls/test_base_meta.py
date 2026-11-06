"""
TestBaseMeta tests 'BaseMeta' from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod

from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import AbstractMetaclass, BaseMeta, BaseSpace, BaseObject
from . import MclsTest, FlexSpace, FlexMeta


class TestBaseMeta(MclsTest):
  """
  'BaseMeta' is 'AbstractMetaclass' with 'BaseSpace' as its namespace,
  so a class it builds declares overloads. The tests pin the namespace,
  a metaclass built on it with a namespace of its own, a class built
  without 'BaseObject', and the combination with 'abc.ABCMeta' the
  package docstring describes, beside the conflict it avoids.
  """

  def test_prepare_gives_base_space(self) -> None:
    space = BaseMeta.__prepare__('A', (BaseObject,), tag=1)
    self.assertIs(type(space), BaseSpace)
    self.assertIs(space.getMetaclass(), BaseMeta)
    self.assertEqual(space.getBases(), (BaseObject,))
    self.assertEqual(space.getKwargs(), {'tag': 1})
    self.assertIs(BaseMeta.getNamespaceClass(), BaseSpace)
    self.assertIsSubclass(BaseMeta, AbstractMetaclass)

  def test_metaclass_with_own_namespace(self) -> None:
    self.assertIsSubclass(FlexMeta, BaseMeta)
    self.assertIs(FlexMeta.getNamespaceClass(), FlexSpace)

    class A(metaclass=FlexMeta):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

    self.assertIsInstance(A.__namespace__, FlexSpace)
    self.assertEqual(A().f(1), 'int')

  def test_overloads_without_base_object(self) -> None:
    class A(metaclass=BaseMeta):
      @overload(int)
      def f(self, n: int) -> str:
        return 'int'

      @overload(str)
      def f(self, s: str) -> str:
        return 's'

    self.assertIsInstance(A.__dict__['f'], Dispatcher)
    self.assertEqual(A().f(1), 'int')
    self.assertEqual(A().f('s'), 's')
    self.assertNotIsInstance(A(), BaseObject)

  def test_combined_with_abc_meta(self) -> None:
    class ABCBaseMeta(BaseMeta, ABCMeta):
      pass

    class Shape(BaseObject, metaclass=ABCBaseMeta):
      @abstractmethod
      def area(self) -> float:
        """Every shape has one."""

      @overload(int)
      def scale(self, n: int) -> str:
        return 'int'

    class Square(Shape):
      def area(self) -> float:
        return 1.0

    with self.assertRaises(TypeError):
      Shape()
    self.assertEqual(Square().scale(2), 'int')
    self.assertEqual(Square().area(), 1.0)
    self.assertIsInstance(Square.__dict__['scale'], Dispatcher)
    self.assertIsInstance(Square(), Shape)
    self.assertIs(type(Square), ABCBaseMeta)

  def test_abc_beside_base_object_conflicts(self) -> None:
    with self.assertRaises(TypeError):
      class Bad(BaseObject, ABC):
        """Never runs: the metaclasses conflict first."""

