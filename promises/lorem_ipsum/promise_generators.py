"""
PromiseGenerators promises 'Clause', 'Sentence' and 'Paragraph' from
'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from unittest import TestCase

from worktoy.lorem_ipsum import Clause, Sentence, Paragraph


class PromiseGenerators(TestCase):
  """
  A generator gives placeholder text of exactly the character count it
  is given, by position, as 'charCount' or not at all for 40, and
  'str', 'realize' and 'len' agree on it. A 'Clause' is words joined by
  single spaces, without punctuation; a 'Sentence' is clauses joined by
  ', ', its first letter capital and its last character a period; a
  'Paragraph' is sentences joined by single spaces. A paragraph opens
  with 'Lorem ipsum' unless 'isFirst' is set to False; a clause or a
  sentence opens with it only when made by 'first', and a first clause
  too short for the lead-in and a word comes out as a placeholder of the
  same count, as 'Lorem ipsum....' at fifteen; a subclass of 'Clause'
  rebinding '__lead_in__' opens with words of its own. A text is made at
  the first read and kept: assigning 'charCount' or 'isFirst', or
  calling 'reset()', makes a new one. The draws come from Python's
  'random', so 'random.seed' repeats a text. A negative count raises
  'ValueError', and so does a clause too short for any word; a keyword
  other than 'charCount' raises 'TypeError'. A generator given another
  of its kind copies it, the text the other has realized included.
  Source: the docstrings of 'BaseGenerator',
  'Clause', 'Sentence' and 'Paragraph'.
  """

  def test_exact_count(self) -> None:
    for count in (12, 30, 47, 80, 133):
      for generator in (Clause, Sentence, Paragraph):
        with self.subTest(generator=generator.__name__, count=count):
          text = generator(count)
          self.assertEqual(len(str(text)), count)
          self.assertEqual(text.realize(), str(text))
          self.assertEqual(len(text), count)

  def test_count_spellings(self) -> None:
    self.assertEqual(len(str(Clause(charCount=25))), 25)
    self.assertEqual(len(str(Clause())), 40)
    self.assertEqual(len(str(Clause(None))), 40)

  def test_clause(self) -> None:
    for _ in range(20):
      clause = Clause(40)
      words = str(clause).split(' ')
      self.assertEqual(list(clause), words)
      for word in words:
        self.assertTrue(word.isalpha())

  def test_sentence(self) -> None:
    for _ in range(20):
      text = str(Sentence(70))
      self.assertTrue(text[0].isupper())
      self.assertTrue(text.endswith('.'))

  def test_lead_in(self) -> None:
    self.assertTrue(str(Paragraph(200)).startswith('Lorem ipsum'))
    self.assertTrue(str(Clause.first(40)).startswith('Lorem ipsum'))
    self.assertTrue(str(Sentence.first(60)).startswith('Lorem ipsum'))
    self.assertEqual(str(Clause.first(15)), 'Lorem ipsum....')
    for _ in range(20):
      self.assertFalse(str(Clause(40)).startswith('Lorem ipsum'))

  def test_paragraph_not_first(self) -> None:
    paragraph = Paragraph(150)
    paragraph.isFirst = False
    for _ in range(20):
      paragraph.charCount = 150
      self.assertEqual(len(str(paragraph)), 150)

  def test_text_kept_until_reset(self) -> None:
    clause = Clause(40)
    first = str(clause)
    self.assertEqual(str(clause), first)
    clause.reset()
    self.assertEqual(len(str(clause)), 40)

  def test_seeded(self) -> None:
    random.seed(7)
    first = str(Paragraph(200))
    random.seed(7)
    self.assertEqual(str(Paragraph(200)), first)

  def test_is_first_flip(self) -> None:
    paragraph = Paragraph(150)
    self.assertTrue(str(paragraph).startswith('Lorem ipsum'))
    paragraph.isFirst = False
    for _ in range(20):
      paragraph.reset()
      self.assertFalse(str(paragraph).startswith('Lorem ipsum'))
    self.assertFalse(Clause(40).isFirst)

  def test_own_lead_in(self) -> None:
    class Greeting(Clause):
      __lead_in__ = ('Hello', 'world')

    for _ in range(10):
      text = str(Greeting.first(30))
      self.assertTrue(text.startswith('Hello world '))
      self.assertEqual(len(text), 30)

  def test_new_count(self) -> None:
    clause = Clause(30)
    _ = str(clause)
    clause.charCount = 50
    self.assertEqual(len(str(clause)), 50)

  def test_refusals(self) -> None:
    with self.assertRaises(ValueError):
      Clause(-1)
    with self.assertRaises(ValueError):
      str(Clause(1))
    with self.assertRaises(TypeError):
      Clause(size=30)

  def test_copy(self) -> None:
    for generator in (Clause, Sentence, Paragraph):
      with self.subTest(generator=generator.__name__):
        original = generator(60)
        text = str(original)
        self.assertEqual(str(generator(original)), text)
