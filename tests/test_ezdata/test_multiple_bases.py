"""
TestMultipleBases subclasses 'EZTest' from the 'tests.test_ezdata' package
and pins that an 'EZData' class may derive from several 'EZData' classes
that each declare fields. The combined class gathers the fields of every
base in the order 'dataclasses' uses, which walks the method resolution
order from the far end, so a base listed further right contributes its
fields first. When several classes declare the same name, the class
nearest in the method resolution order decides the field, just as
attribute lookup would find it. The combined classes are built inside
the tests, so a class that fails to build fails its own test rather than
the whole file.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class Named(EZData):
  """Named declares a 'str' field and a method reading it."""

  name = EZField[str]('anon')

  def greeting(self) -> str:
    return 'hello %s' % self.name


class Sized(EZData):
  """Sized declares an 'int' field."""

  size = EZField[int](0)


class IntTag(EZData):
  """IntTag declares 'tag' as an 'int' field."""

  tag = EZField[int](1)


class StrTag(EZData):
  """StrTag declares 'tag' as a 'str' field, clashing with 'IntTag'."""

  tag = EZField[str]('one')


class Root(EZData):
  """Root is the shared base at the top of a diamond."""

  root = EZField[int](0)


class Left(Root):
  """Left adds a field on one side of the diamond."""

  left = EZField[int](0)


class Right(Root):
  """Right adds a field on the other side of the diamond."""

  right = EZField[int](0)


class Tuned(Root):
  """Tuned redeclares the inherited 'root' field with another default."""

  root = EZField[int](5)


class TestMultipleBases(EZTest):
  """
  TestMultipleBases provides tests for 'EZData' classes combining several
  'EZData' bases that declare fields.
  """

  def test_fields_from_both_bases(self) -> None:
    """
    Combining 'Named' and 'Sized' gives a class with both fields, the
    field of the right-hand base first, and positional construction
    follows that order.
    """

    class Labelled(Named, Sized):
      pass

    self.assertEqual(tuple(Labelled.__ez_fields__), ('size', 'name'))
    labelled = Labelled(3, 'box')
    self.assertEqual(labelled.size, 3)
    self.assertEqual(labelled.name, 'box')
    self.assertEqual(labelled.asDict(), {'size': 3, 'name': 'box'})
    self.assertEqual(repr(labelled), "Labelled(3, 'box')")

  def test_keywords_and_defaults(self) -> None:
    """
    Keywords reach the fields of either base, and an omitted field takes
    the default its own base declared.
    """

    class Labelled(Named, Sized):
      pass

    labelled = Labelled(name='box')
    self.assertEqual(labelled.name, 'box')
    self.assertEqual(labelled.size, 0)
    self.assertEqual(Labelled().name, 'anon')

  def test_combined_instance_serves_both_bases(self) -> None:
    """
    An instance of the combined class is an instance of each base, and a
    method defined on a base reads the field that base declared.
    """

    class Labelled(Named, Sized):
      pass

    labelled = Labelled(3, 'box')
    self.assertIsInstance(labelled, Named)
    self.assertIsInstance(labelled, Sized)
    self.assertEqual(labelled.greeting(), 'hello box')

  def test_leftmost_base_wins_clash(self) -> None:
    """
    When both bases declare 'tag', the combined class has a single 'tag'
    field taken from the base listed first, with that base's type and
    default.
    """

    class Tagged(IntTag, StrTag):
      pass

    tagField, = Tagged.fields
    self.assertEqual(tagField.fieldName, 'tag')
    self.assertIs(tagField.fieldType, int)
    self.assertEqual(Tagged().tag, 1)
    self.assertEqual(Tagged('2').tag, 2)

  def test_diamond(self) -> None:
    """
    In a diamond the shared field appears once. Reading the method
    resolution order from the far end puts the shared 'root' first, then
    the field of the right-hand side, then that of the left-hand side.
    """

    class Diamond(Left, Right):
      pass

    self.assertEqual(tuple(Diamond.__ez_fields__), ('root', 'right', 'left'))
    diamond = Diamond(1, 2, 3)
    self.assertEqual((diamond.root, diamond.right, diamond.left), (1, 2, 3))

  def test_nearest_redeclaration_wins_in_diamond(self) -> None:
    """
    When the right-hand side of a diamond redeclares a field of the
    shared base, the combined class takes the redeclared field, since the
    right-hand side comes before the shared base in the method resolution
    order. The field keeps the position the shared base gave it. Here
    'dataclasses' differs: it also copies the fields the left-hand side
    inherited, so the shared base's version wins there.
    """

    class Diamond(Left, Tuned):
      pass

    self.assertEqual(tuple(Diamond.__ez_fields__), ('root', 'left'))
    self.assertEqual(Diamond().root, 5)

  def test_repeated_base_keeps_order(self) -> None:
    """
    Listing a base again that the method resolution order already holds
    leaves that order unchanged, so the fields must keep their order too.
    'Relabelled' names 'Named' a second time and still has the fields of
    'Labelled' in the same order, exactly as 'dataclasses' gives them.
    Gathering the fields base by base, right to left, would instead pull
    'name' in front of 'size' here.
    """

    class Labelled(Named, Sized):
      pass

    class Relabelled(Labelled, Named):
      pass

    self.assertEqual(tuple(Relabelled.__ez_fields__), ('size', 'name'))
    self.assertEqual(Relabelled(3, 'box').asTuple(), (3, 'box'))

  def test_subclass_of_combined_class(self) -> None:
    """
    A subclass of the combined class keeps every inherited field and
    appends its own after them.
    """

    class Labelled(Named, Sized):
      pass

    class Weighed(Labelled):
      weight = EZField[float](0.0)

    expected = ('size', 'name', 'weight')
    self.assertEqual(tuple(Weighed.__ez_fields__), expected)
    self.assertEqual(Weighed(3, 'box', 1).asTuple(), (3, 'box', 1.0))

  def test_combined_frozen_class(self) -> None:
    """
    The combined class may be frozen. Equal instances hash alike, and
    assignment is refused.
    """

    class FrozenLabel(Named, Sized, frozen=True):
      pass

    first, second = FrozenLabel(3, 'box'), FrozenLabel(3, 'box')
    self.assertEqual(first, second)
    self.assertEqual(hash(first), hash(second))
    with self.assertRaises(AttributeError):
      first.name = 'crate'

  def test_base_without_fields(self) -> None:
    """
    Combining a base that declares fields with one that declares none
    keeps only the declared fields.
    """

    class Empty(EZData):
      pass

    class Combined(Named, Empty):
      pass

    self.assertEqual(tuple(Combined.__ez_fields__), ('name',))
    self.assertEqual(Combined('box').greeting(), 'hello box')
