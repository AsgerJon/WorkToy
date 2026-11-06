"""
TestParagraph tests 'Paragraph' from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Paragraph, Sentence, GaussianLengths
from worktoy.lorem_ipsum import BaseGenerator
from worktoy.work_test.samplers import IntSampler
from . import LoremTest


class TestParagraph(LoremTest):
  """
  A paragraph is sentences joined by single spaces at exactly the
  requested count, opening with 'Lorem ipsum' unless told otherwise.
  The tests pin the layout and its arithmetic, the first-word flag and
  its callback, the short paragraph, the caches, the copy constructor
  and the renderings.
  """

  def test_layout(self) -> None:
    paragraph = Paragraph(300)
    sentences = paragraph.sentenceArray
    lengths = paragraph.sentenceLengths
    text = str(paragraph)
    self.assertEqual(len(text), 300)
    self.assertEqual(len(paragraph), 300)
    self.assertTrue(text.startswith('Lorem ipsum '))
    self.assertEqual(text, ' '.join(str(s) for s in sentences))
    self.assertEqual(sum(lengths) + len(lengths) - 1, 300)
    self.assertGreater(len(sentences), 1)
    self.assertEqual(paragraph.realize(), text)
    self.assertEqual([*paragraph], sentences)
    for sentence, length in zip(sentences, lengths):
      with self.subTest(length=length):
        self.assertIsInstance(sentence, Sentence)
        self.assertEqual(len(sentence), length)
        self.assertTrue(str(sentence).endswith('.'))
    self.assertTrue(sentences[0].isFirst)
    self.assertFalse(sentences[1].isFirst)
    self.assertEqual(repr(paragraph),
                     '\n'.join(repr(s) for s in sentences))

  def test_first_by_default(self) -> None:
    self.assertTrue(Paragraph().isFirst)
    self.assertTrue(Paragraph(100).isFirst)
    self.assertTrue(Paragraph.first(100).isFirst)
    self.assertFalse(Sentence().isFirst)
    paragraph = Paragraph(200)
    first = str(paragraph)
    paragraph.isFirst = False
    self.assertIsNone(paragraph.__sentences_array__)
    self.assertIsNone(paragraph.__sentences_lengths__)
    self.assertFalse(paragraph.sentenceArray[0].isFirst)
    self.assertEqual(len(paragraph), 200)
    self.assertNotEqual(str(paragraph), first)
    self.assertIs(Paragraph.__dict__['_onSetIsFirst'],
                  BaseGenerator.__dict__['_onSetIsFirst'])

  def test_short(self) -> None:
    paragraph = Paragraph(39)
    self.assertEqual(paragraph.sentenceLengths, [39])
    self.assertEqual(len(paragraph.sentenceArray), 1)
    self.assertEqual(len(paragraph), 39)
    self.assertTrue(str(paragraph).startswith('Lorem ipsum '))
    self.assertEqual(str(Paragraph(10)), 'Lorem I...')
    self.assertEqual(len(Paragraph(10)), 10)
    self.assertEqual(str(Paragraph(0)), '')
    self.assertEqual(len(Paragraph(0)), 0)
    self.assertEqual(Paragraph(0).sentenceLengths, [0])

  def test_sentence_distribution(self) -> None:
    paragraph = Paragraph()
    dist = paragraph.sentenceDist
    self.assertIsInstance(dist, GaussianLengths)
    self.assertEqual((dist.mean, dist.var, dist.minVal, dist.maxVal),
                     (80.0, 20.0, 40, 120))
    self.assertIs(paragraph.sentenceDist, dist)
    self.assertIsNot(Paragraph().sentenceDist, dist)

  def test_caches(self) -> None:
    paragraph = Paragraph(150)
    self.assertIsNone(paragraph.__sentences_lengths__)
    self.assertIsNone(paragraph.__sentences_array__)
    with self.assertRaises(RecursionError) as context:
      paragraph._getSentenceLengths(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      paragraph._getSentenceArray(_recursion=True)
    self.assertEqual(context.exception.args, ())
    sentences = paragraph.sentenceArray
    self.assertIs(paragraph.sentenceArray, sentences)
    paragraph.clear()
    self.assertIsNone(paragraph.__sentences_lengths__)
    self.assertIsNone(paragraph.__sentences_array__)
    paragraph.reset()
    self.assertIsNotNone(paragraph.__sentences_array__)
    self.assertIsNot(paragraph.sentenceArray, sentences)
    self.assertEqual(len(paragraph), 150)
    paragraph.charCount = 250
    self.assertIsNone(paragraph.__sentences_array__)
    self.assertEqual(len(paragraph), 250)

  def test_copy_constructor(self) -> None:
    blank = Paragraph(150)
    blank.isFirst = False
    copy = Paragraph(blank)
    self.assertEqual(copy.charCount, 150)
    self.assertFalse(copy.isFirst)
    self.assertIsNone(copy.__sentences_lengths__)
    self.assertIsNone(copy.__sentences_array__)
    built = Paragraph(200)
    text = str(built)
    copy = Paragraph(built)
    self.assertEqual(str(copy), text)
    self.assertTrue(copy.isFirst)
    self.assertEqual(copy.sentenceLengths, built.sentenceLengths)
    self.assertIsNot(copy.sentenceLengths, built.sentenceLengths)
    for mine, theirs in zip(copy.sentenceArray, built.sentenceArray):
      with self.subTest(text=str(theirs)):
        self.assertIsNot(mine, theirs)
        self.assertEqual(str(mine), str(theirs))
        self.assertIsNot(mine.clausesArray[0], theirs.clausesArray[0])

  def test_random_counts(self) -> None:
    self.randomInteger = IntSampler(40, 600, seed=self.__sampler_seed__)
    self.randomInteger.size = 10
    for count in self.randomInteger.row:
      with self.subTest(count=count):
        paragraph = Paragraph(count)
        self.assertEqual(len(paragraph), count)
        self.assertEqual(len(str(paragraph)), count)
        self.assertTrue(str(paragraph).startswith('Lorem ipsum'))
