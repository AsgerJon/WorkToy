"""
TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
fundamental object in the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import os

from worktoy.waitaminute import TypeException
from worktoy.core import Object, ContextInstance, ContextOwner
from worktoy.core.sentinels import DESC, THIS, OWNER
from worktoy.mcls import BaseObject
from worktoy.utilities import Directory
from worktoy.waitaminute.desc import WithoutException, ReadOnlyError
from worktoy.waitaminute.desc import ProtectedError
from . import CoreTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foo(BaseObject):
  def __instance_get__(self, *args, **kwargs) -> Any:
    pvtName = self.getPrivateName()
    return getattr(self.instance, pvtName, 69)


class Owned(BaseObject):
  def __instance_get__(self, *args, **kwargs) -> Any:
    return self.owner


class Bar(BaseObject):
  foo1 = Foo(THIS, OWNER, DESC)
  foo2 = Foo(tom=THIS, dick=OWNER, harry=DESC)
  owned = Owned()


class TestObjectUmbrella(CoreTest):
  """
  TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
  fundamental object in the 'worktoy' library.
  """

  def testWithoutException(self) -> None:
    """Tests WithoutException handling."""
    with self.assertRaises(WithoutException) as context:
      _ = Bar.foo1.instance
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Bar.foo1)
    with self.assertRaises(WithoutException) as context:
      _ = Bar.foo1.owner
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Bar.foo1)
    with self.assertRaises(WithoutException) as context:
      _ = Bar.owned.owner
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Bar.owned)

  def testExitContextWithoutCreate(self) -> None:
    """Popping the context stack when it is empty must raise
    'WithoutException', since that indicates an unpaired
    'createContext' / 'exitContext' call."""
    obj = Object()
    with self.assertRaises(WithoutException) as context:
      obj.exitContext()
    e = context.exception
    self.assertIs(e.desc, obj)

  def testGoodContext(self) -> None:
    """Tests context manager"""
    bar = Bar()
    self.assertEqual(bar.foo1, 69)
    self.assertIs(bar.owned, Bar)
    self.assertIsInstance(Bar.owned, Owned)

  def testGoodClassContext(self) -> None:
    """Tests class context manager"""
    self.assertIsInstance(Bar.foo1, Foo)
    self.assertIsInstance(Bar.foo2, Foo)
    self.assertIsInstance(Bar.owned, Owned)
    self.assertIsInstance(Bar.owner, ContextOwner)

  def testClassContextInstance(self) -> None:
    """Tests class context manager with instance"""
    self.assertIsInstance(Object.instance, ContextInstance)

  def testObjectDirectory(self) -> None:
    """Tests that Object has a directory."""

    self.assertIsInstance(Object.directory, Directory)
    self.assertTrue(os.path.exists(Object().directory))
    with self.assertRaises(ReadOnlyError):
      Object().directory = 'breh'
    with self.assertRaises(ProtectedError):
      del Object().directory

  def testKeyArgs(self, ) -> None:
    """Keyword argument related coverage gymnastics"""
    foo = Object(a=0, b=1, c=2)
    kwargs = foo.getKeyArgs()
    for i, c in enumerate('abc'):
      self.assertEqual(kwargs[c], i)

  def testParseKwargs(self, ) -> None:
    """Tests the parsing of keyword arguments."""
    foo = Object(a=0, b=1, c=2)
    kwargs = foo.getKeyArgs()
    breh, kwargs = foo.parseKwargs(69, 420, 'a', int, **kwargs)
    self.assertEqual(breh, 0)
    lol, kwargs = foo.parseKwargs(**kwargs)
    with self.assertRaises(TypeException) as context:
      _ = foo.parseKwargs('b', str, set, **kwargs)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'b')
    self.assertEqual(e.actualObject, 1)
    self.assertEqual(e.actualType, int)
    self.assertEqual(e.expectedTypes, (str, set))

    lol, kwargs = foo.parseKwargs('breh', complex, **dict())
    self.assertIsNone(lol)
    self.assertIsInstance(kwargs, dict)
    lol, kwargs = foo.parseKwargs('breh', complex, float, **dict())
    self.assertIsNone(lol)
    self.assertIsInstance(kwargs, dict)
    lol, kwargs = foo.parseKwargs('breh', complex, int, **dict())
    self.assertIsNone(lol)
    self.assertIsInstance(kwargs, dict)
    lol, kwargs = foo.parseKwargs('breh', float, int, **dict())
    self.assertIsNone(lol)
    self.assertIsInstance(kwargs, dict)
    lol, kwargs = foo.parseKwargs('breh', float, **dict())
    self.assertIsNone(lol)
    self.assertIsInstance(kwargs, dict)

  def test_fallback_set(self) -> None:
    """Tests the fallback __setattr__ of Object."""

    class Ham(Object):
      sus = Object()

    ham = Ham()

    with self.assertRaises(ReadOnlyError) as context:
      ham.sus = 69
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, ham)
    self.assertIs(e.desc, Ham.sus)
    self.assertEqual(e.newVal, 69)
