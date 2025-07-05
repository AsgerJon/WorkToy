"""
TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
AbstractMetaclass from the worktoy.mcls module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import MetaType
from worktoy.core._meta_type import _Space  # NOQA
from worktoy.mcls import AbstractMetaclass, AbstractNamespace

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestMetaUmbrella(TestCase):
  """
  TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
  AbstractMetaclass from the worktoy.mcls module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def testNamespaceDescriptor(self) -> None:
    """
    Test ad-hoc metaclass functionality.
    """
    self.assertIsInstance(MetaType.namespaceClass, _Space)
    self.assertIs(AbstractMetaclass.namespaceClass, AbstractNamespace)

    class Foo: pass
