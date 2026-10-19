"""
TestClassKeywordSpellings tests the class keywords an 'EZData' class
statement accepts.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import new_class

from worktoy.ezdata import EZData, EZField, EZHook
from . import EZTest


def _build(name: str, **kwargs) -> type:
  """Build an 'EZData' class with one field and the given class
  keywords."""

  def body(namespace: dict) -> None:
    namespace['x'] = EZField[int](0)

  return new_class(name, (EZData,), kwargs, body)


class TestClassKeywordSpellings(EZTest):
  """
  TestClassKeywordSpellings tests the class keywords of 'EZData' classes:
  every spelling of the 'frozen', 'ordered' and 'kwOnly' options sets its
  option, 'order', the spelling 'dataclasses' uses, among them, and the
  'trustMeBro' and '_strictMRO' keywords the namespace reads work beside
  them.
  """

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
