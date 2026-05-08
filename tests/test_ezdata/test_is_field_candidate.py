"""Tests for ``isFieldCandidate``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import isFieldCandidate
from . import EZTest


class TestIsFieldCandidate(EZTest):

  def test_dunder_excluded(self) -> None:
    self.assertFalse(isFieldCandidate('__init__', 0))

  def test_callable_excluded(self) -> None:
    self.assertFalse(isFieldCandidate('foo', lambda: 0))

  def test_get_descriptor_excluded(self) -> None:
    class Desc:
      def __get__(self, *_) -> int: return 0

    self.assertFalse(isFieldCandidate('foo', Desc()))
    self.assertFalse(Desc().__get__(None, None, ))

  def test_set_descriptor_excluded(self) -> None:
    class Desc:
      def __set__(self, *_) -> int: pass

    self.assertFalse(isFieldCandidate('foo', Desc()))
    self.assertIsNone(Desc().__set__(None, None, ))

  def test_plain_value_accepted(self) -> None:
    self.assertTrue(isFieldCandidate('foo', 0))
    self.assertTrue(isFieldCandidate('bar', 'hi'))
