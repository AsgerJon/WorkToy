"""
TestFrozenClassAttribute subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that a frozen 'EZData' instance works as a class
attribute, as in 'class Palette: RED = RGB(255, 0, 0)'. An 'EZData'
instance is an 'Object', so Python calls its '__set_name__' when a class
body holds it, and reading it through an instance runs the context
bookkeeping of 'Object.__get__'. Both used to write onto the value
through its generated '__setattr__', which a frozen class refuses: the
first failed the class body, the second failed every read through an
instance. The bookkeeping of 'Object' now bypasses the '__setattr__' of
the subclass, so neither touches the frozen guard.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError

from . import EZTest


class FrozenRGB(EZData, frozen=True):
  """FrozenRGB is a frozen colour held as a class attribute below."""

  r = EZField[int](0)
  g = EZField[int](0)
  b = EZField[int](0)


RED = FrozenRGB(255, 0, 0)


class TestFrozenClassAttribute(EZTest):
  """
  TestFrozenClassAttribute provides tests for frozen 'EZData' instances
  held as class attributes.
  """

  def test_class_creation(self) -> None:
    """A class body holding a frozen instance builds, whether the class
    is a plain class, a 'BaseObject' or an 'EZData' class. In the first
    two the instance is a class attribute; in an 'EZData' class it is a
    bare value like any other, so it becomes a field with the instance as
    its default (item 26, decided 2026-09-29)."""

    class Palette:
      red = RED

    class Theme(BaseObject):
      red = RED

    class Swatch(EZData):
      red = RED

    for owner in (Palette, Theme):
      self.assertIs(owner.__dict__['red'], RED)
    self.assertEqual([f.fieldName for f in Swatch.fields], ['red'])
    self.assertEqual(Swatch().red, RED)

  def test_read_through_class(self) -> None:
    """Reading the attribute through the class returns the instance."""

    class Palette:
      red = RED

    self.assertIs(Palette.red, RED)

  def test_read_through_instance(self) -> None:
    """Reading the attribute through an instance of the class, directly
    or from a method, returns the instance."""

    class Palette:
      red = RED

      def getRed(self) -> FrozenRGB:
        return self.red

    self.assertIs(Palette().red, RED)
    self.assertIs(Palette().getRed(), RED)

  def test_value_unchanged(self) -> None:
    """Holding and reading the instance leaves its fields, equality and
    hash as they were."""

    class Palette:
      red = RED

    _ = Palette().red
    self.assertEqual((RED.r, RED.g, RED.b), (255, 0, 0))
    self.assertEqual(RED, FrozenRGB(255, 0, 0))
    self.assertEqual(hash(RED), hash(FrozenRGB(255, 0, 0)))

  def test_write_through_instance_refused(self) -> None:
    """Assigning or deleting the attribute through an instance raises
    'ReadOnlyError' or 'ProtectedError', as for any 'Object' held as a
    class attribute, instead of the frozen guard's 'AttributeError'
    about the bookkeeping. Item 26 of the 1.1 audit asks whether values
    should act as descriptors at all; this pins the behaviour until
    then."""

    class Palette:
      red = RED

    palette = Palette()
    with self.assertRaises(ReadOnlyError):
      palette.red = FrozenRGB(0, 0, 255)
    with self.assertRaises(ProtectedError):
      del palette.red
    self.assertIs(palette.red, RED)
