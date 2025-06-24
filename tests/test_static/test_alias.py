"""
TestAlias tests that the 'Alias' class from the 'worktoy.static' module
works as expected.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.static import AbstractObject, Alias
from worktoy.waitaminute import AliasException
from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestAlias(TestCase):
  """
  TestAlias tests that the 'Alias' class from the 'worktoy.static' module
  works as expected.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_missing_parent(self) -> None:
    """
    Tests that an 'Alias' instance without a parent raises a
    'MissingVariable' exception. Please note that in Python 3.7,
    the RuntimeError is raised before the custom descriptor implementation
    is able to raise AliasException.
    """

    with self.assertRaises(RuntimeError) as context:
      class Foo:
        breh = Alias('lmao')
    e = context.exception
    info = 'python: %s: %s' % (sys.version, type(e).__name__)
    f = None
    try:
      f = open('test_alias.log', 'w')
    except:
      raise
    else:
      f.write(info + '\n')
    finally:
      if hasattr(f, 'close'):
        f.close()
    if isinstance(e, AliasException):
      self.assertEqual(e.owner.__name__, 'Foo')  # Cause can't access lol
      self.assertEqual(e.name, 'breh')
      self.assertEqual(str(e), repr(e))
    else:
      self.assertIsInstance(e, RuntimeError)

  def test_good_alias(self) -> None:
    """
    Tests that an 'Alias' instance with a valid parent and name works as
    expected.
    """

    class Foo:
      bar = AbstractObject()

    class Alias2(Alias):
      """
      Debugging subclass
      """

    class Bar(Foo):
      baz = Alias2('bar')

    bar = Bar()
    self.assertEqual(bar.baz, bar.bar)
