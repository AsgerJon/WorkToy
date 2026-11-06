"""
TestFlexCallHook tests 'FlexCallHook' from 'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import isFlex, overload
from worktoy.mcls import BaseSpace
from worktoy.mcls.space_hooks import FlexCallHook
from . import MclsTest, FlexSpace, FlexMeta


class TestFlexCallHook(MclsTest):
  """
  'FlexCallHook' wraps every plain function of a class dictionary with
  'flexCall' after the body is merged, so the methods take and drop
  surplus positional arguments; nothing else in the dictionary is
  touched, and 'flexCall' itself leaves a dunder method as it is. The
  tests pin the wrapping on a class built under 'FlexMeta', the values
  left alone, the hook called by hand, and that 'BaseSpace' itself
  declares no such hook.
  """

  def test_methods_take_surplus_arguments(self) -> None:
    class A(metaclass=FlexMeta):
      def first(self, x: int) -> int:
        return x

      def pair(self, x: int, y: int) -> tuple:
        return x, y

    self.assertTrue(isFlex(A.__dict__['first']))
    self.assertTrue(isFlex(A.__dict__['pair']))
    a = A()
    self.assertEqual(a.first(1), 1)
    self.assertEqual(a.first(1, 2, 3), 1)
    self.assertEqual(a.pair(1, 2, 3), (1, 2))
    with self.assertRaises(TypeError) as context:
      a.pair(1)
    self.assertIn("'pair' requires at least '3'", str(context.exception))

  def test_other_values_left_alone(self) -> None:
    class A(metaclass=FlexMeta):
      count = 5

      @classmethod
      def kind(cls) -> str:
        return cls.__name__

      @overload(int)
      def take(self, n: int) -> int:
        return n

      def __repr__(self) -> str:
        return 'A'

    self.assertFalse(isFlex(A.__dict__['__repr__']))
    self.assertEqual(repr(A()), 'A')
    self.assertEqual(A.__dict__['count'], 5)
    self.assertIsInstance(A.__dict__['kind'], classmethod)
    self.assertEqual(A.kind(), 'A')
    self.assertFalse(isFlex(A.__dict__['take']))
    self.assertEqual(A().take(3), 3)

  def test_by_hand(self) -> None:
    hook = FlexCallHook()

    def plain(x: int) -> int:
      return x

    compiled = {'plain': plain, 'count': 1}
    self.assertIs(hook.postCompilePhase(compiled), compiled)
    self.assertTrue(isFlex(compiled['plain']))
    self.assertEqual(compiled['plain'](4, 5), 4)
    self.assertEqual(compiled['count'], 1)

  def test_declared_only_where_wanted(self) -> None:
    hook = FlexSpace.__dict__['flexCallHook']
    self.assertIs(FlexSpace.classGetHooks()[-1], hook)
    self.assertNotIn(hook, BaseSpace.classGetHooks())
    self.assertIs(FlexMeta.getNamespaceClass(), FlexSpace)
