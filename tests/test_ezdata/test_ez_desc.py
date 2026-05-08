"""Tests for ``worktoy.ezdata._ez_desc.EZDesc``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZDesc
from worktoy.waitaminute import TypeException
from . import EZTest


class _NS:
  """A stand-in for the ``__namespace__`` attribute carried by
  classes constructed with ``BaseMeta``."""

  def __init__(self, **kwargs) -> None:
    self.__key_args__ = kwargs


class TestEZDesc(EZTest):

  def test_get_kwarg_name(self) -> None:
    d = EZDesc('frozen', bool, False)
    self.assertEqual(d._getKwarg(), 'frozen')

  def test_value_type_default_is_bool(self) -> None:
    d = EZDesc('frozen')
    self.assertIs(d._getValueType(), bool)

  def test_value_type_explicit(self) -> None:
    d = EZDesc('count', int, 0)
    self.assertIs(d._getValueType(), int)

  def test_init_with_extra_args_silently_absorbs(self) -> None:
    #  Implementation-detail: the rest pattern accepts more args.
    d = EZDesc('count', int, 0, 'extra1', 'extra2')
    self.assertIs(d._getValueType(), int)
    self.assertEqual(d.__default_value__, 0)

  def test_bool_target_truthy(self) -> None:
    class Foo:
      bar = EZDesc('bar', bool, False)
      __namespace__ = _NS(bar='whatever')

    self.assertEqual(Foo().bar, True)

  def test_bool_target_falsy(self) -> None:
    class Foo:
      bar = EZDesc('bar', bool, False)
      __namespace__ = _NS()

    self.assertEqual(Foo().bar, False)

  def test_non_bool_isinstance_match(self) -> None:
    class Foo:
      bar = EZDesc('bar', int, 7)
      __namespace__ = _NS(bar=42)

    self.assertEqual(Foo().bar, 42)

  def test_non_bool_default_used_when_kwarg_missing(self) -> None:
    class Foo:
      bar = EZDesc('bar', int, 7)
      __namespace__ = _NS()

    self.assertEqual(Foo().bar, 7)

  def test_non_bool_type_mismatch_raises(self) -> None:
    class Foo:
      bar = EZDesc('bar', int, 7)
      __namespace__ = _NS(bar='not an int')

    with self.assertRaises(TypeException):
      _ = Foo().bar
