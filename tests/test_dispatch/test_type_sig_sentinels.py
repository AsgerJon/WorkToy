"""
TestTypeSigSentinels subclasses 'DispatcherTest' and pins what
'TypeSig.validateTypes' makes of the sentinels in a declared signature.
'THIS' is handled first and passes, alone or as the inner type of a
trailing 'ARGS', since placement swaps it for the class. Every other
'Sentinel' subclass, 'OWNER', 'DESC', 'DELETED', 'METACALL' and
'Sentinel' itself, is refused with 'TypeError' naming its position and
the sentinel, alone or inside a trailing 'ARGS': a sentinel class cannot
be instantiated, so a signature holding one could never match a call.
'OWNER' alone used to be refused by name, and 'DESC' and the rest were
registered in silence as overloads nothing could reach.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import Sentinel, THIS, OWNER, DESC
from worktoy.core.sentinels import DELETED, METACALL, ARGS
from worktoy.dispatch import TypeSig, overload
from worktoy.mcls import BaseObject

from . import DispatcherTest


class TestTypeSigSentinels(DispatcherTest):
  """
  TestTypeSigSentinels provides tests for sentinels in a declared
  signature.
  """

  others = (OWNER, DESC, DELETED, METACALL, Sentinel)

  def test_this_passes(self) -> None:
    """'THIS' passes alone, beside a class, and inside 'ARGS'."""
    TypeSig.validateTypes(THIS)
    TypeSig.validateTypes(int, THIS)
    TypeSig.validateTypes(THIS, ARGS[THIS])

  def test_other_sentinels_refused(self) -> None:
    """Every other sentinel is refused, naming its position and itself."""
    for sentinel in self.others:
      with self.subTest(sentinel=sentinel.__name__):
        with self.assertRaises(TypeError) as context:
          TypeSig.validateTypes(int, sentinel)
        text = str(context.exception)
        self.assertIn('position 1', text)
        self.assertIn(sentinel.__name__, text)

  def test_sentinel_inside_args_refused(self) -> None:
    """A sentinel as the inner type of a trailing 'ARGS' is refused."""
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(int, ARGS[DESC])
    self.assertIn('DESC', str(context.exception))

  def test_overload_refuses_at_declaration(self) -> None:
    """'@overload' refuses the sentinel at the decorator, so no dead
    signature is registered."""
    with self.assertRaises(TypeError):
      class Host(BaseObject):
        @overload(DESC)
        def g(self, x: object) -> str:
          return 'never'  # pragma: no cover
