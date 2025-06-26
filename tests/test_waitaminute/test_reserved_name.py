"""
TestReservedName tests the ReservedName exception from the
'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject, AbstractNamespace, AbstractMetaclass
from worktoy.mcls.space_hooks import ReservedNames
from worktoy.waitaminute import ReservedName

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestReservedName(TestCase):
  """
  TestReservedName tests the ReservedName exception from the
  'worktoy.waitaminute' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_res_name_in_class_body(self) -> None:
    """
    Tests that a ReservedName exception is raised when a reserved name
    is used in a class body.
    """
    for name in ReservedNames():
      space = AbstractNamespace(AbstractMetaclass, name, ())
      space[name] = 42
      with self.assertRaises(ReservedName) as context:
        space[name] = 42
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertEqual(e.resName, name)
