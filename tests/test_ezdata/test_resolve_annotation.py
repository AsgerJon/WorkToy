"""Tests for ``resolveAnnotation``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import resolveAnnotation
from . import EZTest


class TestResolveAnnotation(EZTest):

  def test_type_passthrough(self) -> None:
    self.assertIs(resolveAnnotation(int), int)

  def test_builtin_string_resolved(self) -> None:
    self.assertIs(resolveAnnotation('int'), int)
    self.assertIs(resolveAnnotation('str'), str)
    self.assertIs(resolveAnnotation('complex'), complex)

  def test_none_type_string(self) -> None:
    self.assertIs(resolveAnnotation('NoneType'), type(None))

  def test_unknown_string(self) -> None:
    self.assertIsNone(resolveAnnotation('Optional[int]'))

  def test_non_type_attribute_in_builtins(self) -> None:
    self.assertIsNone(resolveAnnotation('print'))

  def test_non_string_non_type(self) -> None:
    self.assertIsNone(resolveAnnotation(42))
