"""
TestAttriBoxAccess tests the reads, writes and deletions of an
'AttriBox' from 'worktoy.desc': the value built at the first read, the
tags, the cast on assignment and the deletion.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from types import FunctionType

from worktoy.core.sentinels import THIS, OWNER, DESC
from worktoy.desc import AttriBox
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import MissingInstanceDict
from worktoy.waitaminute.dispatch import TypeCastException
from . import DescTest, Part


def _helper() -> str:
  """A function used as a default."""
  return 'helper'


class TestAttriBoxAccess(DescTest):
  """
  The first read through an instance builds the value from the declared
  arguments, with placeholders replaced and a lone argument of the field
  type copied; an 'Object' the box builds is tagged; an assigned value
  is kept or cast without loss; a deletion leaves a mark the next read
  refuses. The tests pin each of these, the refusals of an instance
  without a dictionary and of a constructor giving the wrong type, and
  the two peeks the recursion flags make.
  """

  def test_builds_from_arguments(self) -> None:
    class Owner:
      n = AttriBox[int]()
      c = AttriBox[complex](1, 2)
      f = AttriBox[float](3)
      p = AttriBox[Part](1, key=2)

    owner = Owner()
    self.assertEqual(owner.n, 0)
    self.assertEqual(owner.c, 1 + 2j)
    self.assertEqual(owner.f, 3.0)
    self.assertIs(type(owner.f), float)
    self.assertEqual(_helper(), 'helper')
    part = owner.p
    self.assertIsInstance(part, Part)
    self.assertIs(owner.p, part)
    self.assertEqual(part.getPosArgs(), (1,))
    self.assertEqual(part.getKeyArgs(), {'key': 2})
    self.assertIs(part.__field_box__, Owner.__dict__['p'])
    self.assertIs(part.__field_owner__, Owner)
    self.assertEqual(part.__field_name__, 'p')
    self.assertIsNot(Owner().p, part)

  def test_placeholders_replaced(self) -> None:
    class Owner:
      p = AttriBox[Part](THIS, OWNER, DESC, inner=[THIS])

    owner = Owner()
    self.assertEqual(owner.p.getPosArgs(),
                     (owner, Owner, Owner.__dict__['p']))
    self.assertEqual(owner.p.getKeyArgs(), {'inner': [THIS]})

  def test_lone_argument_copied(self) -> None:
    class Owner:
      items = AttriBox[list](['a'])
      part = AttriBox[Part](Part(9))
      func = AttriBox[FunctionType](_helper)
      kind = AttriBox[type](int)

    first, second = Owner(), Owner()
    self.assertEqual(first.items, ['a'])
    self.assertIsNot(first.items, second.items)
    self.assertIsNot(first.items, Owner.__dict__['items'].getPosArgs()[0])
    self.assertIsNot(first.part, second.part)
    self.assertEqual(first.part.getPosArgs(), (9,))
    self.assertIs(first.part.__field_box__, Owner.__dict__['part'])
    self.assertIs(first.func, _helper)
    self.assertIs(first.kind, int)

  def test_placeholder_prevents_copy(self) -> None:
    class Owner:
      p = AttriBox[Part](THIS)

    owner = Owner()
    self.assertEqual(owner.p.getPosArgs(), (owner,))

  def test_uncopyable_default_refused(self) -> None:
    class Owner:
      lock = AttriBox[type(threading.Lock())](threading.Lock())

    with self.assertRaises(TypeError) as context:
      _ = Owner().lock
    self.assertIn("The default of 'Owner.lock'", str(context.exception))
    self.assertIn('cannot be copied', str(context.exception))
    self.assertIsNotNone(context.exception.__cause__)

  def test_constructor_result_checked(self) -> None:
    class Weird:
      def __new__(cls) -> int:
        return 5

    class Owner:
      w = AttriBox[Weird]()

    with self.assertRaises(TypeException) as context:
      _ = Owner().w
    self.assertEqual(context.exception.varName, 'w')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Weird,))
    self.assertIn("'w'", str(context.exception))
    self.assertIn("'Weird'", str(context.exception))

  def test_assignment_kept_or_cast(self) -> None:
    class Owner:
      n = AttriBox[int](0)
      s = AttriBox[str]('')

    owner = Owner()
    owner.n = 2.0
    self.assertEqual(owner.n, 2)
    self.assertIs(type(owner.n), int)
    owner.n = True
    self.assertIs(owner.n, True)
    owner.s = b'text'
    self.assertEqual(owner.s, 'text')
    with self.assertRaises(TypeException) as context:
      owner.n = 'x'
    self.assertEqual(context.exception.varName, 'n')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'n'", str(context.exception))
    self.assertIn("'int'", str(context.exception))
    self.assertIsInstance(context.exception.__cause__, TypeCastException)
    self.assertIs(owner.n, True)

  def test_deletion_leaves_a_mark(self) -> None:
    class Owner:
      n = AttriBox[int](0)

    owner = Owner()
    owner.n = 5
    del owner.n
    with self.assertRaises(MissingVariable) as context:
      _ = owner.n
    self.assertEqual(context.exception.varName, 'n')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Owner.n: object'", str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      del owner.n
    self.assertEqual(context.exception.varName, 'n')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    owner.n = 6
    self.assertEqual(owner.n, 6)
    fresh = Owner()
    del fresh.n
    with self.assertRaises(MissingVariable) as context:
      _ = fresh.n
    self.assertEqual(context.exception.varName, 'n')
    self.assertIs(context.exception.instance, fresh)
    self.assertIn("'Owner.n: object'", str(context.exception))

  def test_instance_without_dict(self) -> None:
    class Slotted:
      __slots__ = ()

    class Owner:
      n = AttriBox[int](0)

    box = Owner.__dict__['n']
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict) as context:
      box.__set__(slotted, 1)
    self.assertIs(context.exception.instance, slotted)
    self.assertEqual(context.exception.fieldName, 'n')
    self.assertEqual(context.exception.ownerName, 'Slotted')
    self.assertIn("'Slotted.n'", str(context.exception))
    _ = Owner().n
    clone = box.clone()
    with self.assertRaises(MissingVariable) as context:
      clone._store(slotted, 1)
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, clone)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(str(context.exception),
                     "Missing 'AttriBox.__field_name__: str'!")

  def test_peeks(self) -> None:
    class Owner:
      n = AttriBox[int](0)

    box = Owner.__dict__['n']
    owner = Owner()
    with self.assertRaises(AttributeError):
      box.__instance_get__(owner, Owner, _deleting=True)
    self.assertNotIn(box._getStorageName(), owner.__dict__)
    with self.assertRaises(RecursionError) as context:
      box.__instance_get__(owner, Owner, _recursion=True)
    self.assertEqual(context.exception.args, ())
    with self.assertRaises(RecursionError) as context:
      box.__instance_set__(owner, 'x', _recursion=True)
    self.assertEqual(context.exception.args, ())
    self.assertEqual(box.__instance_get__(owner, Owner), 0)
    self.assertEqual(box.__instance_get__(owner, Owner, _deleting=True), 0)

  def test_random_values(self) -> None:
    class Owner:
      n = AttriBox[int](0)
      s = AttriBox[str]('')

    for number, word in zip(self.randomInteger.row, self.randomWord.row):
      owner = Owner()
      owner.n = number
      owner.s = word
      with self.subTest(number=number, word=word):
        self.assertEqual((owner.n, owner.s), (number, word))

  def test_default_equal_to_its_copy_still_tagged(self) -> None:
    from worktoy.desc import SymbolicName

    class Owner:
      name = AttriBox[SymbolicName](SymbolicName('font', 'size'))

    default = Owner.__dict__['name'].getPosArgs()[0]
    owner = Owner()
    self.assertEqual(owner.name, default)
    self.assertIsNot(owner.name, default)
    self.assertIs(owner.name.__field_box__, Owner.__dict__['name'])
