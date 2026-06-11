"""
TestFieldAlias pins the aliasing of EZField declarations inside an
'EZData' class body. The namespace shadow space keeps a claimed field
name readable later in the same body, and 'EZSpace.registerEZField'
clones a field instance that is already bound to a name, so the alias
becomes an independent field instead of mutating the original's name
binding. A module-level decoy sharing the field's name verifies that
the body reads the claimed field rather than escaping to the module
scope.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from . import EZTest

#  Module-level decoy sharing its name with the field declared below.
x = 'global decoy'

#  A field instance shared between two class bodies. The first class
#  binds the instance itself; the second receives a clone.
SHARED = EZField[float](2.5)


class Pair(EZData):
  """Pair declares the field 'x' and aliases it as 'y'."""

  x = EZField[int](1)
  y = x


class FirstOwner(EZData):
  """FirstOwner binds the shared module-level field instance."""

  val = SHARED


class SecondOwner(EZData):
  """SecondOwner binds the same shared instance and receives a clone."""

  val = SHARED


class TestFieldAlias(EZTest):
  """
  TestFieldAlias provides tests for aliased and shared EZField
  declarations resolving through the namespace shadow space.
  """

  def test_alias_creates_independent_field(self) -> None:
    """
    Testing that 'y = x' declares a second, independent field with the
    same type and default as the original.
    """
    self.assertEqual(tuple(Pair.__ez_fields__), ('x', 'y'))
    pair = Pair()
    self.assertEqual(pair.x, 1)
    self.assertEqual(pair.y, 1)
    pair = Pair(2, 3)
    self.assertEqual(pair.x, 2)
    self.assertEqual(pair.y, 3)
    xField, yField = Pair.fields
    self.assertIsNot(xField, yField)
    self.assertEqual(xField.fieldName, 'x')
    self.assertEqual(yField.fieldName, 'y')

  def test_alias_beats_global_decoy(self) -> None:
    """
    Testing that the alias bound the claimed field rather than the
    module-level decoy sharing its name.
    """
    self.assertEqual(x, 'global decoy')
    pair = Pair()
    self.assertIsInstance(pair.y, int)

  def test_shared_instance_across_classes(self) -> None:
    """
    Testing that binding one field instance in two class bodies leaves
    the first binding untouched while the second class receives an
    independent clone.
    """
    firstField, = FirstOwner.fields
    secondField, = SecondOwner.fields
    self.assertIs(firstField, SHARED)
    self.assertIsNot(secondField, SHARED)
    self.assertEqual(firstField.fieldName, 'val')
    self.assertEqual(secondField.fieldName, 'val')
    self.assertEqual(FirstOwner().val, 2.5)
    self.assertEqual(SecondOwner().val, 2.5)
