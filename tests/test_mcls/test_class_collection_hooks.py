"""
TestClassCollectionHooks tests the class hooks of 'AbstractMetaclass'
from 'worktoy.mcls' that make a class iterable, sized, searchable and
truthy.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable, Iterator, Sized, Container
from collections.abc import Collection

from worktoy.mcls import BaseObject
from . import MclsTest, Roster, Clock, Ledger


class TestClassCollectionHooks(MclsTest):
  """
  A class defining '__class_iter__' is an iterable, one returning
  itself from it and defining '__class_next__' is an iterator, and
  'bool', 'in' and 'len' consult '__class_bool__', '__class_contains__'
  and '__class_len__'. Without them, 'bool' answers from the length or
  'True', 'in' searches the class by iterating it, and 'len' fails, as
  Python does for a plain class; nothing counts a class by iterating
  it. A class defining no hook fails as a plain class does, whatever
  'collections.abc' reports. The tests pin each route on the fixtures
  of the folder, with the plain twins of 'Roster' and 'Clock' beside
  them.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    Roster.members = []
    Clock.ticks = []
    Ledger.entries.clear()

  def test_iter(self) -> None:
    Roster.members = ['a', 'b']
    self.assertEqual(list(Roster), ['a', 'b'])
    self.assertEqual([*iter(Roster)], ['a', 'b'])
    with self.assertRaises(TypeError) as context:
      iter(BaseObject)
    self.assertEqual(str(context.exception),
                     "type object 'BaseObject' is not iterable")

  def test_next(self) -> None:
    Clock.ticks = [1, 2]
    self.assertEqual(next(Clock), 1)
    self.assertEqual(next(Clock), 2)
    with self.assertRaises(StopIteration) as context:
      next(Clock)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(TypeError) as context:
      next(Roster)
    self.assertEqual(str(context.exception),
                     "type object 'Roster' is not an iterator")

  def test_own_iterator(self) -> None:
    Clock.ticks = [1, 2, 3]
    self.assertIs(iter(Clock), Clock)
    with self.assertRaises(TypeError) as context:
      len(Clock)
    self.assertEqual(str(context.exception),
                     "type object 'Clock' has no len()")
    self.assertTrue(Clock)
    self.assertEqual(Clock.ticks, [1, 2, 3])
    self.assertEqual(list(Clock), [1, 2, 3])
    self.assertEqual(list(Clock), [])
    Clock.ticks = [1, 2, 3]
    self.assertIn(2, Clock)
    self.assertEqual(Clock.ticks, [3])

  def test_matches_plain_classes(self) -> None:
    class PlainIterable:
      def __iter__(self) -> iter:
        return iter(['a', 'b'])

    class PlainIterator:
      def __init__(self) -> None:
        self.ticks = [1, 2, 3]

      def __iter__(self) -> PlainIterator:
        return self

      def __next__(self) -> int:
        if self.ticks:
          return self.ticks.pop(0)
        raise StopIteration

    Roster.members = ['a', 'b']
    Clock.ticks = [1, 2, 3]
    plainIterator = PlainIterator()
    pairs = ((PlainIterable(), Roster), (plainIterator, Clock))
    for plain, cls in pairs:
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(TypeError):
          len(plain)
        with self.assertRaises(TypeError) as context:
          len(cls)
        self.assertEqual(str(context.exception),
                         "type object '%s' has no len()" % cls.__name__)
        self.assertTrue(plain)
        self.assertTrue(cls)
        self.assertEqual(list(plain), list(cls))
    self.assertEqual(plainIterator.ticks, Clock.ticks)

  def test_bool(self) -> None:
    class Flagged(BaseObject):
      flag = False

      @classmethod
      def __class_bool__(cls) -> bool:
        return cls.flag

    self.assertFalse(Flagged)
    Flagged.flag = True
    self.assertTrue(Flagged)
    self.assertFalse(Ledger)
    Ledger.entries['k'] = 1
    self.assertTrue(Ledger)
    self.assertTrue(Roster)
    Clock.ticks = [1]
    self.assertTrue(Clock)
    self.assertEqual(Clock.ticks, [1])
    self.assertTrue(BaseObject)

  def test_contains(self) -> None:
    Ledger.entries['k'] = 1
    self.assertIn('k', Ledger)
    self.assertNotIn('q', Ledger)
    Roster.members = ['a', 'b']
    self.assertIn('b', Roster)
    self.assertNotIn('c', Roster)
    Roster.members = ['b']
    self.assertNotIn('a', Roster)
    self.assertNotIn('c', Roster)
    with self.assertRaises(TypeError) as context:
      _ = 'x' in BaseObject
    self.assertEqual(str(context.exception),
                     "argument of type 'BaseObject' is not iterable")

  def test_contains_compares_by_equality(self) -> None:
    Roster.members = [1.0]
    self.assertIn(1, Roster)
    self.assertIn(True, Roster)

  def test_len(self) -> None:
    Ledger.entries['k'] = 1
    Ledger.entries['j'] = 2
    self.assertEqual(len(Ledger), 2)
    Roster.members = ['a', 'b', 'c']
    with self.assertRaises(TypeError) as context:
      len(Roster)
    self.assertEqual(str(context.exception),
                     "type object 'Roster' has no len()")
    self.assertEqual(Roster.members, ['a', 'b', 'c'])
    with self.assertRaises(TypeError) as context:
      len(BaseObject)
    self.assertEqual(str(context.exception),
                     "type object 'BaseObject' has no len()")

  def test_abc_report_is_wrong_by_design(self) -> None:
    class Plain(BaseObject):
      pass

    for abc in (Iterable, Iterator, Sized, Container, Collection):
      with self.subTest(abc=abc.__name__):
        self.assertIsInstance(Plain, abc)
    with self.assertRaises(TypeError) as context:
      iter(Plain)
    self.assertEqual(str(context.exception),
                     "type object 'Plain' is not iterable")
    with self.assertRaises(TypeError) as context:
      len(Plain)
    self.assertEqual(str(context.exception),
                     "type object 'Plain' has no len()")

  def test_random_members(self) -> None:
    self.randomWord.size = 7
    words = [*self.randomWord.row]
    Roster.members = words
    self.assertEqual(list(Roster), words)
    for word in words:
      with self.subTest(word=word):
        self.assertIn(word, Roster)
    self.assertNotIn(''.join(words), Roster)
