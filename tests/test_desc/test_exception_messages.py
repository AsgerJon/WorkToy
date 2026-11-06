"""
TestExceptionMessages renders the messages of the exceptions
'worktoy.desc' raises and pins their slots.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TypeVar
from unittest import skipIf

from worktoy.core import Object
from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import AccessError, MissingInstanceDict
from worktoy.waitaminute.desc import NotADescriptor, PhantomBoxError
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError
from worktoy.waitaminute.desc import WriteOnceError
from . import DescTest


class TestExceptionMessages(DescTest):
  """
  An exception the package raises carries a message naming what went
  wrong, and slots holding what it was given, and both are what a
  reader looks for. 'waitaminute' has no tests of its own: each raising
  package renders the messages of the exceptions it raises. The tests
  pin the names each message carries, the branches the rendering
  takes, every slot of each exception, and the field-name lookup the
  descriptor exceptions share.
  """

  def test_access_error(self) -> None:
    class Owner:
      d = Object()

    placed = AccessError(Owner.__dict__['d'])
    self.assertIs(placed.desc, Owner.__dict__['d'])
    self.assertIn("'Object'", str(placed))
    self.assertIn("'Owner.d'", str(placed))
    desc = Object()
    loose = AccessError(desc)
    self.assertIs(loose.desc, desc)
    self.assertIn("'object.object'", str(loose))
    self.assertEqual(repr(loose), str(loose))

  def test_missing_instance_dict(self) -> None:
    byInstance = MissingInstanceDict(7, 'x')
    self.assertEqual(byInstance.instance, 7)
    self.assertEqual(byInstance.ownerName, 'int')
    self.assertEqual(byInstance.fieldName, 'x')
    self.assertIn("'int.x'", str(byInstance))
    self.assertIn("instances of 'int'", str(byInstance))
    byClass = MissingInstanceDict(int, 'y')
    self.assertIs(byClass.instance, int)
    self.assertEqual(byClass.ownerName, 'int')
    self.assertEqual(byClass.fieldName, 'y')
    self.assertEqual(repr(byClass), str(byClass))

  def test_not_a_descriptor(self) -> None:
    class Owner:
      d = Object()

    found = 'y' * 60
    placed = NotADescriptor(Owner.__dict__['d'], 'real', found)
    self.assertIs(placed.alias, Owner.__dict__['d'])
    self.assertEqual(placed.realName, 'real')
    self.assertIs(placed.found, found)
    text = str(placed)
    self.assertIn("'Owner.d'", text)
    self.assertIn("'real'", text)
    self.assertIn('...', text)
    self.assertNotIn('y' * 50, text)
    self.assertIn("'str'", text)
    alias = object()
    loose = NotADescriptor(alias, 'real', 5)
    self.assertIs(loose.alias, alias)
    self.assertEqual(loose.found, 5)
    self.assertIn("'object.alias'", str(loose))
    self.assertIn("'int'", str(loose))
    self.assertEqual(repr(loose), str(loose))

  @skipIf(sys.version_info < (3, 9), 'list[int] came in 3.9')
  def test_phantom_box_error(self) -> None:
    T = TypeVar('T')

    class FakeAlias:
      __origin__ = AttriBox
      __args__ = (int, list[int], T)

    class Owner:
      """The class the alias was declared in."""

    alias = FakeAlias()
    full = PhantomBoxError(alias, Owner, 'field')
    self.assertIs(full.alias, alias)
    self.assertIs(full.owner, Owner)
    self.assertEqual(full.fieldName, 'field')
    text = str(full)
    self.assertIn("'field = AttriBox[int, list[int], ~T]'", text)
    self.assertIn("in class 'Owner'", text)
    self.assertIn("an 'AttriBox'", text)
    self.assertIn("'field = AttriBox[int](0)'", text)
    plain = object()
    bare = PhantomBoxError(plain)
    self.assertIs(bare.alias, plain)
    self.assertIsNone(bare.owner)
    self.assertIsNone(bare.fieldName)
    text = str(bare)
    self.assertIn("'Box[]'", text)
    self.assertIn("a 'Box'", text)
    self.assertNotIn('in class', text)
    self.assertIn("'Box[int](0)'", text)
    self.assertEqual(repr(bare), text)

  def test_field_name_lookup(self) -> None:
    marker = object()

    class Owner:
      d = Object()
      m = marker

    owner = Owner()
    named = ProtectedError(owner, Owner.__dict__['d'], 'old')
    self.assertIs(named.instance, owner)
    self.assertIs(named.desc, Owner.__dict__['d'])
    self.assertEqual(named.oldVal, 'old')
    self.assertIn("'Owner.d'", str(named))
    self.assertIn("'old'", str(named))
    found = ReadOnlyError(owner, marker, 'new')
    self.assertIs(found.instance, owner)
    self.assertIs(found.desc, marker)
    self.assertEqual(found.newVal, 'new')
    self.assertIn("'Owner.m'", str(found))
    self.assertIn("'new'", str(found))
    stranger = object()
    nowhere = ReadOnlyError(owner, stranger, 'new')
    self.assertIs(nowhere.desc, stranger)
    self.assertIn("'Owner.object'", str(nowhere))
    self.assertEqual(repr(nowhere), str(nowhere))

  def test_write_once_error(self) -> None:
    class Owner:
      d = Object()

    placed = WriteOnceError(Owner.__dict__['d'], 1, 2)
    self.assertIs(placed.desc, Owner.__dict__['d'])
    self.assertEqual(placed.oldValue, 1)
    self.assertEqual(placed.newValue, 2)
    self.assertIn("'Owner.d'", str(placed))
    self.assertIn("'1'", str(placed))
    self.assertIn("'2'", str(placed))
    stranger = object()
    loose = WriteOnceError(stranger, 1, 2)
    self.assertIs(loose.desc, stranger)
    self.assertEqual(str(loose).count('Unknown'), 2)
    self.assertEqual(repr(loose), str(loose))

  def test_random_fields(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      instance = object()
      exception = MissingInstanceDict(instance, word)
      with self.subTest(word=word):
        self.assertIs(exception.instance, instance)
        self.assertEqual(exception.ownerName, 'object')
        self.assertEqual(exception.fieldName, word)
        self.assertIn("'object.%s'" % word, str(exception))
