"""
TestGeneratedQualname subclasses 'EZTest' and pins that the methods EZData
generates carry the qualified name of their class, as a method written in
the class body does. They carried the local name of the factory that made
them, so 'pt.asDict(1)' read 'EZHook.asDictFactory.<locals>.asDict()
takes 1 positional argument'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class Point(EZData, frozen=True, ordered=True):
  """Point is frozen and ordered, so every method is generated."""
  x = EZField[int](0)


class Loose(EZData):
  """Loose is neither frozen nor ordered."""
  x = EZField[int](0)


class Mixin:
  """Mixin writes 'asDict' by hand."""

  def asDict(self) -> dict:
    return dict()


class Mixed(Mixin, EZData):
  """Mixed takes 'asDict' from its plain base."""
  x = EZField[int](0)


class TestGeneratedQualname(EZTest):
  """
  TestGeneratedQualname provides tests for the names of the generated
  methods.
  """

  def test_generated_methods_named(self) -> None:
    """Each generated method is named after the class and itself."""
    names = (
      '__init__', '__iter__', '__len__', '__eq__', '__hash__', '__lt__',
      '__le__', '__gt__', '__ge__', '__setattr__', '__delattr__',
      '__field_pairs__', 'asDict', 'asTuple', 'replace', '__repr__',
      '__str__',
    )
    for name in names:
      with self.subTest(name=name):
        method = Point.__dict__[name]
        self.assertEqual(method.__qualname__, 'Point.%s' % name)
        self.assertEqual(method.__name__, name)

  def test_nested_class_qualname(self) -> None:
    """A class defined in a function prefixes its own qualified name."""

    class Inner(EZData):
      """Inner is defined inside a test."""
      x = EZField[int](0)

    expected = '%s.asDict' % Inner.__qualname__
    self.assertEqual(Inner.__dict__['asDict'].__qualname__, expected)

  def test_setattr_of_loose_class(self) -> None:
    """The '__setattr__' of a class that is not frozen is named too."""
    method = Loose.__dict__['__setattr__']
    self.assertEqual(method.__qualname__, 'Loose.__setattr__')

  def test_shared_function_unchanged(self) -> None:
    """The comparison shared by every unordered class keeps its name."""
    self.assertEqual(Loose.__dict__['__lt__'].__qualname__, '_unorderable')

  def test_hand_written_unchanged(self) -> None:
    """A method taken from a plain base keeps the name it was given."""
    self.assertEqual(Mixed.__dict__['asDict'].__qualname__, 'Mixin.asDict')
    self.assertEqual(Mixed(1).asDict(), dict())
