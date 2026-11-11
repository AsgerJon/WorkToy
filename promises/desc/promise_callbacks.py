"""
PromiseCallbacks promises the notification decorators every worktoy
descriptor takes, from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.control_flow import SkipSet
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.desc import NamelessCallback


class PromiseCallbacks(TestCase):
  """
  A descriptor of worktoy takes seven decorators registering methods of
  the owning class: 'preGet' and 'onGet' around a read, 'preSet' and
  'onSet' around a write, 'preDelete' and 'onDelete' around a deletion,
  and 'setName' as the class is created. A 'preSet' receives the value as
  assigned, before any conversion; raising refuses the write, and
  raising 'SkipSet' skips it silently. An 'onSet' receives the value as
  stored, several run in the order registered, and building the default
  at the first read is no write. One method may serve several boxes, and
  a private name such as '__audit' works. The method is found by
  name on the class of the instance at each access, so a subclass
  overriding it is called instead. A method may declare fewer parameters
  than it is passed, and is called as the kind of method it is: a
  staticmethod receives the value alone. A lambda has no name to find
  and raises 'NamelessCallback'. Source: the 'BaseDescriptor' docstring
  and its example.
  """

  def test_pre_and_on_set(self) -> None:
    log = []

    class Account(BaseObject):
      balance = AttriBox[float](0.0)

      @balance.preSet
      def _checkBalance(self, value: float) -> None:
        if value < 0:
          raise ValueError('negative balance')

      @balance.onSet
      def _audit(self, value: float) -> None:
        log.append(value)

    account = Account()
    account.balance = 5
    self.assertEqual(log, [5.0])
    self.assertIs(type(log[0]), float)
    with self.assertRaises(ValueError):
      account.balance = -1
    self.assertEqual(account.balance, 5.0)

  def test_read_and_delete_callbacks(self) -> None:
    log = []

    class Lamp(BaseObject):
      level = AttriBox[int](3)

      @level.onGet
      def _read(self) -> None:
        log.append('read')

      @level.onDelete
      def _gone(self) -> None:
        log.append('deleted')

    lamp = Lamp()
    _ = lamp.level
    del lamp.level
    self.assertEqual(log, ['read', 'deleted'])

  def test_set_name(self) -> None:
    placed = []

    class Registry(BaseObject):
      entry = AttriBox[int](0)

      @entry.setName
      @classmethod
      def _register(cls, desc) -> None:
        placed.append((cls.__name__, desc))

    self.assertEqual(placed, [('Registry', vars(Registry)['entry'])])

  def test_override_in_subclass(self) -> None:
    log = []

    class Account(BaseObject):
      balance = AttriBox[int](0)

      @balance.onSet
      def _audit(self, value: int) -> None:
        log.append(('account', value))

    class Savings(Account):
      def _audit(self, value: int) -> None:
        log.append(('savings', value))

    Savings().balance = 7
    Account().balance = 3
    self.assertEqual(log, [('savings', 7), ('account', 3)])

  def test_kinds(self) -> None:
    log = []

    class Thermometer(BaseObject):
      degrees = AttriBox[float](20.0)

      @degrees.onSet
      @staticmethod
      def _record(value: float) -> None:
        log.append(value)

    Thermometer().degrees = 25
    self.assertEqual(log, [25.0])

  def test_pre_set_sees_assigned_value(self) -> None:
    log = []

    class Account(BaseObject):
      balance = AttriBox[float](0.0)

      @balance.preSet
      def _check(self, value) -> None:
        log.append(('preSet', value))
        if value == 0:
          raise SkipSet

      @balance.onSet
      def _first(self, value) -> None:
        log.append(('first', value))

      @balance.onSet
      def _second(self, value) -> None:
        log.append(('second', value))

    account = Account()
    _ = account.balance
    self.assertEqual(log, [])
    account.balance = 5
    account.balance = 0
    self.assertEqual(account.balance, 5.0)
    with self.assertRaises(TypeException):
      account.balance = 'five'
    self.assertEqual(log, [('preSet', 5), ('first', 5.0), ('second', 5.0),
                           ('preSet', 0), ('preSet', 'five')])

  def test_one_method_two_boxes(self) -> None:
    log = []

    class Rectangle(BaseObject):
      width = AttriBox[int](0)
      height = AttriBox[int](0)

      @width.onSet
      @height.onSet
      def _changed(self, value: int) -> None:
        log.append(value)

    rectangle = Rectangle()
    rectangle.width = 3
    rectangle.height = 4
    self.assertEqual(log, [3, 4])

  def test_private_name(self) -> None:
    log = []

    class Vault(BaseObject):
      gold = AttriBox[int](0)

      @gold.onSet
      def __audit(self, value: int) -> None:
        log.append(value)

    Vault().gold = 9
    self.assertEqual(log, [9])

  def test_lambda_refused(self) -> None:
    with self.assertRaises(NamelessCallback) as context:
      class Account(BaseObject):
        balance = AttriBox[int](0)
        balance.onSet(lambda self, value: None)
    e = context.exception
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.role, 'onSet')
    self.assertTrue(callable(e.callback))
