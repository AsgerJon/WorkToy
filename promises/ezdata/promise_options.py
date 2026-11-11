"""
PromiseOptions promises the class keywords of an 'EZData' class, from
'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData, fields
from worktoy.waitaminute.ezdata import KwargsOnlyException


class PromiseOptions(TestCase):
  """
  Three class keywords change an 'EZData' class, each under several
  names. 'frozen=True', or 'immutable' or 'hashable', refuses every
  assignment and deletion with 'AttributeError' and makes the instances
  hashable, equal instances alike. 'ordered=True', or 'order', 'sortable'
  or 'comparable', compares instances field by field in order, and is
  inherited. 'kwOnly=True', or 'keywordOnly' or 'kw_only', takes the
  fields by keyword alone, raising 'KwargsOnlyException' for a
  positional argument. The class answers 'isFrozen', 'isOrdered' and
  'kwOnly'. A subclass adds fields of its own to those it inherits, and
  several 'EZData' classes may be combined as bases. Source: the
  docstrings of 'EZData', 'EZMeta' and 'EZHook'.
  """

  def test_frozen(self) -> None:
    for keyword in ('frozen', 'immutable', 'hashable'):
      with self.subTest(keyword=keyword):
        Point = type('Point', (EZData,), {'x': 0.0}, **{keyword: True})
        point = Point(1)
        self.assertTrue(Point.isFrozen)
        with self.assertRaises(AttributeError):
          point.x = 2
        with self.assertRaises(AttributeError):
          point.note = 'scratch'
        with self.assertRaises(AttributeError):
          del point.x
        self.assertEqual(hash(point), hash(Point(1)))

  def test_ordered(self) -> None:
    for keyword in ('ordered', 'order', 'sortable', 'comparable'):
      with self.subTest(keyword=keyword):
        Version = type('Version', (EZData,), {'major': 0, 'minor': 0},
                       **{keyword: True})
        self.assertTrue(Version.isOrdered)
        self.assertLess(Version(1, 9), Version(2, 0))
        self.assertLess(Version(1, 2), Version(1, 3))
        self.assertGreater(Version(2, 0), Version(1, 9))
        versions = sorted([Version(2, 0), Version(1, 5)])
        self.assertEqual(versions[0].major, 1)

  def test_ordered_inherited(self) -> None:
    class Version(EZData, ordered=True):
      major = 0

    class Release(Version):
      patch = 0

    self.assertTrue(Release.isOrdered)
    self.assertLess(Release(1, 1), Release(1, 2))

  def test_keyword_only(self) -> None:
    for keyword in ('kwOnly', 'keywordOnly', 'kw_only'):
      with self.subTest(keyword=keyword):
        Config = type('Config', (EZData,), {'port': 80}, **{keyword: True})
        self.assertTrue(Config.kwOnly)
        self.assertEqual(Config(port=8080).port, 8080)
        with self.assertRaises(KwargsOnlyException) as context:
          Config(8080)
        self.assertIs(context.exception.cls, Config)
        self.assertEqual(context.exception.argCount, 1)

  def test_inheritance(self) -> None:
    class Point(EZData):
      x = 0.0
      y = 0.0

    class Point3D(Point):
      z = 0.0

    class Named(EZData):
      name = ''

    class NamedPoint(Point, Named):
      pass

    self.assertEqual([f.fieldName for f in fields(Point3D)], ['x', 'y', 'z'])
    self.assertEqual(tuple(Point3D(1, 2, 3)), (1.0, 2.0, 3.0))
    self.assertEqual({f.fieldName for f in fields(NamedPoint)},
                     {'x', 'y', 'name'})
