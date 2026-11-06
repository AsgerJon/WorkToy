"""
TestSubclassException tests 'SubclassException' from 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import WorkToyException, SubclassException
from . import WaitaminuteTest, Fraction


class TestSubclassException(WaitaminuteTest):
  """
  'SubclassException' is offered to the builder and raised nowhere in
  worktoy: a builder's class raises it where a class arrives that is no
  subclass of the one expected. It keeps the two classes, names both in
  its text, and is a 'TypeError' so an existing 'except' clause still
  catches it. The tests pin the bases and the slots, the text and the
  slots at a raise by hand, the catch as 'TypeError' and as
  'WorkToyException', the class of the docstring, and names drawn at
  random.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(SubclassException.__bases__,
                     (WorkToyException, TypeError))
    self.assertEqual(SubclassException.__slots__, ('subClass', 'baseClass'))

  def test_raised_by_hand(self) -> None:
    with self.assertRaises(SubclassException) as context:
      raise SubclassException(int, tuple)
    self.assertIs(context.exception.subClass, int)
    self.assertIs(context.exception.baseClass, tuple)
    self.assertEqual(str(context.exception),
                     "Expected class 'int' to be a subclass of 'tuple'!")
    self.assertEqual(repr(context.exception), str(context.exception))
    self.assertEqual(context.exception.args, ())

  def test_caught_as_the_builtin_and_as_the_common_base(self) -> None:
    with self.assertRaises(TypeError) as context:
      raise SubclassException(bool, str)
    self.assertIsInstance(context.exception, WorkToyException)
    self.assertIs(context.exception.subClass, bool)
    self.assertIs(context.exception.baseClass, str)
    self.assertIn("'bool' to be a subclass of 'str'", str(context.exception))
    with self.assertRaises(WorkToyException) as context:
      raise SubclassException(bool, str)
    self.assertIs(context.exception.subClass, bool)
    self.assertIs(context.exception.baseClass, str)
    self.assertIn("'bool' to be a subclass of 'str'", str(context.exception))

  def test_docstring_example(self) -> None:
    fraction = Fraction(69, 420)
    self.assertEqual((fraction.numerator, fraction.denominator), (69, 420))
    with self.assertRaises(SubclassException) as context:
      Fraction(69, '420')
    self.assertIs(context.exception.subClass, str)
    self.assertIs(context.exception.baseClass, int)
    self.assertEqual(str(context.exception),
                     "Expected class 'str' to be a subclass of 'int'!")
    with self.assertRaises(SubclassException) as context:
      Fraction(6.9, 420)
    self.assertIs(context.exception.subClass, float)
    self.assertIs(context.exception.baseClass, int)
    self.assertEqual(str(context.exception),
                     "Expected class 'float' to be a subclass of 'int'!")

  def test_random_names(self) -> None:
    self.randomWord.size = 6
    for word in self.randomWord.row:
      sub = type(word, (), {})
      with self.subTest(word=word):
        exception = SubclassException(sub, object)
        self.assertIs(exception.subClass, sub)
        self.assertIs(exception.baseClass, object)
        self.assertEqual(str(exception), "Expected class '%s' to be a "
                                         "subclass of 'object'!" % word)
