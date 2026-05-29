"""
TestMetaUmbrella provides some coverage gymnastics for the
'AbstractMetaclass' from the 'worktoy.mcls' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject, BaseSpace, BaseMeta, AbstractNamespace
from worktoy.mcls import AbstractMetaclass
from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestMetaUmbrella(MCLSTest):
  """
  TestMetaUmbrella provides some coverage gymnastics for the
  'AbstractMetaclass' from the 'worktoy.mcls' module.
  """

  def test_get_namespace(self) -> None:
    """
    This method tests the 'getNamespace' method of 'BaseObject' and the
    'getNamespaceClass' method of both 'BaseMeta' and 'AbstractMetaclass'.
    """
    self.assertIsInstance(BaseObject.getNamespace(), BaseSpace)
    self.assertIs(BaseMeta.getNamespaceClass(), BaseSpace)
    self.assertIs(AbstractMetaclass.getNamespaceClass(), AbstractNamespace)

  def test_inline_class(self, ) -> None:
    """
    This method tests the inline instantiation of AbstractMetaclass.
    """
    space = dict(tom=69, dick=420, harry=1337)
    A = AbstractMetaclass('A', (), space)
    self.assertEqual(A.tom, 69)
    self.assertEqual(A.dick, 420)
    self.assertEqual(A.harry, 1337)
