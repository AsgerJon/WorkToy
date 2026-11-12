"""
TestEZSpace tests 'EZSpace' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace, EZHook
from worktoy.waitaminute.ezdata import DuplicateError, ReservedFieldError
from . import EzdataTest, Point2D, Vector, Vector3, Labelled

shared = EZField[int](1)


class TestEZSpace(EzdataTest):
  """
  'EZSpace' keeps the own fields of a body apart from the inherited
  ones, clones what it inherits, refuses a field at a reserved name or
  at a name bound twice, and orders the fields from the most general
  class to the most specific. The tests pin the registries, the two
  refusals, the clone of a field bound before, and the order.
  """

  def test_registries(self) -> None:
    space = Point2D.__namespace__
    self.assertIsInstance(space, EZSpace)
    self.assertEqual([*space.getEZFields()], ['x', 'y'])
    self.assertEqual(space.getBaseFields(), {})
    self.assertEqual(space.getFields(), space.getEZFields())
    self.assertIsNot(space.getFields(), space.getEZFields())
    fresh = EZSpace(EZMeta, 'A', ())
    self.assertEqual(fresh.getEZFields(), {})
    self.assertEqual(fresh.getBaseFields(), {})
    self.assertEqual(fresh.getFields(), {})
    self.assertIsInstance(EZSpace.__dict__['ezHook'], EZHook)
    self.assertEqual(len(EZSpace.__reserved_ez_names__), 7)
    self.assertEqual(len(EZSpace.__reserved_ez_methods__), 11)
    self.assertEqual(len(EZSpace.__reserved_ez_attributes__), 6)

  def test_inherited_fields_are_clones(self) -> None:
    space = Vector3.__namespace__
    self.assertEqual([*space.getBaseFields()], ['x', 'y'])
    self.assertEqual([*space.getEZFields()], ['z'])
    self.assertEqual([*space.getFields()], ['x', 'y', 'z'])
    inherited = space.getBaseFields()['x']
    original = Vector.__namespace__.getEZFields()['x']
    self.assertIsNot(inherited, original)
    self.assertEqual(inherited.fieldName, 'x')
    self.assertIs(inherited.fieldOwner, Vector3)
    self.assertIs(original.fieldOwner, Vector)

  def test_reserved_field_name_refused(self) -> None:
    with self.assertRaises(ReservedFieldError) as context:
      class A(EZData):
        asDict = 1

    exception = context.exception
    self.assertEqual(exception.fieldName, 'asDict')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("EZData class 'A', the name 'asDict' is reserved",
                  str(exception))
    self.assertIn("'replace'", str(exception))
    space = EZSpace(EZMeta, 'B', ())
    for name in EZSpace.__reserved_ez_names__:
      with self.subTest(name=name):
        with self.assertRaises(ReservedFieldError) as context:
          space.registerEZField(name, EZField[int](1))
        self.assertEqual(context.exception.fieldName, name)
        self.assertIs(context.exception.space, space)
        self.assertIn("EZData class 'B', the name '%s' is reserved" % name,
                      str(context.exception))
    #  The text passes through 'textFmt', as every message does: a run
    #  of spaces in a quoted name comes out as one.
    space = EZSpace(EZMeta, 'Wide  Gap', ())
    with self.assertRaises(ReservedFieldError) as context:
      space.registerEZField('asDict', EZField[int](1))
    self.assertIn("EZData class 'Wide Gap', the name 'asDict' is reserved",
                  str(context.exception))
    self.assertEqual(context.exception.msg, str(context.exception))

  def test_duplicate_field_refused(self) -> None:
    with self.assertRaises(DuplicateError) as context:
      class A(EZData):
        x = 1
        x = 2

    exception = context.exception
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("class 'A', the already existing attribute name 'x'",
                  str(exception))
    space = EZSpace(EZMeta, 'B', ())
    space.registerEZField('x', EZField[int](1))
    with self.assertRaises(DuplicateError) as context:
      space.registerEZField('x', EZField[int](2))
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIs(context.exception.space, space)
    self.assertIn("class 'B', the already existing attribute name 'x'",
                  str(context.exception))

  def test_field_bound_before_is_cloned(self) -> None:
    class A(EZData):
      a = EZField[int](1)
      b = a
      v = shared

    class B(EZData):
      w = shared

    self.assertIsNot(A.__ez_fields__['a'], A.__ez_fields__['b'])
    self.assertEqual(A.__ez_fields__['b'].fieldName, 'b')
    self.assertEqual(A(1, 2, 3).asTuple(), (1, 2, 3))
    self.assertIs(A.__ez_fields__['v'], shared)
    self.assertEqual(shared.fieldName, 'v')
    self.assertIsNot(B.__ez_fields__['w'], shared)
    self.assertEqual(B.__ez_fields__['w'].fieldName, 'w')
    self.assertIs(B.__ez_fields__['w'].fieldOwner, B)

  def test_nearest_decides_the_field_farthest_its_position(self) -> None:
    class A(EZData):
      a = 1
      b = 2

    class B(A):
      b = 3.0
      c = 4

    self.assertEqual([*B.__ez_fields__], ['a', 'b', 'c'])
    self.assertIs(B.__ez_fields__['b'].fieldType, float)
    self.assertEqual(B().asTuple(), (1, 3.0, 4))
    self.assertEqual([*B.__namespace__.getBaseFields()], ['a', 'b'])
    self.assertEqual([*B.__namespace__.getEZFields()], ['b', 'c'])

  def test_fields_run_from_the_most_general_class(self) -> None:
    class X(EZData):
      x1 = 1

    class Y(EZData):
      y1 = 2

    class Both(X, Y):
      own = 3

    self.assertEqual([*Both.__ez_fields__], ['y1', 'x1', 'own'])
    self.assertEqual(Both.__mro__[1:3], (X, Y))
    self.assertEqual(Both().asTuple(), (2, 1, 3))

  def test_plain_bases_declare_nothing(self) -> None:
    space = Labelled.__namespace__
    self.assertEqual(space.getBaseFields(), {})
    self.assertEqual([*space.getEZFields()], ['label', 'count'])

  def test_random_registrations(self) -> None:
    space = EZSpace(EZMeta, 'R', ())
    self.randomWord.size = 6
    words = [*dict.fromkeys(self.randomWord.row)]
    for word in words:
      space.registerEZField(word, EZField[str](word))
    self.assertEqual([*space.getFields()], words)
    for word in words:
      with self.subTest(word=word):
        self.assertEqual(space.getEZFields()[word].fieldName, word)
