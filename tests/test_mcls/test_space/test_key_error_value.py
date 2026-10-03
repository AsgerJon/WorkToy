"""
TestKeyErrorValue subclasses 'MCLSTest' and pins that a class body may
bind a 'KeyError' instance and read it back. The namespace used the
'KeyError' it caught for a missing name as its marker, and raised any
'KeyError' a read turned up, so a bound one read as a missing name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject

from .. import MCLSTest


class TestKeyErrorValue(MCLSTest):
  """
  TestKeyErrorValue provides tests for a 'KeyError' bound in a class
  body.
  """

  def test_read_back(self) -> None:
    """A bound 'KeyError' is read back as itself."""

    class Foo(BaseObject):
      err = KeyError('stored')
      seen = err

    self.assertIs(Foo.seen, Foo.err)
    self.assertIsInstance(Foo.seen, KeyError)

  def test_missing_name_still_global(self) -> None:
    """A name the class body never bound still reads from the module
    scope."""

    class Foo(BaseObject):
      seen = MCLSTest

    self.assertIs(Foo.seen, MCLSTest)
