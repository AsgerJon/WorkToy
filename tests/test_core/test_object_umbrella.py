"""
TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
fundamental object in the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import DESC, THIS, OWNER
from worktoy.mcls import BaseObject

from typing import TYPE_CHECKING

from worktoy.waitaminute.desc import WithoutException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Foo(BaseObject):
  def __instance_get__(self, *args, **kwargs) -> Any:
    pvtName = self.getPrivateName()
    return getattr(self.instance, pvtName, 69)


class Bar(BaseObject):
  foo1 = Foo(THIS, OWNER, DESC)
  foo2 = Foo(tom=THIS, dick=OWNER, harry=DESC)


class TestObjectUmbrella(TestCase):
  """
  TestObjectUmbrella covers obscure edge cases and esoteric fallbacks of the
  fundamental object in the 'worktoy' library.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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
    self.assertIs(e.desc, Bar.foo1)

  def testBadContext(self) -> None:
    """Tests context manager"""

    with self.assertRaises(WithoutException) as context:
      Bar.foo1.__enter__()

  def testGoodContext(self) -> None:
    """Tests context manager"""
    bar = Bar()
    self.assertEqual(bar.foo1, 69)
 