"""
TestFieldNumberDefault subclasses 'EZTest' and pins that an 'EZField'
default for a number field, one whose type is 'bool', 'int', 'float' or
'complex', goes through 'typeCast' as an argument does, so a class
accepts as a default what it accepts as an argument and refuses the
rest, strings included. 'EZField[int](2.5)' used to default to '2' and
'EZField[bool](2)' to 'True', where the arguments '2.5' and '2' raised
'TypeException', since the default called the field type, which rounds.
A subclass of a builtin is refused a foreign lone default until it
declares '__cast_as__', and keeps an instance of itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest


class MyInt(int):
  """MyInt keeps the constructor of 'int'."""


class Level(IntEnum):
  """Level has a constructor of its own, which resolves a member."""

  LOW = 1
  HIGH = 2


class TestFieldNumberDefault(EZTest):
  """
  TestFieldNumberDefault provides tests for the number defaults of
  'EZData' fields.
  """

  def test_lossy_default_refused(self) -> None:
    """A default the lossless cast refuses raises 'TypeException' naming
    the field, as the same value given as an argument does."""

    class Settings(EZData):
      retries = EZField[int](2.5)

    class Flags(EZData):
      verbose = EZField[bool](2)

    for cls, name, value in ((Settings, 'retries', 2.5),
                             (Flags, 'verbose', 2)):
      with self.subTest(field=name):
        with self.assertRaises(TypeException) as context:
          cls()
        self.assertEqual(context.exception.varName, name)
        self.assertEqual(context.exception.actualObject, value)
        with self.assertRaises(TypeException):
          cls(value)

  def test_default_value_follows(self) -> None:
    """'defaultValue' builds the default by the same rule."""

    class Settings(EZData):
      retries = EZField[int](2.5)

    field, = Settings.fields
    with self.assertRaises(TypeException):
      _ = field.defaultValue

  def test_cast_default_kept(self) -> None:
    """A default the cast converts without loss is stored as the field
    type."""

    class Settings(EZData):
      scale = EZField[float](1)
      plane = EZField[complex](1)

    settings = Settings()
    self.assertIs(type(settings.scale), float)
    self.assertEqual(settings.scale, 1.0)
    self.assertEqual(settings.plane, 1 + 0j)

  def test_string_default_refused(self) -> None:
    """A numeric string is refused as a default, as it is as an argument,
    since no cast parses text."""

    class Settings(EZData):
      retries = EZField[int]('7')

    with self.assertRaises(TypeException):
      Settings()
    with self.assertRaises(TypeException):
      Settings('7')

  def test_several_arguments_build(self) -> None:
    """Several arguments, or keywords, still go to the constructor."""

    class Settings(EZData):
      plane = EZField[complex](1, 2)
      mask = EZField[int]('ff', base=16)

    settings = Settings()
    self.assertEqual(settings.plane, 1 + 2j)
    self.assertEqual(settings.mask, 255)

  def test_subclass_refused_until_it_declares(self) -> None:
    """A subclass of a builtin without '__cast_as__' is refused every
    foreign lone default, lossless or not, and keeps an instance."""

    class Lossy(EZData):
      n = EZField[MyInt](2.5)

    class Foreign(EZData):
      n = EZField[MyInt](2.0)

    class Kept(EZData):
      n = EZField[MyInt](MyInt(2))

    for cls in (Lossy, Foreign):
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(TypeException):
          cls()
    self.assertIs(type(Kept().n), MyInt)
    self.assertEqual(Kept().n, 2)

  def test_int_enum_default(self) -> None:
    """An 'IntEnum' is a subclass of 'int' without '__cast_as__': a
    member is kept, a plain number is refused."""

    class Settings(EZData):
      level = EZField[Level](Level.HIGH)

    class Plain(EZData):
      level = EZField[Level](2)

    self.assertIs(Settings().level, Level.HIGH)
    with self.assertRaises(TypeException):
      Plain()

  def test_container_default_unchanged(self) -> None:
    """A container default still takes any lone iterable that is not
    text."""

    class Bag(EZData):
      items = EZField[list](range(3))

    self.assertEqual(Bag().items, [0, 1, 2])
