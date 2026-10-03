"""
TestClassInitOwner subclasses 'EZTest' and pins that the fields of an
'EZData' class know their owner by the time its '__class_init__' runs.
'EZMeta.__init__' used to bind the owners after the inherited '__init__',
which is what runs the hook, so a '__class_init__' reading 'fieldOwner'
raised 'MissingVariable'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class TestClassInitOwner(EZTest):
  """
  TestClassInitOwner provides tests for the field owners an EZData
  '__class_init__' sees.
  """

  def test_own_fields(self) -> None:
    """The hook sees the class as the owner of its own fields."""
    seen = []

    class Point(EZData):
      x = EZField[int](0)
      y = EZField[int](0)

      @classmethod
      def __class_init__(cls, *args, **kwargs) -> None:
        seen.extend(field.fieldOwner for field in cls.fields)

    self.assertEqual(seen, [Point, Point])

  def test_inherited_fields(self) -> None:
    """The hook of a subclass sees the subclass as the owner of the
    fields it inherits."""
    seen = []

    class Base(EZData):
      x = EZField[int](0)

      @classmethod
      def __class_init__(cls, *args, **kwargs) -> None:
        seen.append([field.fieldOwner for field in cls.fields])

    class Sub(Base):
      y = EZField[int](0)

    self.assertEqual(seen, [[Base], [Sub, Sub]])
    self.assertIs(Base.fields[0].fieldOwner, Base)
