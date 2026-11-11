"""
PromiseRaiseByHand promises the exceptions of 'worktoy.waitaminute' a
project raises in its own code.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.waitaminute import WorkToyException, TypeException
from worktoy.waitaminute import MissingVariable, VariableNotNone
from worktoy.waitaminute import UnpackException, SubclassException


class PromiseRaiseByHand(TestCase):
  """
  The cross-cutting exceptions at the top of 'worktoy.waitaminute' are
  offered to projects as well, and each keeps the facts it was raised
  with as attributes, its message being for people only:
  'TypeException(name, value, *types)' for a value of the wrong type,
  'MissingVariable(instance, name, *types)' for a value still 'None',
  'VariableNotNone(name, value)' for a write-once value written twice,
  'UnpackException(*args)' for arguments with nothing to unpack, and
  'SubclassException(subClass, baseClass)' for a class that is no
  subclass of the one required. A project may base exceptions of its own
  on 'WorkToyException' in the same way, the builtin listed after it,
  and such an exception takes its message as any Python exception does.
  Source: the docstrings of these exceptions and their examples.
  """

  def test_type_exception(self) -> None:
    def setWidth(width: object) -> None:
      if not isinstance(width, (int, float)):
        raise TypeException('width', width, int, float)

    with self.assertRaises(TypeError) as context:
      setWidth('wide')
    e = context.exception
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'width')
    self.assertEqual(e.actualObject, 'wide')
    self.assertIs(e.actualType, str)
    self.assertEqual(e.expectedTypes, (int, float))

  def test_missing_variable(self) -> None:
    class Decorate:
      __wrapped__ = None

      def __call__(self) -> None:
        if self.__wrapped__ is None:
          raise MissingVariable(self, '__wrapped__', type(len))

    decorate = Decorate()
    with self.assertRaises(AttributeError) as context:
      decorate()
    e = context.exception
    self.assertIsInstance(e, MissingVariable)
    self.assertIs(e.instance, decorate)
    self.assertEqual(e.varName, '__wrapped__')
    self.assertEqual(e.expectedTypes, (type(len),))

  def test_variable_not_none(self) -> None:
    e = VariableNotNone('owner', 'Alice')
    self.assertEqual(e.name, 'owner')
    self.assertEqual(e.value, 'Alice')
    self.assertIsInstance(e, WorkToyException)

  def test_unpack_exception(self) -> None:
    e = UnpackException(1, 2)
    self.assertEqual(e.posArgs, (1, 2))
    self.assertIsInstance(e, ValueError)

  def test_subclass_exception(self) -> None:
    e = SubclassException(str, int)
    self.assertIs(e.subClass, str)
    self.assertIs(e.baseClass, int)
    self.assertIsInstance(e, TypeError)

  def test_own_exception(self) -> None:
    class BudgetExceeded(WorkToyException, ValueError):
      pass

    for family in (WorkToyException, ValueError):
      with self.subTest(family=family.__name__):
        with self.assertRaises(family):
          raise BudgetExceeded
    self.assertEqual(str(BudgetExceeded('over by 5')), 'over by 5')
