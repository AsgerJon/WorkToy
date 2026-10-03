"""
TestShortSentenceViews subclasses 'LoremIpsumTest' and pins that a
'Sentence' of fewer than fifteen characters holds the 'Lorem Ipsum...'
placeholder as its one clause, so that 'str()', 'len()', 'repr()',
iteration and 'clausesArray' all show the same text of exactly
'charCount' characters. The rendering used to come from the placeholder
while the other views laid out a real clause the clause distribution
could not make shorter than twelve characters, so a caption of ten
characters rendered 'Lorem I...' and iterated 'Ipsimus amet.'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Sentence, Paragraph, Clause

from . import LoremIpsumTest


class Caption:
  """
  Caption is a line under a picture, laid out to fit a width in
  characters.
  """

  def __init__(self, width: int) -> None:
    self.text = Sentence(width)

  def render(self) -> str:
    return str(self.text)

  def wordCount(self) -> int:
    return sum(len(clause.wordsArray) for clause in self.text)


class TestShortSentenceViews(LoremIpsumTest):
  """
  TestShortSentenceViews provides tests for the views of a short
  'Sentence'.
  """

  placeholders = {
    0 : '',
    2 : '..',
    3 : '...',
    8 : 'Lorem...',
    10: 'Lorem I...',
    14: 'Lorem Ipsum...',
  }

  def test_views_agree(self) -> None:
    """Every view of a short sentence shows the placeholder, exactly
    'charCount' characters long."""
    for count, text in self.placeholders.items():
      with self.subTest(count=count):
        sentence = Sentence(count)
        self.assertEqual(str(sentence), text)
        self.assertEqual(len(sentence), count)
        self.assertEqual(repr(sentence), text)
        self.assertEqual([str(c) for c in sentence], [text])
        self.assertEqual(sentence.clausesLengths, [count])

  def test_placeholder_clause(self) -> None:
    """The one clause holds the placeholder words and their lengths, and
    is a 'Clause' of the same count."""
    sentence = Sentence(10)
    clause, = sentence.clausesArray
    self.assertIsInstance(clause, Clause)
    self.assertEqual(clause.charCount, 10)
    self.assertEqual(clause.wordsArray, ['Lorem', 'I...'])
    self.assertEqual(clause.wordsLengths, [5, 4])

  def test_caption_counts_its_words(self) -> None:
    """A caption counts the words it renders."""
    caption = Caption(10)
    self.assertEqual(caption.render(), 'Lorem I...')
    self.assertEqual(caption.wordCount(), 2)

  def test_full_sentence_unchanged(self) -> None:
    """A sentence of fifteen characters or more lays out real clauses,
    and its views agree as before."""
    for count in (15, 40):
      with self.subTest(count=count):
        sentence = Sentence(count)
        self.assertEqual(len(str(sentence)), count)
        self.assertNotIn('...', str(sentence))
        joined = str.join(', ', [str(c) for c in sentence])
        self.assertEqual(str(sentence), joined)

  def test_copy_and_reset(self) -> None:
    """A copy of a short sentence holds a placeholder clause of its own,
    and a reset lays the placeholder out again."""
    sentence = Sentence(10)
    copied = Sentence(sentence)
    self.assertEqual(str(copied), 'Lorem I...')
    self.assertIsNot(copied.clausesArray[0], sentence.clausesArray[0])
    sentence.reset()
    self.assertEqual(str(sentence), 'Lorem I...')
    self.assertEqual(repr(sentence), 'Lorem I...')

  def test_paragraph_of_short_count(self) -> None:
    """A short paragraph is one short sentence, and its views agree."""
    paragraph = Paragraph(10)
    self.assertEqual(str(paragraph), 'Lorem I...')
    self.assertEqual(repr(paragraph), 'Lorem I...')
    self.assertEqual(len(paragraph), 10)
