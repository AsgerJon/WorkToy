"""
TestGeneratorKeywords tests how the 'worktoy.lorem_ipsum' generators treat
keyword arguments to their constructors.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from worktoy.lorem_ipsum import BaseGenerator, Clause, Sentence, Paragraph
from worktoy.waitaminute import TypeException
from . import LoremIpsumTest


class TestGeneratorKeywords(LoremIpsumTest):
  """
  TestGeneratorKeywords tests the keyword arguments of the constructors of
  'BaseGenerator', 'Clause', 'Sentence' and 'Paragraph'. The target
  character count may be given as the 'charCount' keyword, just as it may
  be given by position, while any other keyword is refused with the
  'TypeError' Python raises for an unexpected keyword argument, which is
  also what the positional form has always raised.
  """

  generators = (BaseGenerator, Clause, Sentence, Paragraph)

  def test_char_count_keyword(self) -> None:
    """
    Testing that each generator takes its character count as the
    'charCount' keyword.
    """
    for generator in self.generators:
      for _ in range(8):
        count = randint(69, 420)
        with self.subTest(generator=generator.__name__, count=count):
          self.assertEqual(generator(charCount=count).charCount, count)

  def test_char_count_keyword_zero(self) -> None:
    """
    Testing that a 'charCount' keyword of zero is honoured rather than
    taken for a missing one.
    """
    for generator in self.generators:
      with self.subTest(generator=generator.__name__):
        self.assertEqual(generator(charCount=0).charCount, 0)

  def test_char_count_keyword_first(self) -> None:
    """
    Testing that 'first' passes the 'charCount' keyword on to the
    constructor and still marks the generator as the first.
    """
    for generator in self.generators:
      with self.subTest(generator=generator.__name__):
        first = generator.first(charCount=69)
        self.assertEqual(first.charCount, 69)
        self.assertTrue(first.isFirst)

  def test_char_count_keyword_cast(self) -> None:
    """
    Testing that a 'charCount' keyword is cast the way an assignment to
    'charCount' is: '30.0' is stored as the integer '30', and '2.5', which
    no integer holds without loss, is refused with 'TypeException'.
    """
    for generator in self.generators:
      with self.subTest(generator=generator.__name__):
        cast = generator(charCount=30.0).charCount
        self.assertEqual(cast, 30)
        self.assertIsInstance(cast, int)
        with self.assertRaises(TypeException):
          generator(charCount=2.5)

  def test_default_without_arguments(self) -> None:
    """
    Testing that a generator built without arguments holds the default of
    the 'charCount' box.
    """
    default = BaseGenerator.charCount.getPosArgs()[0]
    for generator in self.generators:
      with self.subTest(generator=generator.__name__):
        self.assertEqual(generator().charCount, default)

  def test_unknown_keyword_refused(self) -> None:
    """
    Testing that a keyword other than 'charCount', a misspelling such as
    'chars' included, is refused with Python's own 'TypeError' naming the
    keyword, rather than dropped. That holds beside 'charCount' as well,
    and through 'first'.
    """
    calls = (
      lambda generator: generator(chars=30),
      lambda generator: generator(charCount=30, chars=30),
      lambda generator: generator.first(chars=30),
    )
    for generator in self.generators:
      for index, call in enumerate(calls):
        with self.subTest(generator=generator.__name__, call=index):
          with self.assertRaises(TypeError) as context:
            call(generator)
          self.assertIs(type(context.exception), TypeError)
          self.assertIn('chars', str(context.exception))

  def test_positional_form_refuses_keywords(self) -> None:
    """
    Testing that the positional form refuses keywords as it always has:
    'charCount' given both by position and by keyword, and any other
    keyword beside the position, while the position alone is stored.
    """
    for generator in self.generators:
      with self.subTest(generator=generator.__name__):
        self.assertEqual(generator(69).charCount, 69)
        for key in ('charCount', 'chars'):
          with self.assertRaises(TypeError) as context:
            generator(69, **{key: 30})
          self.assertIs(type(context.exception), TypeError)
          self.assertIn(key, str(context.exception))

  def test_copy_refuses_keywords(self) -> None:
    """
    Testing that the copy constructors take no keywords: a 'Clause',
    'Sentence' or 'Paragraph' built from another one refuses 'charCount'
    and any other keyword alike, with Python's own 'TypeError'.
    """
    for generator in (Clause, Sentence, Paragraph):
      other = generator(69)
      for key in ('charCount', 'chars'):
        with self.subTest(generator=generator.__name__, key=key):
          with self.assertRaises(TypeError) as context:
            generator(other, **{key: 30})
          self.assertIs(type(context.exception), TypeError)
          self.assertIn(key, str(context.exception))
