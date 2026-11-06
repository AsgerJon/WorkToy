"""
TestEZFieldDeclare tests the declaration, the slots and the text of an
'EZField' from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import Generic, TypeVar
from unittest import skipIf

from worktoy.core.sentinels import THIS, ARGS
from worktoy.ezdata import EZField
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import UncheckableType
from . import EzdataTest, Point2D, Circle


class TestEZFieldDeclare(EzdataTest):
  """
  'EZField[T](...)' is the declaration: the subscript sets the type and
  refuses what is no class, what cannot be checked and the class being
  declared; the call binds the recipe. The tests pin the subscript, the
  call, the bare-value constructor, the clone, the six getters with
  their refusals, the refusal outside a dataclass body, and the texts.
  """

  def test_subscript_sets_the_type(self) -> None:
    field = EZField[int]
    self.assertIsInstance(field, EZField)
    self.assertIs(field.fieldType, int)
    with self.assertRaises(MissingVariable) as context:
      _ = field.posArgs
    self.assertIs(context.exception.instance, field)
    self.assertEqual(context.exception.varName, '__pos_args__')
    self.assertEqual(context.exception.expectedTypes, (tuple,))
    self.assertEqual(str(context.exception),
                     "Missing 'EZField.__pos_args__: tuple'!")
    with self.assertRaises(MissingVariable) as context:
      _ = field.keyArgs
    self.assertIs(context.exception.instance, field)
    self.assertEqual(context.exception.varName, '__key_args__')
    self.assertEqual(context.exception.expectedTypes, (dict,))
    self.assertEqual(str(context.exception),
                     "Missing 'EZField.__key_args__: dict'!")
    self.assertIsSubclass(EZField, Generic)
    self.assertIsSubclass(EZField, BaseObject)

  def assertSubscriptRefused(self, bad: object) -> None:
    """The subscript raises 'TypeException' naming the bad type."""
    with self.assertRaises(TypeException) as context:
      _ = EZField[bad]
    self.assertEqual(context.exception.varName, 'fieldType')
    self.assertIs(context.exception.actualObject, bad)
    self.assertIs(context.exception.actualType, type(bad))
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'fieldType' to be an instance of 'type'",
                  str(context.exception))
    self.assertIn("of type '%s'" % type(bad).__name__,
                  str(context.exception))

  def test_subscript_refusals(self) -> None:
    for bad in (TypeVar('Q'), 5):
      with self.subTest(bad=str(bad)):
        self.assertSubscriptRefused(bad)
    with self.assertRaises(TypeError) as context:
      _ = EZField[THIS]
    self.assertIn("The subscript 'EZField[THIS]' names 'THIS', the class "
                  "being declared, as the field type",
                  str(context.exception))
    self.assertNotIsInstance(context.exception, TypeException)

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_generic_alias_subscript_refused(self) -> None:
    self.assertSubscriptRefused(list[int])

  def test_uncheckable_type_refused(self) -> None:
    class RefusingMeta(type):
      def __instancecheck__(cls, obj: object) -> bool:
        raise TypeError('no instance checks here')

    class Uncheckable(metaclass=RefusingMeta):
      """A class 'isinstance' refuses."""

    with self.assertRaises(UncheckableType) as context:
      _ = EZField[Uncheckable]
    self.assertIs(context.exception.entry, Uncheckable)
    self.assertEqual(context.exception.declaration, 'EZField[Uncheckable]')
    self.assertIsNone(context.exception.position)
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("The box 'EZField[Uncheckable]' declares 'Uncheckable' "
                  "as its field type, which 'isinstance' refuses: no "
                  "instance checks here", str(context.exception))

  def test_call_binds_the_recipe(self) -> None:
    field = EZField[int](1, k=2)
    self.assertEqual(field.posArgs, (1,))
    self.assertEqual(field.keyArgs, {'k': 2})
    self.assertIs(field(3), field)
    self.assertEqual(field.posArgs, (3,))
    self.assertEqual(field.keyArgs, {})
    plain = EZField(4, k=5)
    self.assertEqual(plain.posArgs, (4,))
    self.assertEqual(plain.keyArgs, {'k': 5})
    with self.assertRaises(MissingVariable) as context:
      _ = plain.fieldType
    self.assertIs(context.exception.instance, plain)
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertEqual(str(context.exception),
                     "Missing 'EZField.__field_type__: type'!")

  def test_from_value(self) -> None:
    field = EZField.fromValue(2.5)
    self.assertIs(field.fieldType, float)
    self.assertEqual(field.posArgs, (2.5,))
    self.assertEqual(field.keyArgs, {})
    self.assertEqual(field.defaultValue, 2.5)

  def test_clone(self) -> None:
    original = Point2D.__ez_fields__['x']
    for clone in (original.clone(), EZField.clone_(original)):
      with self.subTest(clone=repr(clone)):
        self.assertIsNot(clone, original)
        self.assertIs(clone.fieldType, float)
        self.assertEqual(clone.posArgs, (0.0,))
        self.assertEqual(clone.keyArgs, {})
        with self.assertRaises(MissingVariable) as context:
          _ = clone.fieldName
        self.assertIs(context.exception.instance, clone)
        self.assertEqual(context.exception.varName, '__field_name__')
        self.assertEqual(context.exception.expectedTypes, (str,))
        self.assertEqual(str(context.exception),
                         "Missing 'EZField.__field_name__: str'!")
        with self.assertRaises(MissingVariable) as context:
          _ = clone.fieldOwner
        self.assertIs(context.exception.instance, clone)
        self.assertEqual(context.exception.varName, '__field_owner__')
        self.assertEqual(context.exception.expectedTypes, (type,))
        self.assertEqual(str(context.exception),
                         "Missing 'EZField.__field_owner__: type'!")

  def test_bound_getters(self) -> None:
    field = Circle.__ez_fields__['radius']
    self.assertIs(field.fieldOwner, Circle)
    self.assertEqual(field.fieldName, 'radius')
    self.assertIs(field.fieldType, float)
    self.assertEqual(field.posArgs, (1.0,))
    self.assertEqual(field.keyArgs, {})
    self.assertEqual(field.defaultValue, 1.0)
    self.assertIs(Point2D.__ez_fields__['y'],
                  Point2D.__dict__['__ez_fields__']['y'])

  def test_getters_refuse_wrong_types(self) -> None:
    field = EZField[int](1)
    slots = (
      ('__field_owner__', 'fieldOwner', type),
      ('__field_name__', 'fieldName', str),
      ('__field_type__', 'fieldType', type),
      ('__pos_args__', 'posArgs', tuple),
      ('__key_args__', 'keyArgs', dict),
    )
    for slot, name, expected in slots:
      with self.subTest(name=name):
        setattr(field, slot, 1.5)
        with self.assertRaises(TypeException) as context:
          getattr(field, name)
        self.assertEqual(context.exception.varName, slot)
        self.assertEqual(context.exception.actualObject, 1.5)
        self.assertIs(context.exception.actualType, float)
        self.assertEqual(context.exception.expectedTypes, (expected,))
        self.assertIn("'%s' to be an instance of '%s'"
                      % (slot, expected.__name__), str(context.exception))
        self.assertIn("received object: '1.5' of type 'float'",
                      str(context.exception))

  def test_refused_outside_a_dataclass_body(self) -> None:
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        x = EZField[int](1)

    exception = context.exception.__cause__ or context.exception
    self.assertIn("'Plain' is bound to one at 'x' and 'Plain' is no "
                  "'EZData' subclass", str(exception))
    with self.assertRaises(TypeError) as context:
      EZField[int](1).hookSetName(int, 'x')
    self.assertIn("'int' is bound to one at 'x' and 'int' is no "
                  "'EZData' subclass", str(context.exception))

  def test_str(self) -> None:
    self.assertEqual(str(Point2D.__ez_fields__['x']),
                     'Point2D.x: float(0.0)')
    self.assertEqual(str(EZField[int](1, k=2)),
                     'EZField.<unbound>: int(1, k=2)')
    self.assertEqual(str(EZField[int](k=2)), 'EZField.<unbound>: int(k=2)')
    self.assertEqual(str(EZField[int]()), 'EZField.<unbound>: int()')
    self.assertEqual(str(EZField[int]), 'EZField.<unbound>: int()')
    self.assertEqual(str(EZField(1)), 'EZField.<unbound>: object(1)')

  def test_repr(self) -> None:
    self.assertEqual(repr(Point2D.__ez_fields__['x']), 'EZField[float](0.0)')
    self.assertEqual(repr(EZField[int](1, k=2)), 'EZField[int](1, k=2)')
    self.assertEqual(repr(EZField[int](k=2)), 'EZField[int](k=2)')
    self.assertEqual(repr(EZField[int]()), 'EZField[int]()')
    self.assertEqual(repr(EZField[int]), 'EZField[int]()')
    self.assertEqual(repr(EZField(1)), 'EZField[object](1)')

  def test_random_recipes(self) -> None:
    self.randomWord.size = 5
    self.randomInteger.size = 5
    for word, n in zip(self.randomWord.row, self.randomInteger.row):
      field = EZField[str](word, n)
      with self.subTest(word=word):
        self.assertEqual(field.posArgs, (word, n))
        self.assertEqual(repr(field), 'EZField[str](%r, %r)' % (word, n))

  def test_variadic_and_this_refused_in_words(self) -> None:
    with self.assertRaises(TypeError) as context:
      _ = EZField[ARGS]
    self.assertIn("The entry at position 0 of the signature is the "
                  "sentinel 'ARGS'", str(context.exception))
    with self.assertRaises(TypeError) as context:
      _ = EZField[THIS]
    self.assertIn('EZField[THIS]', str(context.exception))
    self.assertNotIn('%s', str(context.exception))
