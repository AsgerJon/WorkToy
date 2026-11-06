"""
TestFastBoxDeclare tests the declaration of a 'FastBox' from
'worktoy.desc': the subscript, the parentheses, the placement and the
clone.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeVar

from worktoy.core.sentinels import THIS, DELETED
from worktoy.desc import FastBox
from worktoy.desc._root_alias import _RootAlias
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import UncheckableType
from worktoy.waitaminute.desc import SharedDescriptor, MissingInstanceDict
from worktoy.waitaminute.dispatch import TypeCastException
from . import DescTest

T = TypeVar('T')


class TestFastBoxDeclare(DescTest):
  """
  A 'FastBox' is declared with a subscript naming the class of its
  values and parentheses holding one shared value, cast once, or
  nothing for a new value per instance; the mistakes are refused on the
  declaration line or as the class is created. The tests pin the
  subscripts a box, an alias and a refusal come from, every shape of the
  parentheses, every refusal of the placement, and the clone.
  """

  def test_subscript_builds_box(self) -> None:
    box = FastBox[int]
    self.assertIsInstance(box, FastBox)
    self.assertIs(box.__field_type__, int)
    self.assertIs(FastBox[THIS].__field_type__, THIS)
    self.assertIsInstance(FastBox[T], _RootAlias)

  def test_bad_subscripts_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      _ = FastBox[DELETED]
    self.assertIn("'FastBox[DELETED]' names a sentinel",
                  str(context.exception))

    class Refusing(type):
      def __instancecheck__(cls, instance: object) -> bool:
        raise TypeError('no instance checks')

    Odd = Refusing('Odd', (), {})
    with self.assertRaises(UncheckableType) as context:
      _ = FastBox[Odd]
    self.assertEqual(context.exception.declaration, 'FastBox[Odd]')
    self.assertIsNone(context.exception.position)
    self.assertIs(context.exception.entry, Odd)
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("box 'FastBox[Odd]'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      _ = FastBox[int, str]
    self.assertEqual(context.exception.varName, 'fieldType')
    self.assertEqual(context.exception.actualObject, (int, str))
    self.assertIs(context.exception.actualType, tuple)
    self.assertEqual(context.exception.expectedTypes, (type, TypeVar))
    self.assertIn("'fieldType'", str(context.exception))
    self.assertIsInstance(context.exception.__cause__, TypeError)

  def test_parentheses(self) -> None:
    self.assertEqual(FastBox[float](1).__declared_value__, (1.0,))
    self.assertEqual(FastBox[list]().__declared_value__, ())
    self.assertIsNone(FastBox[int].__declared_value__)
    with self.assertRaises(TypeCastException) as context:
      FastBox[int](1.5)
    self.assertIs(context.exception.type_, int)
    self.assertEqual(context.exception.arg, 1.5)
    self.assertEqual(str(context.exception),
                     "Unable to cast value '1.5' to type 'int'!")
    with self.assertRaises(TypeError) as context:
      FastBox[int](key=1)
    self.assertIn("'FastBox[int]' takes one value", str(context.exception))
    with self.assertRaises(TypeError) as context:
      FastBox[int](1, 2)
    self.assertIn("'FastBox[int]' takes one value", str(context.exception))
    with self.assertRaises(TypeError) as context:
      FastBox[list]([])
    self.assertIn('cannot be hashed', str(context.exception))
    self.assertIsInstance(context.exception.__cause__, TypeError)
    with self.assertRaises(MissingVariable) as context:
      FastBox.__new__(FastBox)(1)
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertIsInstance(context.exception.instance, FastBox)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertEqual(str(context.exception),
                     "Missing 'FastBox.__field_type__: type'!")

  def test_placed_box_refuses_new_value(self) -> None:
    class Owner:
      x = FastBox[int](1)

    with self.assertRaises(TypeError) as context:
      Owner.x(2)
    self.assertIn("The box at 'Owner.x' took its value",
                  str(context.exception))

  def test_placement(self) -> None:
    class Owner:
      x = FastBox[int](1)
      a = b = FastBox[str]('s')
      me = FastBox[THIS]()

    box = Owner.__dict__['x']
    self.assertEqual(box.__field_name__, 'x')
    self.assertIs(box.__field_owner__, Owner)
    self.assertEqual(box.__private_name__, '__fast_x__')
    self.assertIsNot(Owner.__dict__['a'], Owner.__dict__['b'])
    self.assertEqual(Owner.__dict__['b'].__private_name__, '__fast_b__')
    self.assertIs(Owner.__dict__['me'].__field_type__, Owner)
    self.assertIsInstance(Owner().me, Owner)

  def test_placement_refusals(self) -> None:
    class Owner:
      pass

    class Slotted:
      __slots__ = ()

    class First:
      x = FastBox[int](1)

    with self.assertRaises(SharedDescriptor) as context:
      First.__dict__['x'].__set_name__(Owner, 'y')
    self.assertIs(context.exception.owner, First)
    self.assertIs(context.exception.desc, First.__dict__['x'])
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIs(context.exception.newOwner, Owner)
    self.assertEqual(context.exception.newName, 'y')
    self.assertIn("The 'FastBox' at 'First.x' is placed again at 'Owner.y'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      FastBox.__new__(FastBox).__set_name__(Owner, 'x')
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'FastBox.__field_type__: type'", str(context.exception))
    with self.assertRaises(MissingInstanceDict) as context:
      FastBox[int](1).__set_name__(Slotted, 'x')
    self.assertEqual(context.exception.ownerName, 'Slotted')
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIs(context.exception.instance, Slotted)
    self.assertIn("'Slotted.x'", str(context.exception))
    with self.assertRaises(TypeError) as context:
      FastBox[int].__set_name__(Owner, 'x')
    self.assertIn("'Owner.x' is declared without parentheses",
                  str(context.exception))
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Bad:
        x = FastBox[int]
    exception = context.exception.__cause__ or context.exception
    self.assertIn("'Bad.x' is declared without parentheses",
                  str(exception))

  def test_clone(self) -> None:
    class Owner:
      x = FastBox[float](2)

    clone = Owner.__dict__['x'].clone()
    self.assertIsInstance(clone, FastBox)
    self.assertIs(clone.__field_type__, float)
    self.assertEqual(clone.__declared_value__, (2.0,))
    self.assertIsNone(clone.__field_name__)
    self.assertIsNone(clone.__field_owner__)
    self.assertIsNone(clone.__private_name__)

  def test_second_name_sorting_before_the_first(self) -> None:
    class Owner:
      b = a = FastBox[int](1)

    self.assertIsNot(Owner.__dict__['a'], Owner.__dict__['b'])
    self.assertEqual(Owner.__dict__['a'].__private_name__, '__fast_a__')
    self.assertEqual(Owner.__dict__['b'].__private_name__, '__fast_b__')
    owner = Owner()
    owner.b = 2
    self.assertEqual((owner.a, owner.b), (1, 2))

  def test_clone_copies_every_other_attribute(self) -> None:
    class Owner:
      x = FastBox[int](1)

    box = Owner.__dict__['x']
    object.__setattr__(box, 'extra', 'kept')
    clone = box.clone()
    self.assertEqual(clone.extra, 'kept')
    self.assertIsNone(clone.__field_name__)
