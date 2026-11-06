"""
TestAttriBoxDeclare tests the declaration of an 'AttriBox' from
'worktoy.desc': the subscript, the parentheses, the placement, the
storage name, and copying and pickling the box.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import copyreg
import pickle
from typing import TypeVar

from worktoy.core.sentinels import THIS, DELETED
from worktoy.desc import AttriBox, FixBox
from worktoy.desc._root_alias import _RootAlias
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import UncheckableType
from worktoy.waitaminute.desc import MissingInstanceDict
from . import DescTest, Vessel, Part

T = TypeVar('T')


class TestAttriBoxDeclare(DescTest):
  """
  An 'AttriBox' is declared with a subscript naming the field type and
  parentheses holding the arguments of its default, and the mistakes of
  a declaration are refused as the class is created. The tests pin the
  subscripts, the kept arguments, every refusal of the placement, the
  storage key with its cache, the box answering a copy with itself, and
  the pickle of a placed box, an unplaced one and an instance holding
  box-built values.
  """

  def test_subscript(self) -> None:
    box = AttriBox[int]
    self.assertIsInstance(box, AttriBox)
    self.assertIs(box.getFieldType(), int)
    self.assertIs(box.fieldType, int)
    self.assertIs(AttriBox[THIS].getFieldType(), THIS)
    self.assertIsInstance(FixBox[int], FixBox)
    self.assertIsInstance(AttriBox[T], _RootAlias)
    with self.assertRaises(TypeError) as context:
      _ = AttriBox[DELETED]
    self.assertIn("'AttriBox[DELETED]' names a sentinel",
                  str(context.exception))

    class Refusing(type):
      def __instancecheck__(cls, instance: object) -> bool:
        raise TypeError('no instance checks')

    Odd = Refusing('Odd', (), {})
    with self.assertRaises(UncheckableType) as context:
      _ = AttriBox[Odd]
    self.assertEqual(context.exception.declaration, 'AttriBox[Odd]')
    self.assertIs(context.exception.entry, Odd)
    self.assertIsNone(context.exception.position)
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("box 'AttriBox[Odd]'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      _ = AttriBox[int, str]
    self.assertEqual(context.exception.varName, 'fieldType')
    self.assertEqual(context.exception.actualObject, (int, str))
    self.assertIs(context.exception.actualType, tuple)
    self.assertEqual(context.exception.expectedTypes, (type, TypeVar))
    self.assertIn("'fieldType'", str(context.exception))
    self.assertIsInstance(context.exception.__cause__, TypeError)

  def test_field_type_missing(self) -> None:
    blank = object.__new__(AttriBox)
    with self.assertRaises(MissingVariable) as context:
      blank.getFieldType()
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertEqual(str(context.exception),
                     "Missing 'AttriBox.__field_type__: type'!")
    with self.assertRaises(MissingVariable) as context:
      blank.__get__(object(), object)
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIs(blank.__get__(None, object), blank)

  def test_parentheses_keep_arguments(self) -> None:
    box = AttriBox[int](1, 2, key=3)
    self.assertEqual(box.getPosArgs(), (1, 2))
    self.assertEqual(box.getKeyArgs(), {'key': 3})

    class Owner:
      n = AttriBox[int](1)

    with self.assertRaises(TypeError) as context:
      Owner.n(2)
    self.assertIn("The box at 'Owner.n' took the arguments",
                  str(context.exception))

  def test_placement(self) -> None:
    class Owner:
      me = AttriBox[THIS]()
      n = AttriBox[int]()

    self.assertIs(Owner.__dict__['me'].getFieldType(), Owner)
    self.assertIsInstance(Owner().me, Owner)
    self.assertIs(Owner.n.getFieldOwner(), Owner)
    self.assertEqual(Owner.n.getFieldName(), 'n')

  def test_placement_refusals(self) -> None:
    class Owner:
      pass

    class Slotted:
      __slots__ = ()

    class Lazy(AttriBox[T]):
      def __init__(self, *args, **kwargs) -> None:
        """Hands nothing on to 'AttriBox.__init__'."""

    with self.assertRaises(MissingVariable) as context:
      object.__new__(AttriBox).__set_name__(Owner, 'x')
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'AttriBox.__field_type__: type'", str(context.exception))
    with self.assertRaises(MissingInstanceDict) as context:
      AttriBox[int]().__set_name__(Slotted, 'x')
    self.assertEqual(context.exception.ownerName, 'Slotted')
    self.assertIs(context.exception.instance, Slotted)
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIn("'Slotted.x'", str(context.exception))
    with self.assertRaises(TypeError) as context:
      AttriBox[int].__set_name__(Owner, 'x')
    self.assertIn("'Owner.x' is declared without parentheses",
                  str(context.exception))
    with self.assertRaises(TypeError) as context:
      Lazy[int](1).__set_name__(Owner, 'x')
    self.assertIn("'Owner.x'", str(context.exception))
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Bad:
        x = AttriBox[int]
    exception = context.exception.__cause__ or context.exception
    self.assertIn("'Bad.x' is declared without parentheses",
                  str(exception))
    with self.assertRaises((MissingInstanceDict, RuntimeError)) as context:
      class Slots:
        __slots__ = ()
        x = AttriBox[int]()
    exception = context.exception.__cause__ or context.exception
    self.assertEqual(exception.ownerName, 'Slots')
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.instance.__name__, 'Slots')
    self.assertIn("'Slots.x'", str(exception))

  def test_storage_name(self) -> None:
    class Owner:
      x = AttriBox[int](0)

    box = Owner.__dict__['x']
    self.assertEqual(box._getStorageName(), '__x__attribox_field_object__')
    self.assertIs(box._getStorageName(), box._getStorageName())
    self.assertEqual(FixBox[int](0).__class__.__name__.lower(), 'fixbox')
    unplaced = AttriBox[int](0)
    with self.assertRaises(RecursionError) as context:
      unplaced._getStorageName(_recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(MissingVariable) as context:
      unplaced._getStorageName()
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, unplaced)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(str(context.exception),
                     "Missing 'AttriBox.__field_name__: str'!")
    object.__setattr__(box, '__storage_name__', 42)
    with self.assertRaises(TypeException) as context:
      box._getStorageName()
    self.assertEqual(context.exception.varName, '__storage_name__')
    self.assertEqual(context.exception.actualObject, 42)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__storage_name__'", str(context.exception))
    box._clearStorageName()
    self.assertEqual(box._getStorageName(), '__x__attribox_field_object__')

  def test_copy_gives_box_itself(self) -> None:
    box = Vessel.__dict__['count']
    self.assertIs(copy.copy(box), box)
    self.assertIs(copy.deepcopy(box), box)

  def test_reduce_and_pickle(self) -> None:
    placed = Vessel.__dict__['count']
    self.assertEqual(placed.__reduce__(), (getattr, (Vessel, 'count')))
    self.assertIs(pickle.loads(pickle.dumps(placed)), placed)
    unplaced = AttriBox[int](7)
    reduced = unplaced.__reduce__()
    self.assertIs(reduced[0], copyreg.__newobj__)
    self.assertEqual(reduced[1], (AttriBox,))
    rebuilt = pickle.loads(pickle.dumps(unplaced))
    self.assertIsInstance(rebuilt, AttriBox)
    self.assertIsNot(rebuilt, unplaced)
    self.assertIs(rebuilt.getFieldType(), int)
    self.assertEqual(rebuilt.getPosArgs(), (7,))

  def test_instance_pickle_keeps_tags(self) -> None:
    vessel = Vessel()
    vessel.count = 3
    part = vessel.part
    self.assertIs(part.__field_box__, Vessel.__dict__['part'])
    twin = pickle.loads(pickle.dumps(vessel))
    self.assertEqual((twin.count, twin.label), (3, 'vessel'))
    self.assertIsInstance(twin.part, Part)
    self.assertIsNot(twin.part, part)
    self.assertIs(twin.part.__field_box__, Vessel.__dict__['part'])
    self.assertIs(twin.part.__field_owner__, Vessel)
    self.assertEqual(twin.part.__field_name__, 'part')
    copied = copy.deepcopy(vessel)
    self.assertIs(copied.part.__field_box__, Vessel.__dict__['part'])
