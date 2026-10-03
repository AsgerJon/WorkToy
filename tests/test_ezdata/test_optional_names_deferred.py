"""
TestOptionalNamesDeferred subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins how an 'EZData' class settles the optional names EZData
can generate: '__field_pairs__', 'asDict', 'asTuple', 'replace',
'__repr__', '__str__' and '__match_args__'. The class body's own wins;
failing that, the first hand-written one along the method resolution
order, in an EZData base or a plain base; failing that, EZData generates
one and records the name in '__ez_generated__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class TestOptionalNamesDeferred(EZTest):
  """
  TestOptionalNamesDeferred provides tests for the optional names of
  'EZData' classes and the bases they defer to.
  """

  def test_ezdata_base_helper_inherited(self) -> None:
    """
    Testing that a subclass uses the helpers an EZData base wrote by
    hand, including through '__field_pairs__' in the generated '__str__'.
    """

    class Base(EZData):
      x = EZField[int](1)

      def asDict(self) -> str:
        return 'custom asDict'

      def __field_pairs__(self) -> list:
        return ['custom pairs']

    class Sub(Base):
      pass

    self.assertEqual(Sub().asDict(), 'custom asDict')
    self.assertEqual(str(Sub()), '<Sub: custom pairs>')

  def test_inherited_through_two_levels(self) -> None:
    """
    Testing that a hand-written helper reaches a subclass two levels down.
    """

    class Base(EZData):
      x = EZField[int](1)

      def asTuple(self) -> str:
        return 'custom asTuple'

    class Middle(Base):
      y = EZField[int](2)

    class Leaf(Middle):
      pass

    self.assertEqual(Leaf().asTuple(), 'custom asTuple')

  def test_plain_base_after_ezdata(self) -> None:
    """
    Testing that a plain base's hand-written helper is used when the plain
    base is listed after 'EZData'.
    """

    class Named:
      def __repr__(self) -> str:
        return 'named'

    class Point(EZData, Named):
      x = EZField[int](1)

    self.assertEqual(repr(Point()), 'named')

  def test_plain_base_before_ezdata(self) -> None:
    """
    Testing that a plain base's hand-written helper is used when the plain
    base is listed before 'EZData'.
    """

    class Named:
      def __str__(self) -> str:
        return 'named'

    class Point(Named, EZData):
      x = EZField[int](1)

    self.assertEqual(str(Point()), 'named')

  def test_generated_base_helper_skipped(self) -> None:
    """
    Testing that a helper an EZData base received generated does not hide
    a plain base's hand-written one further along.
    """

    class Base(EZData):
      x = EZField[int](1)

    class Named:
      def __repr__(self) -> str:
        return 'named'

    class Point(Base, Named):
      pass

    self.assertEqual(repr(Point()), 'named')

  def test_nearest_hand_written_wins(self) -> None:
    """
    Testing that of two hand-written helpers along the bases, the nearest
    in the method resolution order is used.
    """

    class Base(EZData):
      x = EZField[int](1)

      def __repr__(self) -> str:
        return 'from base'

    class Named:
      __repr__ = lambda self: 'from plain base'

    class Point(Base, Named):
      pass

    self.assertEqual(repr(Point()), 'from base')

  def test_class_body_wins(self) -> None:
    """
    Testing that the class body's own helper wins over a base's.
    """

    class Base(EZData):
      x = EZField[int](1)
      __repr__ = lambda self: 'from base'

    class Sub(Base):
      def __repr__(self) -> str:
        return 'from body'

    self.assertEqual(repr(Sub()), 'from body')

  def test_generated_without_hand_written(self) -> None:
    """
    Testing that without a hand-written helper EZData generates each, and
    records the generated names in '__ez_generated__'.
    """

    class Point(EZData):
      x = EZField[int](1)
      asDict = lambda self: 'custom'

    self.assertEqual(Point().asTuple(), (1,))
    self.assertEqual(repr(Point()), 'Point(1)')
    self.assertIn('asTuple', Point.__ez_generated__)
    self.assertIn('__match_args__', Point.__ez_generated__)
    self.assertNotIn('asDict', Point.__ez_generated__)

  def test_match_args_inherited_from_ezdata_base(self) -> None:
    """
    Testing that a subclass uses the '__match_args__' its EZData base set
    by hand, rather than a generated one.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)
      __match_args__ = ('y',)

    class Point3D(Point):
      z = EZField[float](0.0)

    self.assertEqual(Point3D.__match_args__, ('y',))

  def test_match_args_from_plain_base(self) -> None:
    """
    Testing that a '__match_args__' a plain base sets is used.
    """

    class Matching:
      __match_args__ = ('y', 'x')

    class Point(EZData, Matching):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    self.assertEqual(Point.__match_args__, ('y', 'x'))

  def test_match_args_generated_for_generated_base(self) -> None:
    """
    Testing that a subclass of a class whose '__match_args__' was generated
    receives a generated tuple of all its own fields.
    """

    class Point(EZData):
      x = EZField[float](0.0)

    class Point3D(Point):
      z = EZField[float](0.0)

    self.assertEqual(Point3D.__match_args__, ('x', 'z'))
