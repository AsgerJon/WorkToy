"""
TestMetaclassConflict tests that the confusing error message:
'metaclass conflict: the metaclass of a derived class must be a (
non-strict) subclass of the metaclasses of all its bases' is raised when a
class is created with conflicting metaclasses.'
is correctly replaced with the far superior:

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass, BaseSpace
from worktoy.waitaminute import VariableNotNone
from worktoy.waitaminute.meta import MetaclassException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestMetaclassConflict(TestCase):
  """
  TestMetaclassConflict tests that the confusing error message:
  'metaclass conflict: the metaclass of a derived class must be a (
  non-strict) subclass of the metaclasses of all its bases' is correctly
  replaced with the far superior:
  'The metaclasses of the bases are not compatible.'
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_metaclass_conflict(self) -> None:
    """
    Tests that a metaclass conflict raises the correct error message.
    """

    class MetaA(type):
      pass

    class MetaB(type):
      pass

    class SubMetaA(MetaA):
      pass

    class SubMetaB(MetaB):
      pass

    class BaseA(metaclass=MetaA):
      pass

    class BaseB(metaclass=MetaB):
      pass

    with self.assertRaises(MetaclassException) as context:
      class Bad(BaseA, BaseB):
        """
        Bad is a bad class
        """
    e = context.exception
    self.assertEqual(e.name, 'Bad')
    self.assertIs(e.meta, MetaA)
    self.assertIs(e.badBase, BaseB)
    self.assertIs(e.badMeta, MetaB)
