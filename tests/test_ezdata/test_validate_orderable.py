"""Tests for ``validateOrderable``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import validateOrderable
from worktoy.waitaminute.ez import UnorderedEZException
from . import EZTest
from ._factory_helpers import slot


class TestValidateOrderable(EZTest):

  def test_orderable_passes(self) -> None:
    fields = [slot('x', int, 1), slot('y', str, 'a')]
    validateOrderable(fields, 'C')

  def test_none_default_skipped(self) -> None:
    fields = [slot('x', complex, None)]
    validateOrderable(fields, 'C')

  def test_non_orderable_raises(self) -> None:
    with self.assertRaises(UnorderedEZException) as ctx:
      validateOrderable([slot('x', complex, 1 + 2j)], 'C')
    self.assertEqual(ctx.exception.className, 'C')
    self.assertEqual(ctx.exception.fieldName, 'x')

  def test_non_typeerror_propagates(self) -> None:
    class Boom(Exception):
      pass

    class Trololo:
      def __lt__(self, other) -> bool:
        raise Boom

    with self.assertRaises(Boom):
      validateOrderable([slot('x', Trololo, Trololo())], 'C')
