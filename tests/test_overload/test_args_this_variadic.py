"""
TestArgsThisVariadic subclasses 'OverloadTest' from the 'tests.test_overload'
package and pins that '@overload(ARGS[THIS])' matches calls of any length.
'TypeSig.swapTHIS' used to replace 'THIS' in a concrete signature once the
class existed, but not the 'THIS' inside the 'ARGS' of a variadic one, so
a long call of instances of the class matched nothing while the short
calls, then matched through concrete signatures expanded from the
declaration, did. 'swapTHIS' rebuilds a trailing 'ARGS[THIS]' as 'ARGS' of
the class, and the one variadic signature decides every length.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import TypeSig, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


class Node(BaseObject):
  """Node links to any number of other nodes. It takes no constructor
  arguments, so the cast pass cannot build a node from another value."""

  def __init__(self, ) -> None:
    pass

  @overload(ARGS[THIS])
  def link(self, *others) -> int:
    return len(others)

  @overload(int, ARGS[THIS])
  def tagged(self, tag: int, *others) -> tuple:
    return tag, len(others)


class SubNode(Node):
  """SubNode is a node by inheritance."""


class TestArgsThisVariadic(OverloadTest):
  """
  TestArgsThisVariadic provides tests for variadic overloads over the
  class being defined.
  """

  def test_short_calls(self) -> None:
    """Calls of zero to five nodes match."""
    for n in range(6):
      with self.subTest(n=n):
        self.assertEqual(Node().link(*[Node() for _ in range(n)]), n)

  def test_long_calls(self) -> None:
    """Calls of more than five nodes match too, through the same
    signature."""
    for n in (6, 7, 12):
      with self.subTest(n=n):
        self.assertEqual(Node().link(*[Node() for _ in range(n)]), n)

  def test_long_call_with_prefix(self) -> None:
    """A long call after a fixed prefix matches."""
    nodes = [Node() for _ in range(8)]
    self.assertEqual(Node().tagged(3, *nodes), (3, 8))

  def test_subclass_instances(self) -> None:
    """Instances of a subclass count as nodes in a long call."""
    nodes = [SubNode() for _ in range(7)]
    self.assertEqual(SubNode().link(*nodes), 7)

  def test_foreign_argument_refused(self) -> None:
    """A long call holding something other than a node matches
    nothing."""
    with self.assertRaises(DispatchException):
      Node().link(*[Node() for _ in range(6)], 'not a node')

  def test_variadic_signature_names_class(self) -> None:
    """The variadic signature names the class rather than 'THIS'."""
    variadics = Node.__dict__['link']._getVariadicFuncs()
    self.assertEqual(len(variadics), 1)
    self.assertEqual(variadics[0][0], TypeSig(ARGS[Node]))

  def test_swap_this(self) -> None:
    """'swapTHIS' rebuilds a trailing 'ARGS[THIS]' as 'ARGS' of the class
    and leaves an 'ARGS' of another type as it was."""
    sig = TypeSig(THIS, ARGS[THIS])
    sig.swapTHIS(Node)
    self.assertEqual(sig, TypeSig(Node, ARGS[Node]))
    other = TypeSig(int, ARGS[str])
    other.swapTHIS(Node)
    self.assertEqual(other, TypeSig(int, ARGS[str]))
