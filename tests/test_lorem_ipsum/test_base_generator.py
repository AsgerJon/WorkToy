"""
TestBaseGenerator tests 'BaseGenerator' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import BaseGenerator, Clause
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import IntSampler
from . import LoremTest, Noted


class TestBaseGenerator(LoremTest):
  """
  'BaseGenerator' holds the contract of the three generators: the count
  by position, by keyword or by default, the first-word flag and its
  constructor, the refusals, the dropping of the layout on assignment,
  and the placeholder of a short count. The tests pin each of these on
  the base itself and on 'Noted', which counts the drops.
  """

  def test_defaults(self) -> None:
    gen = BaseGenerator()
    self.assertEqual(gen.charCount, 40)
    self.assertFalse(gen.isFirst)
    self.assertEqual(BaseGenerator.__truncate_below__, 15)
    self.assertIsInstance(gen, BaseObject)
    self.assertIsNone(gen.clear())

  def test_count_by_position_or_keyword(self) -> None:
    self.assertEqual(BaseGenerator(30).charCount, 30)
    self.assertEqual(BaseGenerator(charCount=30).charCount, 30)
    self.assertEqual(BaseGenerator(charCount=None).charCount, 40)
    self.assertEqual(BaseGenerator(None).charCount, 40)
    self.assertTrue(BaseGenerator.first(None).isFirst)
    self.assertEqual(BaseGenerator(0).charCount, 0)
    with self.assertRaises(TypeError):
      BaseGenerator(foo=1)
    with self.assertRaises(DispatchException) as context:
      BaseGenerator('30')
    self.assertIs(context.exception.dispatch,
                  BaseGenerator.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, ('30',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("no overload of 'BaseGenerator.__init__' accepts",
                  str(context.exception))
    self.assertIn("<str '30'>", str(context.exception))
    with self.assertRaises(DispatchException) as context:
      BaseGenerator(30, 40)
    self.assertIs(context.exception.dispatch,
                  BaseGenerator.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, (30, 40))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn('<TypeSig: [int, int]>', str(context.exception))

  def test_count_cast_and_refused(self) -> None:
    gen = BaseGenerator()
    gen.charCount = 30.0
    self.assertEqual(gen.charCount, 30)
    self.assertIs(type(gen.charCount), int)
    with self.assertRaises(TypeException) as context:
      gen.charCount = 'abc'
    self.assertEqual(context.exception.varName, 'charCount')
    self.assertEqual(context.exception.actualObject, 'abc')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'charCount' to be an instance of 'int'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      BaseGenerator(charCount='abc')
    self.assertEqual(context.exception.varName, 'charCount')
    self.assertEqual(context.exception.actualObject, 'abc')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'charCount' to be an instance of 'int'",
                  str(context.exception))
    self.assertEqual(gen.charCount, 30)

  def test_negative_count_refused(self) -> None:
    for make in (lambda: BaseGenerator(-1),
                 lambda: BaseGenerator(charCount=-1)):
      with self.subTest(make=make.__name__):
        with self.assertRaises(ValueError) as context:
          make()
        self.assertIn("A 'BaseGenerator' needs a character count of zero "
                      "or more, but received: -1", str(context.exception))
    gen = BaseGenerator(5)
    with self.assertRaises(ValueError) as context:
      gen.charCount = -5
    self.assertIn("A 'BaseGenerator' needs a character count of zero or "
                  "more, but received: -5", str(context.exception))
    self.assertEqual(gen.charCount, 5)

  def test_first(self) -> None:
    gen = BaseGenerator.first(25)
    self.assertTrue(gen.isFirst)
    self.assertEqual(gen.charCount, 25)
    self.assertTrue(BaseGenerator.first(charCount=12).isFirst)
    self.assertTrue(BaseGenerator.first().isFirst)
    self.assertIsInstance(Clause.first(20), Clause)

  def test_assignments_drop_the_layout(self) -> None:
    noted = Noted(10)
    self.assertEqual(noted.cleared, 1)
    noted.charCount = 11
    self.assertEqual(noted.cleared, 2)
    noted.isFirst = True
    self.assertEqual(noted.cleared, 3)
    noted.isFirst = True
    self.assertEqual(noted.cleared, 4)
    self.assertEqual(Noted().cleared, 0)
    self.assertEqual(Noted.first(5).cleared, 2)

  def test_short_text(self) -> None:
    expected = {
      0: '', 1: '.', 2: '..', 3: '...', 4: 'L...', 5: 'Lo...',
      11: 'Lorem Ip...', 14: 'Lorem Ipsum...', 15: 'Lorem Ipsum....',
      20: 'Lorem Ipsum.........',
    }
    for count, text in expected.items():
      with self.subTest(count=count):
        self.assertEqual(BaseGenerator(count)._shortText(), text)
        self.assertEqual(len(text), count)

  def test_random_short_texts(self) -> None:
    self.randomInteger = IntSampler(0, 60, seed=self.__sampler_seed__)
    self.randomInteger.size = 10
    for count in self.randomInteger.row:
      with self.subTest(count=count):
        text = BaseGenerator(count)._shortText()
        self.assertEqual(len(text), count)
        self.assertTrue(text.endswith('.' * min(count, 3)))
