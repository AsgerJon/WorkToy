"""
TestBaseOverload tests the simple use of the overload functionality. By
simple, we mean the simple case of overloaded constructors tested on the
class defining them without any inheritance or other complications.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import OverloadTest

from tests import WYD
from worktoy.mcls import BaseObject
from worktoy.static import Dispatch, overload
from worktoy.waitaminute.dispatch import DispatchException
from . import ComplexOverload, OverloadTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBaseOverload(OverloadTest):
  """
  TestBaseOverload tests the simple use of the overload functionality. By
  simple, we mean the simple case of overloaded constructors tested on the
  class defining them without any inheritance or other complications.
  """

  def setUp(self, ) -> None:
    """
    Set up the test case by creating an instance of ComplexOverload.
    """
    self.fast1 = (0.80085, 0.1337)
    self.fast2 = (420 + 69j)
    self.cast1 = (69, 420)
    self.cast2 = ('0.80085', '0.1337')

  def test_init(self, ) -> None:
    """
    Test that the ComplexOverload can actually be instantiated
    """
    fast1Z = ComplexOverload(*self.fast1)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)
    cast1Z = ComplexOverload(*self.cast1)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._castDispatch)
    fast2Z = ComplexOverload(self.fast2)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)
    cast2Z = ComplexOverload(*self.cast2)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._castDispatch)
    fast3Z = ComplexOverload(fast1Z)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)
    self.assertEqual(ComplexOverload.__init__.__name__, '__init__')

  def test_good_get(self, ) -> None:
    """
    Test that the RE and IM attributes can be accessed correctly.
    """
    z = ComplexOverload(*self.fast1)
    self.assertEqual(z.RE, self.fast1[0])
    self.assertEqual(z.IM, self.fast1[1])
    z = ComplexOverload(*self.cast1)
    self.assertEqual(z.RE, float(self.cast1[0]))
    self.assertEqual(z.IM, float(self.cast1[1]))
    z = ComplexOverload(self.fast2)
    self.assertEqual(z.RE, self.fast2.real)
    self.assertEqual(z.IM, self.fast2.imag)
    z = ComplexOverload(*self.cast2)
    self.assertEqual(z.RE, float(self.cast2[0]))
    self.assertEqual(z.IM, float(self.cast2[1]))

  def test_str_repr(self) -> None:
    """
    Test that the __str__ and __repr__ methods return the expected values.
    """
    func = ComplexOverload.__init__
    self.assertEqual(str(func), repr(func))

  def test_exception(self) -> None:
    """
    Test that the ComplexOverload raises an exception when given invalid
    arguments.
    """

    class Foo(BaseObject):
      """
      This class has an overloaded method called 'bar'
      """

      @overload(int)
      def bar(self, x: int) -> None:
        """
        Overloaded method that takes an integer.
        """
        raise WYD(int)

      @overload(str)
      def bar(self, x: str) -> None:
        """
        Overloaded method that takes a string.
        """
        raise WYD(str)

    foo = Foo()
    with self.assertRaises(DispatchException) as context:
      foo.bar(69, 420)
    e = context.exception
    self.assertIs(e.dispatchObject, Foo.bar)
    self.assertEqual(e.receivedArguments, (foo, 69, 420))
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(WYD):
      foo.bar(69)
    with self.assertRaises(WYD):
      foo.bar('420')
