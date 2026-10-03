"""
TestFieldNumberDefault subclasses 'EZTest' and pins that an 'EZField'
default for a number field, one whose type is 'bool', 'int', 'float' or
'complex', or a subclass keeping the constructor of one, goes through
'typeCast' as an argument does, so a class accepts as a default what it
accepts as an argument and refuses the rest. 'EZField[int](2.5)' used to
default to '2' and 'EZField[bool](2)' to 'True', where the arguments '2.5'
and '2' raised 'TypeException', since the default called the field type,
which rounds.
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
      retries = EZField[int]('7')
      plane = EZField[complex](1)

    settings = Settings()
    self.assertIs(type(settings.scale), float)
    self.assertEqual(settings.scale, 1.0)
    self.assertEqual(settings.retries, 7)
    self.assertEqual(settings.plane, 1 + 0j)

  def test_several_arguments_build(self) -> None:
    """Several arguments, or keywords, still go to the constructor."""

    class Settings(EZData):
      plane = EZField[complex](1, 2)
      mask = EZField[int]('ff', base=16)

    settings = Settings()
    self.assertEqual(settings.plane, 1 + 2j)
    self.assertEqual(settings.mask, 255)

  def test_subclass_held_to_rule(self) -> None:
    """A subclass keeping the constructor of its builtin is held to the
    rule of the builtin, and the field holds an instance of the
    subclass."""

    class Lossy(EZData):
      n = EZField[MyInt](2.5)

    class Exact(EZData):
      n = EZField[MyInt](2.0)

    with self.assertRaises(TypeException):
      Lossy()
    self.assertIs(type(Exact().n), MyInt)
    self.assertEqual(Exact().n, 2)

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own, such as an 'IntEnum',
    receives the default as given."""

    class Settings(EZData):
      level = EZField[Level](2)

    self.assertIs(Settings().level, Level.HIGH)

  def test_container_default_unchanged(self) -> None:
    """A container default still takes any lone iterable that is not
    text."""

    class Bag(EZData):
      items = EZField[list](range(3))

    self.assertEqual(Bag().items, [0, 1, 2])
