"""
TestEZFieldConstruct tests how an 'EZField' from 'worktoy.ezdata' builds
its default value.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from fractions import Fraction

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException
from . import EzdataTest, Bag, Point2D


class TestEZFieldConstruct(EzdataTest):
  """
  A default is a recipe: a lone value of the field type is deep-copied,
  a lone value a text or number type casts is cast or refused, any
  other lone value is the one argument of the constructor, and several
  arguments, keywords or none call the constructor. The result must be
  an instance of the field type. The tests pin each route of
  '_construct', the two helpers, and 'defaultValue' building afresh.
  """

  @staticmethod
  def unbuiltText(name: str, typeName: str) -> str:
    """The refusal of a default the constructor would not build."""
    spec = """The default of the field '%s' could not be built: '%s'
    refused the call the declaration describes. Declare the field with
    arguments '%s' accepts, as 'EZField[%s](...)', or give the field a
    value when the instance is made."""
    info = spec % (name, typeName, typeName, typeName)
    return str.join(' ', info.split())

  def test_lone_instance_is_copied(self) -> None:
    seed = [1, [2]]
    field = EZField[list](seed)
    first = field.defaultValue
    second = field.defaultValue
    self.assertEqual(first, seed)
    self.assertIsNot(first, seed)
    self.assertIsNot(first, second)
    self.assertIsNot(first[1], seed[1])
    self.assertIsNot(Bag().seeds, Bag().seeds)
    point = Point2D(1.0, 2.0)
    copied = EZField[Point2D](point).defaultValue
    self.assertEqual(copied, point)
    self.assertIsNot(copied, point)

  def test_lone_value_is_cast(self) -> None:
    self.assertEqual(EZField[int](3.0).defaultValue, 3)
    self.assertIs(type(EZField[int](3.0).defaultValue), int)
    self.assertEqual(EZField[float](2).defaultValue, 2.0)
    self.assertEqual(EZField[complex](1).defaultValue, 1 + 0j)
    with self.assertRaises(TypeException) as context:
      _ = EZField[int]('x').defaultValue
    exception = context.exception
    self.assertEqual(exception.varName, 'defaultValue')
    self.assertEqual(exception.actualObject, 'x')
    self.assertIs(exception.actualType, str)
    self.assertEqual(exception.expectedTypes, (int,))
    self.assertIsNotNone(exception.__cause__)
    self.assertIn("'defaultValue' to be an instance of 'int'",
                  str(exception))

  def test_bool_stays_bool(self) -> None:
    value = EZField[int](True).defaultValue
    self.assertIs(value, True)
    self.assertIsInstance(value, int)

  def test_lone_other_value_is_the_argument(self) -> None:
    self.assertEqual(EZField[Fraction]('1/2').defaultValue, Fraction(1, 2))
    self.assertEqual(EZField[list]('abc').defaultValue, ['a', 'b', 'c'])
    self.assertEqual(EZField[tuple]('ab').defaultValue, ('a', 'b'))
    with self.assertRaises(TypeException) as context:
      _ = EZField[Fraction]('junk').defaultValue
    self.assertEqual(context.exception.varName, 'defaultValue')
    self.assertEqual(context.exception.actualObject, 'junk')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (Fraction,))
    self.assertIn("'defaultValue' to be an instance of 'Fraction'",
                  str(context.exception))

  def test_several_arguments_call_the_constructor(self) -> None:
    self.assertEqual(EZField[complex](1, 2).defaultValue, 1 + 2j)
    self.assertEqual(EZField[dict](a=1).defaultValue, {'a': 1})
    self.assertEqual(EZField[dict]([('b', 2)], c=3).defaultValue,
                     {'b': 2, 'c': 3})
    self.assertEqual(EZField[list]().defaultValue, [])
    self.assertEqual(EZField[int]().defaultValue, 0)
    with self.assertRaises(TypeError) as context:
      _ = EZField[int](1, 2, 3).defaultValue
    self.assertIs(type(context.exception), TypeError)
    self.assertEqual(str(context.exception),
                     self.unbuiltText('defaultValue', 'int'))
    self.assertIsInstance(context.exception.__cause__, TypeError)
    with self.assertRaises(TypeError) as context:
      _ = EZField[int]('!', 10).defaultValue
    self.assertIs(type(context.exception), TypeError)
    self.assertEqual(str(context.exception),
                     self.unbuiltText('defaultValue', 'int'))
    self.assertIsInstance(context.exception.__cause__, ValueError)

  def test_keyword_beside_one_value_is_a_call(self) -> None:
    #  One value and a keyword are the arguments of a call, not a lone
    #  value, so the refusal does not report the value as of a wrong type.
    with self.assertRaises(TypeError) as context:
      _ = EZField[float](1.0, digits=2).defaultValue
    self.assertIs(type(context.exception), TypeError)
    self.assertEqual(str(context.exception),
                     self.unbuiltText('defaultValue', 'float'))
    self.assertIsInstance(context.exception.__cause__, TypeError)

  def test_constructor_returning_something_else(self) -> None:
    class Weird:
      def __new__(cls, *args) -> int:
        return 5

    with self.assertRaises(TypeException) as context:
      _ = EZField[Weird]().defaultValue
    self.assertEqual(context.exception.varName, 'defaultValue')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Weird,))
    self.assertIn("'defaultValue' to be an instance of 'Weird'",
                  str(context.exception))

  def test_uncopyable_default_refused(self) -> None:
    lock = threading.Lock()
    with self.assertRaises(TypeError) as context:
      _ = EZField[type(lock)](lock).defaultValue
    self.assertIn('cannot be copied', str(context.exception))
    self.assertIn("'defaultValue'", str(context.exception))
    self.assertIsNotNone(context.exception.__cause__)

  def test_helpers_by_hand(self) -> None:
    copied = EZField._copyValue(list, 'n', [1])
    self.assertEqual(copied, [1])
    self.assertEqual(EZField._castValue(int, 'n', 2.0), 2)
    self.assertEqual(EZField._construct(str, 'n', ('s',), {}), 's')
    self.assertEqual(EZField._construct(str, 'n', (), {}), '')
    with self.assertRaises(TypeException) as context:
      EZField._castValue(int, 'named', 'x')
    self.assertEqual(context.exception.varName, 'named')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'named' to be an instance of 'int'",
                  str(context.exception))

  def test_default_named_after_the_field(self) -> None:
    class Owner(Point2D):
      seeds = EZField[int]('x')

    with self.assertRaises(TypeException) as context:
      _ = Owner()
    self.assertEqual(context.exception.varName, 'seeds')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'seeds' to be an instance of 'int'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      _ = Owner.__ez_fields__['seeds'].defaultValue
    self.assertEqual(context.exception.varName, 'seeds')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'seeds' to be an instance of 'int'",
                  str(context.exception))

  def test_random_defaults(self) -> None:
    self.randomInteger.size = 6
    self.randomFloat.size = 6
    for n, x in zip(self.randomInteger.row, self.randomFloat.row):
      with self.subTest(n=n, x=x):
        self.assertEqual(EZField[int](n).defaultValue, n)
        self.assertEqual(EZField[float](n).defaultValue, float(n))
        self.assertEqual(EZField[float](x).defaultValue, x)
        self.assertEqual(EZField[complex](x, n).defaultValue,
                         complex(x, n))

  def test_constructor_refused_without_arguments(self) -> None:
    class Needy:
      def __init__(self, n: int) -> None:
        self.n = n

    class Owner(EZData):
      need = EZField[Needy]()

    with self.assertRaises(TypeError) as context:
      Owner()
    self.assertIs(type(context.exception), TypeError)
    self.assertEqual(str(context.exception),
                     self.unbuiltText('need', 'Needy'))
    self.assertIsInstance(context.exception.__cause__, TypeError)
    self.assertEqual(Owner(Needy(1)).need.n, 1)
