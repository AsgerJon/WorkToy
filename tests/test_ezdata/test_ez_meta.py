"""
TestEZMeta tests 'EZMeta' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import TypeSig
from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace
from worktoy.mcls import BaseMeta
from worktoy.waitaminute.meta import ShadowedClassHook
from . import EzdataTest, Point2D, Circle, Vector, FrozenVector, Vector3


class TestEZMeta(EzdataTest):
  """
  'EZMeta' gives a dataclass its introspection: the fields, the
  signature and the three option flags; iterating, measuring and
  searching the class run over its fields; every field knows its
  owner; and 'isCongruent' decides which classes may compare equal.
  The tests pin each of these and the class hooks the metaclass keeps
  for itself.
  """

  def test_accessors(self) -> None:
    self.assertIsSubclass(EZMeta, BaseMeta)
    self.assertEqual([f.fieldName for f in Point2D.fields], ['x', 'y'])
    self.assertEqual(Point2D.sig, TypeSig(float, float))
    self.assertEqual(Circle.sig, TypeSig(Point2D, float))
    self.assertEqual(EZData.sig, TypeSig())
    self.assertFalse(Point2D.isFrozen)
    self.assertTrue(Circle.isFrozen)
    self.assertTrue(Circle.kwOnly)
    self.assertFalse(Circle.isOrdered)

  def test_class_iteration_length_and_membership(self) -> None:
    self.assertEqual([*Point2D], [*Point2D.fields])
    self.assertEqual(len(Point2D), 2)
    self.assertEqual(len(Vector3), 3)
    self.assertEqual(len(EZData), 0)
    field = Point2D.__ez_fields__['x']
    self.assertIn(field, Point2D)
    self.assertNotIn(field.clone(), Point2D)
    self.assertNotIn(Vector.__ez_fields__['x'], Point2D)

    class Agreeing:
      def __eq__(self, other: object) -> bool:
        return True

    self.assertTrue(Agreeing() == field)
    self.assertNotIn(Agreeing(), Point2D)
    self.assertNotIn(field, EZData)

  def test_prepare(self) -> None:
    space = EZMeta.__prepare__('A', (Point2D,), frozen=True)
    self.assertIs(type(space), EZSpace)
    self.assertIs(space.getMetaclass(), EZMeta)
    self.assertEqual(space.getKwargs(), {'frozen': True})
    self.assertEqual([*space.getBaseFields()], ['x', 'y'])
    self.assertIs(EZMeta.getNamespaceClass(), EZSpace)

  def test_owners_bound_before_class_init(self) -> None:
    self.assertIs(Vector3.__ez_fields__['x'].fieldOwner, Vector3)
    self.assertIs(Vector.__ez_fields__['x'].fieldOwner, Vector)
    seen = []

    class A(EZData):
      x = EZField[int](1)

      @classmethod
      def __class_init__(cls, name: str, bases: tuple, space, **kw) -> None:
        seen.append((name, cls.fields[0].fieldOwner))

    self.assertEqual(seen, [('A', A)])

  def test_congruence(self) -> None:
    self.assertTrue(Vector.isCongruent(Vector))
    self.assertTrue(Vector.isCongruent(FrozenVector))
    self.assertTrue(FrozenVector.isCongruent(Vector))
    self.assertFalse(Vector.isCongruent(Vector3))
    self.assertFalse(Vector3.isCongruent(Vector))
    self.assertFalse(Vector.isCongruent(Point2D))
    self.assertFalse(Vector.isCongruent(int))
    self.assertFalse(Vector.isCongruent(5))
    self.assertFalse(Vector.isCongruent(Vector(1, 2)))

  def test_collection_hooks_kept_by_the_metaclass(self) -> None:
    for name in ('__class_iter__', '__class_len__', '__class_contains__'):
      with self.subTest(name=name):
        with self.assertRaises(ShadowedClassHook) as context:
          type('A', (EZData,), {name: classmethod(lambda cls: ())})
        self.assertEqual(context.exception.className, 'A')
        self.assertEqual(context.exception.hookName, name)
        self.assertEqual(context.exception.metaclassName, 'EZMeta')
        self.assertEqual(context.exception.methodName,
                         name.replace('class_', ''))
        self.assertIn("The class body of 'A' binds '%s'" % name,
                      str(context.exception))
        self.assertIn("'EZMeta' implements '%s'"
                      % name.replace('class_', ''), str(context.exception))

    class B(EZData):
      x = 1

      @classmethod
      def __class_str__(cls) -> str:
        return 'dataclass B'

    self.assertEqual(str(B), 'dataclass B')
    self.assertEqual(len(B), 1)

  def test_random_bodies(self) -> None:
    self.randomWord.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    cls = EZMeta('R', (EZData,), {word: 1.5 for word in words})
    self.assertEqual(len(cls), len(words))
    self.assertEqual(cls.sig, TypeSig(*(float for _ in words)))
    for field in cls:
      with self.subTest(field=field.fieldName):
        self.assertIs(field.fieldOwner, cls)
        self.assertIn(field, cls)
