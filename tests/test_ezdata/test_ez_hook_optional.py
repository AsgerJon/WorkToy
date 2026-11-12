"""
TestEZHookOptional tests how 'EZHook' from 'worktoy.ezdata' settles the
optional names of a dataclass.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.dispatch import overload, Dispatcher
from worktoy.ezdata import EZData, EZField, EZHook
from . import EzdataTest, Point2D, Circle, Labelled, Reporter


class TestEZHookOptional(EzdataTest):
  """
  The optional names, '__field_pairs__', 'asDict', 'asTuple',
  'replace', '__repr__', '__str__' and '__match_args__', are generated
  only where neither the body nor a base supplies one: the body's own
  wins, then the first hand-written one along the bases, dataclass and
  plain alike, past what EZData generated. The tests pin each route and
  the two helpers.
  """

  def test_body_wins(self) -> None:
    class A(EZData):
      x = 1

      def asDict(self) -> dict:
        return {'own': self.x}

      @overload()
      def asTuple(self) -> tuple:
        return ('overloaded',)

    self.assertEqual(A(2).asDict(), {'own': 2})
    self.assertIsInstance(A.__dict__['asTuple'], Dispatcher)
    self.assertEqual(A(2).asTuple(), ('overloaded',))
    self.assertNotIn('asDict', A.__ez_generated__)
    self.assertNotIn('asTuple', A.__ez_generated__)
    self.assertIn('replace', A.__ez_generated__)

  def test_replace_reads_the_fields_past_an_own_as_dict(self) -> None:
    class Wrapped(EZData):
      inner = EZField[Point2D]()
      scale = 1.0

      def asDict(self) -> dict:
        nested = self.inner.asDict()
        return {'inner': nested, 'scale': self.scale, 'extra': True}

    wrapped = Wrapped(Point2D(1, 2), 3)
    self.assertEqual(wrapped.asDict()['inner'], {'x': 1.0, 'y': 2.0})
    self.assertIn('replace', Wrapped.__ez_generated__)
    grown = wrapped.replace(scale=5)
    self.assertIsNot(grown, wrapped)
    self.assertEqual(grown.scale, 5.0)
    self.assertIs(grown.inner, wrapped.inner)
    self.assertEqual(wrapped.scale, 3.0)
    self.assertEqual(wrapped.replace().asTuple(), wrapped.asTuple())

  def test_plain_base_wins(self) -> None:
    self.assertIs(Labelled.__dict__['asDict'], Reporter.__dict__['asDict'])
    self.assertIs(Labelled.__dict__['__repr__'],
                  Reporter.__dict__['__repr__'])
    self.assertEqual(Labelled('t').asDict(), {'reported': True})
    self.assertEqual(repr(Labelled('t')), 'Reporter!')
    self.assertEqual(str(Labelled('t')), '<Labelled: label=\'t\', count=1>')
    self.assertNotIn('asDict', Labelled.__ez_generated__)
    self.assertIn('__str__', Labelled.__ez_generated__)
    self.assertEqual(len(Labelled('t')), 2)
    self.assertEqual(Reporter.__len__(Labelled('t')), 99)

  def test_dataclass_base_wins_past_generated(self) -> None:
    class A(EZData):
      x = 1

      def asTuple(self) -> tuple:
        return ('hand',)

    class B(A):
      y = 2

    self.assertIs(B.__dict__['asTuple'], A.__dict__['asTuple'])
    self.assertEqual(B().asTuple(), ('hand',))
    self.assertIsNot(B.__dict__['__repr__'], A.__dict__['__repr__'])
    self.assertIn('__repr__', B.__ez_generated__)
    self.assertNotIn('asTuple', B.__ez_generated__)
    self.assertEqual(repr(B()), 'B(1, 2)')

  def test_match_args(self) -> None:
    self.assertEqual(Point2D.__match_args__, ('x', 'y'))
    self.assertEqual(Circle.__match_args__, ())

    class A(EZData, kwOnly=True):
      x = 1
      __match_args__ = ('x',)

    class B(A, kwOnly=True):
      y = 2

    self.assertEqual(A.__match_args__, ('x',))
    self.assertEqual(B.__match_args__, ('x',))
    self.assertNotIn('__match_args__', B.__ez_generated__)
    self.assertEqual(EZHook.matchArgsFactory(Point2D.__ez_fields__, True),
                     ())
    self.assertEqual(EZHook.matchArgsFactory(Point2D.__ez_fields__, False),
                     ('x', 'y'))

  def test_field_pairs_drive_the_texts(self) -> None:
    class A(EZData, kwOnly=True):
      x = 1

      def __field_pairs__(self) -> list:
        return ['custom']

    self.assertEqual(str(A()), '<A: custom>')
    self.assertEqual(repr(A()), 'A(custom)')
    self.assertEqual(Point2D(1, 2).__field_pairs__(), ['x=1.0', 'y=2.0'])

  def test_find_hand_written(self) -> None:
    order = [Labelled, Reporter, EZData, Object, object]
    self.assertEqual(EZHook._findHandWritten('asDict', order),
                     (True, Reporter.__dict__['asDict']))
    self.assertEqual(EZHook._findHandWritten('asDict', [Point2D, EZData]),
                     (False, None))
    self.assertEqual(EZHook._findHandWritten('__repr__', [object]),
                     (False, None))
    self.assertEqual(EZHook._findHandWritten('count', [Reporter]),
                     (True, 99))

  def test_settle_optional(self) -> None:
    compiled = {'asDict': 'own'}
    factories = {'asDict': lambda: 'gen', 'asTuple': lambda: 'gen2'}
    generated = EZHook._settleOptional(compiled, factories, [Reporter])
    self.assertEqual(generated, frozenset(('asTuple',)))
    self.assertEqual(compiled, {'asDict': 'own', 'asTuple': 'gen2'})
    compiled = {}
    generated = EZHook._settleOptional(compiled, factories, [Reporter])
    self.assertEqual(generated, frozenset(('asTuple',)))
    self.assertIs(compiled['asDict'], Reporter.__dict__['asDict'])
    hook = EZHook()
    keys = [*hook._optionalFactories({}, False)]
    self.assertEqual(keys, [
      '__field_pairs__', 'asDict', 'asTuple', 'replace', '__repr__',
      '__str__', '__match_args__',
    ])
    factory = hook._optionalFactories({'a': 1}, True)['__match_args__']
    self.assertEqual(factory(), ())

  def test_random_hand_written(self) -> None:
    self.randomWord.size = 4
    for word in self.randomWord.row:
      def asDict(self, word=word) -> dict:
        return {'word': word}

      cls = type('R', (EZData,), {'x': 1, 'asDict': asDict})
      with self.subTest(word=word):
        self.assertEqual(cls().asDict(), {'word': word})
        self.assertNotIn('asDict', cls.__ez_generated__)

  def test_hand_written_found_past_generated_and_plain_bases(self) -> None:
    class Loud:
      def __repr__(self) -> str:
        return 'loud'

    class Quiet:
      tag = 'quiet'

    class After(Point2D, Loud):
      pass

    class Later(Point2D, Quiet, Loud):
      pass

    self.assertEqual(repr(After()), 'loud')
    self.assertEqual(repr(Later()), 'loud')
    self.assertEqual(Later.tag, 'quiet')
