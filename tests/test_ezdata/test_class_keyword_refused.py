"""
TestClassKeywordRefused tests that an 'EZData' class statement refuses a
class keyword that is none of the options 'EZData' reads.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import new_class

from worktoy.ezdata import EZData, EZField, EZHook
from worktoy.waitaminute.ezdata import ClassKeywordError
from . import EZTest


def _build(name: str, **kwargs) -> type:
  """Build an 'EZData' class with one field and the given class
  keywords."""

  def body(namespace: dict) -> None:
    namespace['x'] = EZField[int](0)

  return new_class(name, (EZData,), kwargs, body)


class TestClassKeywordRefused(EZTest):
  """
  TestClassKeywordRefused tests the class keywords of 'EZData' classes. The
  spellings of the 'frozen', 'ordered' and 'kwOnly' options, and the
  'trustMeBro' and '_strictMRO' keywords the namespace reads, are
  accepted, and any other class keyword raises 'ClassKeywordError' at the
  class statement, before the class body runs. 'order', the spelling
  'dataclasses' uses, is among the spellings of 'ordered'.
  """

  def test_misspelled_option(self) -> None:
    """
    Testing that a misspelled option is refused with 'ClassKeywordError'
    naming the class, the keyword and the accepted spellings.
    """
    with self.assertRaises(ClassKeywordError) as context:
      _build('Q', frozn=True)
    exception = context.exception
    self.assertEqual(exception.clsName, 'Q')
    self.assertEqual(exception.keyword, 'frozn')
    self.assertIn('frozen', exception.accepted)
    self.assertIn('frozn', str(exception))
    self.assertIn('frozen', str(exception))

  def test_refused_before_the_body(self) -> None:
    """
    Testing that the refusal comes at the class statement, before the
    class body runs.
    """
    ran = []
    body = lambda namespace: ran.append('body')
    with self.assertRaises(ClassKeywordError):
      new_class('Q', (EZData,), dict(frozn=True), body)
    self.assertEqual(ran, [])

  def test_is_type_error(self) -> None:
    """
    Testing that 'ClassKeywordError' is a 'TypeError', as Python's own
    refusal of an unexpected keyword is.
    """
    with self.assertRaises(TypeError):
      _build('Q', order_by='x')

  def test_order_spelling(self) -> None:
    """
    Testing that 'order', the spelling 'dataclasses' uses, makes the class
    ordered.
    """
    cls = _build('R', order=True)
    self.assertTrue(cls.isOrdered)
    self.assertLess(cls(1), cls(2))

  def test_every_option_spelling(self) -> None:
    """
    Testing that every spelling of every option is accepted and sets its
    option.
    """
    options = (
      (EZHook.__frozen_keys__, 'isFrozen'),
      (EZHook.__ordered_keys__, 'isOrdered'),
      (EZHook.__kw_only_keys__, 'kwOnly'),
    )
    for keys, flag in options:
      for key in keys:
        with self.subTest(key=key):
          cls = _build('Opt', **{key: True})
          self.assertTrue(getattr(cls, flag))

  def test_namespace_keywords(self) -> None:
    """
    Testing that the 'trustMeBro' and '_strictMRO' keywords the namespace
    reads are accepted.
    """

    class Trusted(EZData, trustMeBro=True):
      x = EZField[int](0)
      __del__ = lambda self: None

    class Strict(EZData, _strictMRO=True):
      x = EZField[int](0)

    self.assertIn('__del__', Trusted.__dict__)
    self.assertEqual(Strict(1).x, 1)
