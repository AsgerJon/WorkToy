"""
TestMetaUmbrella provides some coverage gymnastics for the
'AbstractMetaclass' from the 'worktoy.mcls' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import MetaType
from worktoy.core._meta_type import _Space
from worktoy.mcls import (BaseObject, BaseSpace, BaseMeta,
                          AbstractNamespace, \
                          AbstractMetaclass)
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
    Test the 'get_namespace' method of the 'AbstractMetaclass'.
    """
    self.assertIsInstance(BaseObject.getNamespace(), BaseSpace)
    self.assertIs(BaseMeta.getNamespaceClass(), BaseSpace)
    self.assertIs(AbstractMetaclass.namespaceClass, AbstractNamespace)
    expected = MetaType.namespaceClass
    actual = _Space
    self.assertIsInstance(expected, actual)
