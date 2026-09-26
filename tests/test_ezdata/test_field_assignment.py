"""
TestFieldAssignment subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that assigning to a field of a non-frozen 'EZData'
instance applies the same cast as the generated '__init__'. A value that
casts to the field type is stored as the cast result, and a value that
does not raises 'TypeException' and leaves the field as it was. Without
the cast, one assignment could break the guarantee that every field
holds a value of its declared type, which is the guarantee the generated
'__delattr__' refuses deletion to protect.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException

from . import EZTest


class Reading(EZData):
  """Reading holds a 'float' field and a 'str' field."""

  value = EZField[float](0.0)
  unit = EZField[str]('m')


class LabelledReading(Reading):
  """LabelledReading declares a field of its own next to the inherited
  ones."""

  label = EZField[str]('')


class TestFieldAssignment(EZTest):
  """
  TestFieldAssignment provides tests for assignment to the fields of
  non-frozen 'EZData' instances.
  """

  def test_castable_value_is_cast(self) -> None:
    """
    An 'int' assigned to a 'float' field is stored as a 'float', just as
    the constructor stores it.
    """
    reading = Reading()
    reading.value = 2
    self.assertEqual(reading.value, 2.0)
    self.assertIs(type(reading.value), float)

  def test_uncastable_value_raises(self) -> None:
    """
    A value the cast refuses raises 'TypeException' naming the field,
    chained from the 'TypeCastException' behind it, and the field keeps
    the value it held before.
    """
    reading = Reading(1.5)
    with self.assertRaises(TypeException) as context:
      reading.value = 'not a float'
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'not a float')
    self.assertIn(float, e.expectedTypes)
    self.assertIsInstance(e.__cause__, TypeCastException)
    self.assertEqual(reading.value, 1.5)

  def test_accepted_values_match_construction(self) -> None:
    """
    Every value the constructor accepts for a field is accepted by
    assignment as well, and both store the same value of the same type.
    """
    samples = (
      ('value', 2),
      ('value', '3.5'),
      ('value', True),
      ('unit', b'cm'),
    )
    for name, sample in samples:
      with self.subTest(name=name, sample=sample):
        built = getattr(Reading(**{name: sample}), name)
        reading = Reading()
        setattr(reading, name, sample)
        assigned = getattr(reading, name)
        self.assertEqual(assigned, built)
        self.assertIs(type(assigned), type(built))

  def test_refused_values_match_construction(self) -> None:
    """
    Every value the constructor refuses for a field with 'TypeException'
    is refused by assignment with the same exception.
    """
    samples = (
      ('value', [1]),
      ('value', None),
      ('unit', 5),
      ('unit', None),
    )
    for name, sample in samples:
      with self.subTest(name=name, sample=sample):
        with self.assertRaises(TypeException):
          Reading(**{name: sample})
        reading = Reading()
        with self.assertRaises(TypeException):
          setattr(reading, name, sample)

  def test_inherited_field_is_cast(self) -> None:
    """
    A field that a subclass inherits is cast on assignment just like a
    field it declares itself.
    """
    reading = LabelledReading()
    reading.value = 4
    self.assertIs(type(reading.value), float)
    with self.assertRaises(TypeException):
      reading.label = 7

  def test_post_init_assignment_is_cast(self) -> None:
    """
    An assignment made in '__post_init__' takes the same route, so a hook
    that normalizes a field cannot leave it holding the wrong type.
    """

    class Rounded(EZData):
      value = EZField[float](0.0)

      def __post_init__(self) -> None:
        self.value = round(self.value)

    rounded = Rounded(2.6)
    self.assertEqual(rounded.value, 3.0)
    self.assertIs(type(rounded.value), float)

  def test_other_names_pass_through(self) -> None:
    """
    Only field names are cast. An attribute that is not a field is stored
    exactly as given.
    """
    reading = Reading()
    reading.note = [1, 2]
    self.assertNotIn('note', Reading.__ez_fields__)
    self.assertEqual(reading.note, [1, 2])
