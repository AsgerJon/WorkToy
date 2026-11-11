"""
TestKee tests 'Kee' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.keenum import Kee, KeeNum
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import VariableNotNone, DeprecatedPromise
from worktoy.waitaminute.keenum import KeeCaseException
from . import KeenumTest, WeekDay


class TestKee(KeenumTest):
  """
  A 'Kee' declares one member: it carries the value type and the
  constructor arguments as a box does, builds the value at the first
  read, and receives its name from the namespace and its index from the
  metaclass, each once. The tests pin the value, the two settings and
  their refusals, the placement outside an enumeration, the text, the
  integer, the pickling and the clone.
  """

  def test_value_built_once(self) -> None:
    kee = Kee[list]([1, 2])
    self.assertFalse(kee.__value_built__)
    first = kee.value
    self.assertEqual(first, [1, 2])
    self.assertTrue(kee.__value_built__)
    self.assertIs(kee.value, first)
    self.assertIs(kee.getValue(), first)

  def test_none_is_a_value(self) -> None:
    kee = Kee[object](None)
    self.assertIsNone(kee.value)
    self.assertTrue(kee.__value_built__)
    self.assertIsNone(kee.value)

  def test_written_value_honoured(self) -> None:
    kee = Kee[int](1)
    object.__setattr__(kee, '__field_value__', 7)
    self.assertEqual(kee.value, 7)
    self.assertFalse(kee.__value_built__)

  def test_value_of_wrong_type_refused(self) -> None:
    kee = Kee[int](1)
    object.__setattr__(kee, '__field_value__', 'seven')
    with self.assertRaises(TypeException) as context:
      _ = kee.value
    self.assertEqual(context.exception.varName, '__field_value__')
    self.assertEqual(context.exception.actualObject, 'seven')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'__field_value__'", str(context.exception))
    self.assertIn("'int'", str(context.exception))
    with self.assertRaises(RecursionError) as context:
      Kee[int](1).getValue(_recursion=True)
    self.assertEqual(context.exception.args, ())

  def test_name_and_index(self) -> None:
    kee = Kee[int](1)
    with self.assertRaises(MissingVariable) as context:
      _ = kee.name
    self.assertIs(context.exception.instance, kee)
    self.assertEqual(context.exception.varName, '__num_name__')
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(str(context.exception),
                     "Missing 'Kee.__num_name__: str'!")
    with self.assertWarns(DeprecatedPromise):
      with self.assertRaises(MissingVariable) as context:
        _ = kee.index
    self.assertIs(context.exception.instance, kee)
    self.assertEqual(context.exception.varName, '__num_index__')
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertEqual(str(context.exception),
                     "Missing 'Kee.__num_index__: int'!")
    kee.name = 'RED'
    with self.assertWarns(DeprecatedPromise):
      kee.index = 3
    self.assertEqual(kee.name, 'RED')
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(kee.index, 3)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(int(kee), 3)
    with self.assertRaises(VariableNotNone) as context:
      kee.name = 'BLUE'
    self.assertEqual(context.exception.name, 'name')
    self.assertEqual(context.exception.value, 'RED')
    self.assertIn("'RED' at name 'name'", str(context.exception))
    with self.assertWarns(DeprecatedPromise), \
        self.assertRaises(VariableNotNone) as context:
      kee.index = 4
    self.assertEqual(context.exception.name, 'index')
    self.assertEqual(context.exception.value, 3)
    self.assertIn("'3' at name 'index'", str(context.exception))

  def test_empty_parentheses_take_the_name(self) -> None:
    class Tag(str):
      pass

    class Rgb(KeeNum):
      RED = Kee[str]()
      GREEN = Kee[str]('verde')
      BLUE = Kee[str](object='azul')

    class Labels(KeeNum):
      HOT = Kee[Tag]()

    class Count(KeeNum):
      ZERO = Kee[int]()

    self.assertEqual(Rgb.RED.value, 'RED')
    self.assertEqual(Rgb.GREEN.value, 'verde')
    self.assertEqual(Rgb.BLUE.value, 'azul')
    self.assertIs(Rgb('RED'), Rgb.RED)
    self.assertEqual(Labels.HOT.value, 'HOT')
    self.assertIs(type(Labels.HOT.value), Tag)
    self.assertEqual(Count.ZERO.value, 0)
    unnamed = Kee[str]()
    with self.assertRaises(MissingVariable) as context:
      _ = unnamed.value
    self.assertIs(context.exception.instance, unnamed)
    self.assertEqual(context.exception.varName, '__num_name__')
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(str(context.exception),
                     "Missing 'Kee.__num_name__: str'!")

  def test_name_must_be_upper_case(self) -> None:
    kee = Kee[int](1)
    for name in ('red', 'Red', 'rED', 'red_one'):
      with self.subTest(name=name):
        with self.assertRaises(KeeCaseException) as context:
          kee.name = name
        self.assertEqual(context.exception.name, name)
        self.assertIn(name, str(context.exception))
    kee.name = 'RED_ONE'
    self.assertEqual(kee.name, 'RED_ONE')

  def test_index_must_be_an_int(self) -> None:
    kee = Kee[int](1)
    with self.assertWarns(DeprecatedPromise), \
        self.assertRaises(TypeException) as context:
      kee.index = '3'
    self.assertEqual(context.exception.varName, 'index')
    self.assertEqual(context.exception.actualObject, '3')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'index'", str(context.exception))
    self.assertIn("'int'", str(context.exception))

  def test_settings_of_wrong_type_refused(self) -> None:
    kee = Kee[int](1)
    object.__setattr__(kee, '__num_name__', 5)
    object.__setattr__(kee, '__num_index__', 'x')
    with self.assertRaises(TypeException) as context:
      _ = kee.name
    self.assertEqual(context.exception.varName, '__num_name__')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__num_name__'", str(context.exception))
    with self.assertWarns(DeprecatedPromise), \
        self.assertRaises(TypeException) as context:
      _ = kee.index
    self.assertEqual(context.exception.varName, '__num_index__')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'__num_index__'", str(context.exception))

  def test_placed_only_in_an_enumeration(self) -> None:
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        RED = Kee[int](1)

    exception = context.exception.__cause__ or context.exception
    self.assertIn("'Plain' is no enumeration", str(exception))
    self.assertIn("'RED'", str(exception))
    kee = Kee[int](1)
    with self.assertRaises(TypeError) as context:
      kee.__set_name__(int, 'RED')
    self.assertIn("'int' is no enumeration", str(context.exception))
    self.assertIn("'RED'", str(context.exception))

  def test_placed_kee(self) -> None:
    kee = WeekDay.MONDAY.kee
    self.assertIsInstance(kee, Kee)
    self.assertIs(kee.getFieldOwner(), WeekDay)
    self.assertEqual(kee.getFieldName(), 'MONDAY')
    self.assertEqual(kee.name, 'MONDAY')
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(kee.index, 0)
    self.assertEqual(kee.value, 'mandag')
    self.assertIs(kee.getFieldType(), str)

  def test_text(self) -> None:
    kee = Kee[int](1)
    self.assertEqual(str(kee), '<Kee member: - N/A ->')
    kee.name = 'RED'
    self.assertEqual(str(kee), '<Kee member: RED>')
    self.assertEqual(repr(kee), '<Kee member: RED>')
    self.assertEqual(str(WeekDay.FRIDAY.kee), '<Kee member: FRIDAY>')

  def test_pickle(self) -> None:
    placed = WeekDay.SUNDAY.kee
    self.assertIs(pickle.loads(pickle.dumps(placed)), placed)
    loose = Kee[int](4)
    loose.name = 'FOUR'
    loaded = pickle.loads(pickle.dumps(loose))
    self.assertIsNot(loaded, loose)
    self.assertIsInstance(loaded, Kee)
    self.assertIs(loaded.getFieldType(), int)
    self.assertEqual(loaded.getPosArgs(), (4,))
    self.assertEqual(loaded.name, 'FOUR')
    self.assertEqual(loaded.value, 4)

  def test_clone(self) -> None:
    kee = Kee[int](4, )
    kee.name = 'FOUR'
    with self.assertWarns(DeprecatedPromise):
      kee.index = 2
    cloned = kee.clone()
    self.assertIsNot(cloned, kee)
    self.assertIs(type(cloned), Kee)
    self.assertIs(cloned.getFieldType(), int)
    self.assertEqual(cloned.getPosArgs(), (4,))
    self.assertEqual(cloned.name, 'FOUR')
    with self.assertWarns(DeprecatedPromise), \
        self.assertRaises(MissingVariable) as context:
      _ = cloned.index
    self.assertIs(context.exception.instance, cloned)
    self.assertEqual(context.exception.varName, '__num_index__')
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertEqual(str(context.exception),
                     "Missing 'Kee.__num_index__: int'!")
    with self.assertWarns(DeprecatedPromise):
      cloned.index = 0
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(cloned.index, 0)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(kee.index, 2)

  def test_subclass_of_kee(self) -> None:
    class Loud(Kee):
      def shout(self) -> str:
        return self.name.upper()

    class Volume(KeeNum):
      SOFT = Loud[int](1)
      HARD = Loud[int](2)

    self.assertIsInstance(Volume.SOFT.kee, Loud)
    self.assertEqual(Volume.HARD.kee.shout(), 'HARD')
    self.assertIs(type(Volume.SOFT.kee.clone()), Loud)

  def test_random_names(self) -> None:
    self.randomWord.size = 6
    for word in self.randomWord.row:
      kee = Kee[str](word)
      kee.name = word.upper()
      with self.subTest(word=word):
        self.assertEqual(kee.value, word)
        self.assertEqual(str(kee), '<Kee member: %s>' % word.upper())
