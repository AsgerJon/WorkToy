"""
TestClassObjectRejected subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that an 'EZData' class body refuses class objects with
'ClassFieldError'. A bare class-body value becomes a field whose default
is rebuilt as 'type(value)(value)', which for a class gives its
metaclass, so a nested class or a class bound to a name would quietly
become a field whose default is 'type' itself. The class body fails at
the offending line instead, the same way it does for a bare 'None'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ClassFieldError

from . import EZTest


class TestClassObjectRejected(EZTest):
  """
  TestClassObjectRejected provides tests for the refusal of class objects
  in 'EZData' class bodies.
  """

  def test_nested_class_raises(self) -> None:
    """
    A nested class statement raises 'ClassFieldError' while the class is
    being built. The exception is a 'TypeError' and names the class under
    construction, the name, and the nested class.
    """
    with self.assertRaises(ClassFieldError) as context:
      class Holder(EZData):  # noqa: F841
        x = EZField[int](0)

        class Inner:
          pass
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertEqual(e.clsName, 'Holder')
    self.assertEqual(e.fieldName, 'Inner')
    self.assertEqual(e.classObject.__name__, 'Inner')
    self.assertIn('Holder', str(e))
    self.assertIn('Inner', str(e))
    self.assertEqual(str(e), repr(e))

  def test_class_bound_to_name_raises(self) -> None:
    """
    Binding an existing class to a name, as in 'kind = int', is refused
    the same way as a nested class statement, and the exception carries
    the class that was bound.
    """
    with self.assertRaises(ClassFieldError) as context:
      class Holder(EZData):  # noqa: F841
        kind = int
    e = context.exception
    self.assertEqual(e.clsName, 'Holder')
    self.assertEqual(e.fieldName, 'kind')
    self.assertIs(e.classObject, int)
    self.assertIn('kind', str(e))
    self.assertIn('int', str(e))

  def test_bare_values_still_become_fields(self) -> None:
    """
    The refusal covers class objects only. A bare value that is not a
    class still becomes a field with that value as its default.
    """

    class Holder(EZData):
      label = 'anon'
      count = 3

    self.assertEqual(tuple(Holder.__ez_fields__), ('label', 'count'))
    holder = Holder()
    self.assertEqual(holder.label, 'anon')
    self.assertEqual(holder.count, 3)
