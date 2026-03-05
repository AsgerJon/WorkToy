"""
TestMetaclassException tests the exception handling in the WaitAMinute
metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import WaitAMinuteTest
from worktoy.mcls import BaseObject, BaseMeta
from worktoy.utilities import textFmt
from worktoy.waitaminute.meta import MetaclassException


class TestMetaclassException(WaitAMinuteTest):
  """
  TestMetaclassException tests the exception handling in the WaitAMinute
  metaclass.
  """

  def test_raises(self, ) -> None:
    """
    Tests that MetaclassException correctly raises TypeError when passing
    a metaclass which does support each received base class.
    """

    with self.assertRaises(TypeError) as context:
      raise MetaclassException(type, 'breh', int, str, list)
    e = context.exception
    expected = """was raised with no base classes incompatible 
      with the received metaclass"""
    self.assertIn(textFmt(expected), str(e))

  def test_str_repr(self) -> None:
    """
    Tests that MetaclassException has a correct string representation.
    """

    class _Meta(type):
      pass

    class Sus(metaclass=_Meta):
      pass

    with self.assertRaises(Exception) as context:
      class Breh(BaseObject, Sus):
        """
        Breh is a sus class
        """
    e = context.exception
    self.assertIs(e.name, 'Breh')
    self.assertIs(e.meta, BaseMeta)
    self.assertIs(e.badBase, Sus)
    self.assertIs(e.badMeta, _Meta)
    self.assertEqual(str(e), repr(e))
