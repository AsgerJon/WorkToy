"""
TestLoremText tests 'LOREM_WORDS', 'randomWord' and 'loremSentence' from
'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random
from random import Random

from worktoy.work_test.samplers import LOREM_WORDS, randomWord
from worktoy.work_test.samplers import loremSentence, IntSampler
from worktoy.work_test.samplers._lorem_text import _LONGEST, _OF_LENGTH
from worktoy.work_test.samplers._lorem_text import _UP_TO_LENGTH
from worktoy.work_test.samplers._lorem_text import _fittingWord
from . import WorkTestTest


class TestLoremText(WorkTestTest):
  """
  The samplers take their text from a vocabulary of their own, with a
  word of every length up to the longest, which is what lets a sentence
  close at exactly the count asked for. 'randomWord' draws one word and
  'loremSentence' builds a sentence of exactly 'charCount' characters,
  capitalised and closed with a period, each drawing from the generator
  given or from the 'random' module. The tests pin the vocabulary, the
  two draws with and without a generator, the exact lengths from one
  character up, the refusal below one, and the fitting of a word into
  the room left.
  """

  def test_vocabulary(self) -> None:
    self.assertEqual(_LONGEST, 10)
    self.assertEqual(len(LOREM_WORDS), len(set(LOREM_WORDS)))
    for n in range(1, _LONGEST + 1):
      with self.subTest(n=n):
        self.assertTrue(_OF_LENGTH[n])
        for word in _OF_LENGTH[n]:
          self.assertEqual(len(word), n)
        for word in _UP_TO_LENGTH[n]:
          self.assertLessEqual(len(word), n)
        upTo = sum(len(_OF_LENGTH[k]) for k in range(1, n + 1))
        self.assertEqual(len(_UP_TO_LENGTH[n]), upTo)
    self.assertEqual(len(_UP_TO_LENGTH[_LONGEST]), len(LOREM_WORDS))
    self.assertEqual(sorted(_OF_LENGTH), [*range(1, _LONGEST + 1)])
    self.assertEqual(sorted(_UP_TO_LENGTH), [*range(1, _LONGEST + 1)])
    for word in LOREM_WORDS:
      with self.subTest(word=word):
        self.assertTrue(word.isalpha())
        self.assertTrue(word.islower())

  def test_random_word(self) -> None:
    first, second = Random(3), Random(3)
    self.assertEqual([randomWord(first) for _ in range(8)],
                     [randomWord(second) for _ in range(8)])
    for word in (randomWord(first) for _ in range(8)):
      self.assertIn(word, LOREM_WORDS)
    random.seed(3)
    one = [randomWord() for _ in range(8)]
    random.seed(3)
    self.assertEqual([randomWord() for _ in range(8)], one)
    self.assertIn(one[0], LOREM_WORDS)

  def test_sentence_lengths(self) -> None:
    generator = Random(1)
    for count in range(1, 80):
      with self.subTest(count=count):
        sentence = loremSentence(count, generator)
        self.assertEqual(len(sentence), count)
        self.assertTrue(sentence.endswith('.'))
        body = sentence[:-1]
        self.assertNotIn('.', body)
        self.assertEqual(body, body[:1].upper() + body[1:])
        words = body.lower().split()
        self.assertEqual(str.join(' ', words), body.lower())
        for word in words:
          self.assertIn(word, LOREM_WORDS)
    self.assertEqual(loremSentence(1, generator), '.')
    self.assertEqual(loremSentence(2, generator), 'A.')
    random.seed(5)
    one = loremSentence(30)
    random.seed(5)
    self.assertEqual(loremSentence(30), one)
    self.assertEqual(len(one), 30)

  def test_count_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      loremSentence(0)
    self.assertEqual(str(context.exception), 'A sentence needs at least '
                                             'one character, but 0 were '
                                             'asked for!')
    with self.assertRaises(ValueError) as context:
      loremSentence(-3, Random(1))
    self.assertIn('but -3 were asked for!', str(context.exception))

  def test_fitting_word(self) -> None:
    generator = Random(2)
    for room in range(1, _LONGEST + 1):
      with self.subTest(room=room):
        self.assertEqual(len(_fittingWord(room, generator)), room)
    for room in (_LONGEST + 1, _LONGEST + 2, 25, 100):
      with self.subTest(room=room):
        word = _fittingWord(room, generator)
        self.assertLessEqual(len(word), min(room - 2, _LONGEST))
        self.assertIn(word, LOREM_WORDS)
    random.seed(4)
    self.assertEqual(len(_fittingWord(7)), 7)
    #  A room of one or two more than the longest word leaves a space and
    #  a letter after a word two shorter, and no word is longer than that.
    for seed in range(40):
      for room in (_LONGEST + 1, _LONGEST + 2):
        with self.subTest(seed=seed, room=room):
          word = _fittingWord(room, Random(seed))
          self.assertLessEqual(len(word), room - 2)
          self.assertIn(word, _UP_TO_LENGTH[room - 2])

  def test_sentences_at_the_edge_of_the_longest_word(self) -> None:
    #  A body of eleven or twelve characters is the one case where the
    #  first word is drawn from the words two shorter than the room.
    for seed in range(40):
      for count in (11, 12, 13, 14):
        with self.subTest(seed=seed, count=count):
          sentence = loremSentence(count, Random(seed))
          self.assertEqual(len(sentence), count)
          first = sentence[:-1].split(' ')[0].lower()
          self.assertIn(first, LOREM_WORDS)
    self.assertEqual(loremSentence(12, Random(0)), 'Suscipit in.')
    self.assertEqual(loremSentence(12, Random(1)), 'Eum quaerat.')
    self.assertEqual(loremSentence(12, Random(2)), 'Voluptate a.')
    self.assertEqual(loremSentence(13, Random(0)), 'Quaerat quia.')
    self.assertEqual(loremSentence(13, Random(1)), 'Enim quaerat.')
    self.assertEqual(loremSentence(13, Random(2)), 'Est deserunt.')

  def test_random_counts(self) -> None:
    self.randomInteger = IntSampler(1, 120, seed=self.__sampler_seed__)
    self.randomInteger.size = 12
    generator = Random(self.__sampler_seed__)
    for count in self.randomInteger.row:
      with self.subTest(count=count):
        self.assertEqual(len(loremSentence(count, generator)), count)
