"""
TestBareNoneField subclasses 'EZTest' from the 'tests.test_ezdata'
package and provides tests for the rejection of bare 'None' values in
'EZData' class bodies.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import IncompleteFieldException

from . import EZTest


class TestBareNoneField(EZTest):
  """
  TestBareNoneField provides tests for the bare-None guard in the
  'EZData' class-body machinery. A bare assignment like 'b = None'
  carries no type to infer a field from, so the class body itself
  must fail with 'IncompleteFieldException' at the offending line
  rather than producing a class whose instantiation dies later with
  a confusing message about 'NoneType'.
  """

  def test_bare_none_raises_at_class_body(self) -> None:
    """
    A class body containing a bare 'None' assignment raises
    'IncompleteFieldException' while the class is being built, and
    the exception identifies the class, the offending name, and
    the reason in plain prose.
    """
    with self.assertRaises(IncompleteFieldException) as context:
      class Sus(EZData):  # noqa: F841
        a = EZField[int](0)
        b = None
    e = context.exception
    self.assertEqual(e.clsName, 'Sus')
    self.assertEqual(e.fieldName, 'b')
    info = str(e)
    self.assertIn('bare None default cannot infer a field type', info)
    self.assertNotIn('takes no arguments', info)

  def test_explicit_field_still_works(self) -> None:
    """
    The guard only rejects the bare 'None' spelling. A class with
    only explicit 'EZField' declarations builds and instantiates
    normally.
    """

    class Fine(EZData):
      a = EZField[int](0)
      b = EZField[str]('')

    instance = Fine(7, 'seven')
    self.assertEqual(instance.a, 7)
    self.assertEqual(instance.b, 'seven')
