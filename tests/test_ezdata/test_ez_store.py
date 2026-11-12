"""
TestEZStore tests 'EZStore' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Alias
from worktoy.ezdata import EZStore
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import EzdataTest, Labelled, Point2D


class TestEZStore(EzdataTest):
  """
  An 'EZStore' stands at the name of a field that a data descriptor
  further along the resolution order would take over. It defines
  '__get__' alone, so the instance dictionary answers every populated
  read and takes every write; it runs only for an instance holding no
  value. The tests pin the two routes of '__get__', the placement on
  'Labelled', the field without a clash, and an 'Alias' of the field.
  """

  def test_get_by_hand(self) -> None:
    store = EZStore('label')
    self.assertIs(store.__get__(None, Labelled), store)
    labelled = Labelled('t')
    self.assertEqual(store.__get__(labelled, Labelled), 't')
    empty = Labelled.__new__(Labelled)
    with self.assertRaises(MissingVariable) as context:
      store.__get__(empty, Labelled)
    self.assertIs(context.exception.instance, empty)
    self.assertEqual(context.exception.varName, 'label')
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'Labelled.label'!")
    self.assertIsNotNone(context.exception.__cause__)

  def test_placed_where_a_descriptor_clashes(self) -> None:
    self.assertIsInstance(Labelled.__dict__['label'], EZStore)
    self.assertNotIn('count', Labelled.__dict__)
    self.assertNotIn('x', Point2D.__dict__)
    labelled = Labelled('t')
    self.assertEqual(labelled.label, 't')
    labelled.label = 'u'
    self.assertEqual(labelled.__dict__['label'], 'u')
    self.assertEqual(Labelled.__new__(Labelled).__dict__, {})
    with self.assertRaises(MissingVariable) as context:
      _ = Labelled.__new__(Labelled).label
    self.assertIsInstance(context.exception.instance, Labelled)
    self.assertEqual(context.exception.varName, 'label')
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'Labelled.label'!")

  def test_alias_reads_through_the_store(self) -> None:
    class Named(Labelled):
      same = Alias('label')

    named = Named('t')
    self.assertEqual(named.same, 't')
    with self.assertRaises(ReadOnlyError) as context:
      named.same = 'u'
    self.assertIs(context.exception.instance, named)
    self.assertIs(context.exception.desc, Named.__dict__['same'])
    self.assertEqual(context.exception.newVal, 'u')
    self.assertIn("read-only attribute 'Named.same' with new value: 'u'",
                  str(context.exception))
    with self.assertRaises(ProtectedError) as context:
      del named.same
    self.assertIs(context.exception.instance, named)
    self.assertIs(context.exception.desc, Named.__dict__['same'])
    self.assertIsNone(context.exception.oldVal)
    self.assertIn("protected attribute 'Named.same'",
                  str(context.exception))
    self.assertEqual(named.label, 't')

  def test_random_values(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertEqual(Labelled(word).label, word)
        self.assertEqual(Labelled(label=word).__dict__['label'], word)
