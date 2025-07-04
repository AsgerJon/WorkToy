"""
TestDelException tests the functionality of the DelException class from
the 'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass as AMeta
from worktoy.mcls import AbstractNamespace as ASpace
from worktoy.waitaminute.meta import DelException

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

    space = ASpace(AMeta, 'Sus', (), )
    with self.assertRaises(DelException) as context:
      space['__del__'] = 'yikes'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.mcls, AMeta)
    self.assertEqual(e.name, 'Sus')
    self.assertFalse(e.bases)
    self.assertIsInstance(e.space, ASpace)

    withBases = ASpace(AMeta, 'Sus', (AMeta,), )
    with self.assertRaises(DelException) as context:
      withBases['__del__'] = 'yikes'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.mcls, AMeta)
    self.assertEqual(e.name, 'Sus')
    self.assertEqual(e.bases, (AMeta,))
    self.assertIsInstance(e.space, ASpace)
