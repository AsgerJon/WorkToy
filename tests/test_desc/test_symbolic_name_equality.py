"""
TestSymbolicNameEquality subclasses 'DescTest' and pins that two
'SymbolicName' objects of the same words compare equal and hash alike,
ignoring case, as every rendering of them is the same string. A name used
to compare and hash by identity, so a settings table keyed by names grew
a second entry for the same option and never found it again, two names
made a set of two, and an 'EZData' holding a name never equalled another
built from the same words.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import SymbolicName
from worktoy.ezdata import EZData, EZField

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Settings:
  """
  Settings keyed by the symbolic name of each option, so one key renders
  as 'font_size' in a config file and 'FONT_SIZE' in the environment.
  """

  def __init__(self) -> None:
    self.values = dict()

  def set(self, name: SymbolicName, value: Any) -> None:
    self.values[name] = value

  def get(self, name: SymbolicName) -> Any:
    return self.values[name]


class Option(EZData):
  """
  Option is a setting named symbolically.
  """

  name = EZField[SymbolicName](SymbolicName('font', 'size'))
  value = EZField[int](12)


class TestSymbolicNameEquality(DescTest):
  """
  TestSymbolicNameEquality provides tests for the equality and hashing of
  'SymbolicName'.
  """

  def test_same_words_equal(self) -> None:
    """Two names of the same words are equal, hash alike and make one
    member of a set."""
    a, b = SymbolicName('font', 'size'), SymbolicName('font', 'size')
    self.assertIsNot(a, b)
    self.assertEqual(a, b)
    self.assertEqual(hash(a), hash(b))
    self.assertEqual(len({a, b}), 1)

  def test_case_ignored(self) -> None:
    """Two names differing in case alone render alike, and are equal."""
    a, c = SymbolicName('font', 'size'), SymbolicName('Font', 'SIZE')
    self.assertEqual(a.snake, c.snake)
    self.assertEqual(a.camel, c.camel)
    self.assertEqual(a, c)
    self.assertEqual(hash(a), hash(c))

  def test_different_words_unequal(self) -> None:
    """Fewer words, other words or another order make another name."""
    a = SymbolicName('font', 'size')
    self.assertNotEqual(a, SymbolicName('font'))
    self.assertNotEqual(a, SymbolicName('size', 'font'))
    self.assertNotEqual(a, SymbolicName('font', 'sizes'))

  def test_other_types(self) -> None:
    """Compared with anything but a name, a name answers 'NotImplemented',
    so a rendering of it is not equal to it."""
    a = SymbolicName('font', 'size')
    self.assertIs(a.__eq__('font_size'), NotImplemented)
    self.assertFalse(a == 'font_size')
    self.assertTrue(a != ('font', 'size'))

  def test_empty_names_equal(self) -> None:
    """Two names without words are equal."""
    self.assertEqual(SymbolicName(), SymbolicName())
    self.assertNotEqual(SymbolicName(), SymbolicName('a'))

  def test_settings_table(self) -> None:
    """A settings table keyed by names updates an option in place and
    finds it again, whatever the case of the lookup."""
    settings = Settings()
    settings.set(SymbolicName('font', 'size'), 12)
    settings.set(SymbolicName('font', 'size'), 14)
    self.assertEqual(len(settings.values), 1)
    self.assertEqual(settings.get(SymbolicName('Font', 'Size')), 14)

  def test_ez_data_holding_names(self) -> None:
    """An 'EZData' holding a name equals another of the same words."""
    self.assertEqual(Option(), Option())
    self.assertEqual(Option().name, SymbolicName('font', 'size'))
    self.assertEqual(Option(SymbolicName('a')), Option(SymbolicName('A')))
    self.assertNotEqual(Option(SymbolicName('a')), Option(SymbolicName('b')))
