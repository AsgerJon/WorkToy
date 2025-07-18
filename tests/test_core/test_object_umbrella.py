"""
TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
fundamental object in the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from . import CoreTest
from worktoy.core import Object, ContextInstance
from worktoy.core.sentinels import DESC, THIS, OWNER
from worktoy.mcls import BaseObject
from worktoy.utilities import Directory
from worktoy.waitaminute.desc import WithoutException, ReadOnlyError
from worktoy.waitaminute.desc import ProtectedError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foo(BaseObject):
  def __instance_get__(self, *args, **kwargs) -> Any:
    pvtName = self.getPrivateName()
    return getattr(self.instance, pvtName, 69)


class Bar(BaseObject):
  foo1 = Foo(THIS, OWNER, DESC)
  foo2 = Foo(tom=THIS, dick=OWNER, harry=DESC)


class TestObjectUmbrella(CoreTest):
  """
  TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
  fundamental object in the 'worktoy' library.
  """

  def testSentinelResolution(self) -> None:
    """
    Test that BaseObject resolves sentinels correctly.
    """
    posArgs = Bar.foo1.getPosArgs(DESC=69, THIS=420, OWNER=1337)
    self.assertIsInstance(posArgs, tuple)
    for arg in posArgs:
      self.assertIsInstance(arg, int)

    keyArgs = Bar.foo2.getKeyArgs(DESC=69, THIS=420, OWNER=1337)
    for key, value in keyArgs.items():
      self.assertIsInstance(key, str)
      self.assertIsInstance(value, int)

  def testWithoutException(self) -> None:
    """Tests WithoutException handling."""
    with self.assertRaises(WithoutException) as context:
      _ = Bar.foo1.instance
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Bar.foo1)

  def testBadContext(self) -> None:
    """Tests context manager"""

    with self.assertRaises(WithoutException) as context:
      Bar.foo1.__enter__()
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def testGoodContext(self) -> None:
    """Tests context manager"""
    bar = Bar()
    self.assertEqual(bar.foo1, 69)

  def testClassContextInstance(self) -> None:
    """Tests class context manager with instance"""
    self.assertIsInstance(Object.instance, ContextInstance)

  def testObjectDirectory(self) -> None:
    """Tests that Object has a directory."""

    self.assertIsInstance(Object.directory, Directory)
    self.assertTrue(os.path.exists(Object().directory))
    with self.assertRaises(ReadOnlyError) as context:
      Object().directory = 'breh'
    with self.assertRaises(ProtectedError) as context:
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
      lol, kwargs = foo.parseKwargs('b', str, set, **kwargs)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'b')
    self.assertEqual(e.actualObject, 1)
    self.assertEqual(e.actualType, int)
    self.assertEqual(e.expectedTypes, (str, set))

    lol, kwargs = foo.parseKwargs('breh', complex, **dict())
    lol, kwargs = foo.parseKwargs('breh', complex, float, **dict())
    lol, kwargs = foo.parseKwargs('breh', complex, int, **dict())
    lol, kwargs = foo.parseKwargs('breh', float, int, **dict())
    lol, kwargs = foo.parseKwargs('breh', float, **dict())
