"""Integration tests for the reserved-name guard and ``@trust``
decorator interactions."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, trust
from worktoy.waitaminute.meta import ReservedName
from . import EZTest


class TestReservedNames(EZTest):

  def test_reserved_init_without_trust_raises(self) -> None:
    with self.assertRaises(ReservedName):
      # noinspection PyUnusedLocal
      class Reserved(EZData):
        x = 0

        def __init__(self, *_) -> None:
          """ignored"""

  def test_reserved_init_with_trust_passes(self) -> None:
    class Trusted(EZData):
      x = 0

      @trust
      def __init__(self, *_) -> None:
        """ignored"""

    obj = Trusted()
    self.assertEqual(obj.x, 0)

  def test_str_repr_user_overridable(self) -> None:
    class CustomRepr(EZData):
      x = 0

      def __str__(self) -> str:
        return 'custom-str'

      __repr__ = __str__

    obj = CustomRepr(7)
    self.assertEqual(str(obj), 'custom-str')
    self.assertEqual(repr(obj), 'custom-str')
