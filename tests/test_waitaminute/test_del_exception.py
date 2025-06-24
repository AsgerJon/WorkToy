"""
TestDelException tests the functionality of the DelException class from
the 'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass, AbstractNamespace
from worktoy.static import Dispatch, PreClass

from typing import TYPE_CHECKING

from worktoy.text import stringList
from worktoy.waitaminute import MissingVariable, TypeException, DelException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDelException(TestCase):
  """
  TestDelException tests the functionality of the DelException class from
  the 'worktoy.waitaminute' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_del_implementation(self) -> None:
    """
    Tests that the DelException class correctly implements the __del__
    method.
    """

    with self.assertRaises(DelException) as context:
      class Sus(metaclass=AbstractMetaclass):
        def __del__(self) -> None: pass
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.mcls, AbstractMetaclass)
    self.assertEqual(e.name, 'Sus')
    self.assertFalse(e.bases)
    self.assertIsInstance(e.space, AbstractNamespace)

  def test_del_implementation_with_bases(self) -> None:
    """
    Tests that the DelException class correctly handles bases when
    implementing the __del__ method.
    """

    with self.assertRaises(DelException) as context:
      class Sus(object, int, metaclass=AbstractMetaclass):
        def __del__(self) -> None: pass
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.mcls, AbstractMetaclass)
    self.assertEqual(e.name, 'Sus')
    self.assertEqual(e.bases, (object, int))
    self.assertIsInstance(e.space, AbstractNamespace)
    self.assertEqual
