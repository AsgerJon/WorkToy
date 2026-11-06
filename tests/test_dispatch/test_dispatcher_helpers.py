"""
TestDispatcherHelpers tests the module-level helpers of
'worktoy.dispatch._dispatcher'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch._dispatcher import _dropReceiver, _uniformType
from worktoy.dispatch._dispatcher import _orderByClass, _orderByInstance
from worktoy.dispatch._dispatcher import _castWidening, _orderByCast
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException
from . import DispatchTest


def _gather(*args, **kwargs) -> tuple:
  """Returns what it received."""
  return args, kwargs


class TestDispatcherHelpers(DispatchTest):
  """
  The dispatch function leans on a few helpers: one dropping the
  receiver a staticmethod does not take, one telling whether a tail is
  of one class, three putting the arguments of a flexible call into
  declared order by exact class, by 'isinstance' and by cast, and the
  cast that widens numbers but never narrows them. The tests pin each.
  """

  def test_drop_receiver(self) -> None:
    dropped = _dropReceiver(_gather)
    self.assertEqual(dropped('receiver', 1, k=2), ((1,), {'k': 2}))
    self.assertEqual(dropped.__name__, '_gather')
    self.assertEqual(dropped.__doc__, _gather.__doc__)

  def test_uniform_type(self) -> None:
    self.assertIs(_uniformType((int, int, int)), int)
    self.assertIs(_uniformType((str,)), str)
    self.assertIsNone(_uniformType((int, str)))
    self.assertIsNone(_uniformType((int, bool)))

  def test_order_by_class(self) -> None:
    self.assertEqual(_orderByClass((str, int, str), (1, 'a', 'b')),
                     ('a', 1, 'b'))
    self.assertEqual(_orderByClass((int,), (5,)), (5,))
    self.assertEqual(_orderByClass((), ()), ())

  def test_order_by_instance(self) -> None:
    self.assertEqual(_orderByInstance((int, str), ('a', 1)), (1, 'a'))
    self.assertEqual(_orderByInstance((int,), (True,)), (True,))
    self.assertIsNone(_orderByInstance((int, str), (1,)))
    self.assertIsNone(_orderByInstance((int, int), (1, 'a')))

  def test_cast_widening(self) -> None:
    self.assertEqual(_castWidening(int, 3), 3)
    self.assertEqual(_castWidening(str, b'a'), 'a')
    self.assertEqual(_castWidening(float, 2), 2.0)
    self.assertIs(type(_castWidening(float, 2)), float)
    self.assertEqual(_castWidening(complex, 1.5), 1.5 + 0j)
    self.assertEqual(_castWidening(complex, True), 1 + 0j)
    for target, value in ((int, 2.0), (bool, 1), (int, 'x'), (float, '1'),
                          (float, 1 + 0j)):
      with self.subTest(target=target.__name__, value=value):
        with self.assertRaises(TypeCastException) as context:
          _castWidening(target, value)
        self.assertIs(context.exception.type_, target)
        self.assertIs(context.exception.arg, value)
        self.assertIn("'%s'" % target.__name__, str(context.exception))

  def test_order_by_cast(self) -> None:
    self.assertEqual(_orderByCast((float, int), (1, 2.0), _castWidening),
                     (2.0, 1))
    self.assertEqual(_orderByCast((float, int), (1, 2.0), typeCast),
                     (1.0, 2))
    self.assertIsNone(_orderByCast((int,), ('x',), typeCast))
    self.assertIsNone(_orderByCast((int, int), (1,), typeCast))
    self.assertEqual(_orderByCast((str, int), (1, b'a'), typeCast), ('a', 1))

  def test_more_arguments_than_declared(self) -> None:
    self.assertIsNone(_orderByInstance((int,), (1, 2)))
    self.assertIsNone(_orderByCast((int,), (1, 2), typeCast))
