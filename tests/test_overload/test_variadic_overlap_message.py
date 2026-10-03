"""
TestVariadicOverlapMessage subclasses 'OverloadTest' and pins that two
variadic declarations of different functions accepting one call by exact
type raise 'VariadicOverlap', a 'DuplicateSignature' whose message names
the two declarations as written and the shared signature, and says how
to settle it: by declaring the shared signature explicitly, or, for two
declarations of one inner type, which share every longer call too, not at
all. The refusal used to name only the expanded signature,
'<TypeSig: [int]>' for '@overload(ARGS[int])' beside
'@overload(int, ARGS[int])', which neither declaration wrote.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DuplicateSignature, VariadicOverlap

from . import OverloadTest


def _addAll(self, *xs: int) -> int:
  """Adds any number of integers."""
  return sum(xs)  # pragma: no cover


def _addFirst(self, first: int, *rest: int) -> int:
  """Adds a first integer and any number more."""
  return first + sum(rest)  # pragma: no cover


class TestVariadicOverlapMessage(OverloadTest):
  """
  TestVariadicOverlapMessage provides tests for the refusal of two
  overlapping variadic declarations.
  """

  def test_overlap_names_declarations(self) -> None:
    """The refusal is a 'VariadicOverlap' naming the two declarations,
    the name, the shared signature and the two functions."""
    with self.assertRaises(VariadicOverlap) as context:
      class Totals(BaseObject):
        add = overload(ARGS[int])(_addAll)
        add = overload(int, ARGS[int])(_addFirst)  # noqa: F811
    e = context.exception
    self.assertIsInstance(e, DuplicateSignature)
    self.assertEqual(e.overloadName, 'add')
    self.assertEqual(e.firstSig, TypeSig(ARGS[int]))
    self.assertEqual(e.secondSig, TypeSig(int, ARGS[int]))
    self.assertEqual(e.sig, TypeSig(int))
    self.assertIs(e.existing, _addAll)
    self.assertIs(e.duplicate, _addFirst)
    message = str(e)
    self.assertIn('<TypeSig: [ARGS[int]]>', message)
    self.assertIn('<TypeSig: [int, ARGS[int]]>', message)
    self.assertIn("'add'", message)
    self.assertIn('<TypeSig: [int]>', message)
    self.assertIn(_addAll.__name__, message)
    self.assertIn(_addFirst.__name__, message)
    self.assertEqual(message, repr(e))
    self.assertIn('every longer call', message)
    self.assertNotIn('Declare', message)

  def test_declaration_order_kept(self) -> None:
    """The declaration registered first is the first named, whichever
    is written first."""
    with self.assertRaises(VariadicOverlap) as context:
      class Totals(BaseObject):
        add = overload(int, ARGS[int])(_addFirst)
        add = overload(ARGS[int])(_addAll)  # noqa: F811
    e = context.exception
    self.assertEqual(e.firstSig, TypeSig(int, ARGS[int]))
    self.assertEqual(e.secondSig, TypeSig(ARGS[int]))
    self.assertIs(e.existing, _addFirst)
    self.assertIs(e.duplicate, _addAll)

  def test_empty_prefix(self) -> None:
    """Two variadics without a prefix share the empty signature, which an
    explicit declaration settles, as the message says."""
    with self.assertRaises(VariadicOverlap) as context:
      class Joined(BaseObject):
        @overload(ARGS[int])
        def join(self, *xs: int) -> str:
          return 'ints'  # pragma: no cover

        @overload(ARGS[str])
        def join(self, *xs: str) -> str:
          return 'strs'  # pragma: no cover
    e = context.exception
    self.assertEqual(e.sig, TypeSig())
    self.assertIn('<TypeSig: []>', str(e))
    self.assertIn('Declare <TypeSig: []> explicitly', str(e))
    self.assertNotIn('every longer call', str(e))

  def test_explicit_duplicate_stays_plain(self) -> None:
    """Two explicit declarations of one signature raise the plain
    'DuplicateSignature', not an overlap."""
    with self.assertRaises(DuplicateSignature) as context:
      class Doubled(BaseObject):
        @overload(int)
        def f(self, n: int) -> str:
          return 'first'  # pragma: no cover

        @overload(int)
        def f(self, n: int) -> str:
          return 'second'  # pragma: no cover
    self.assertNotIsInstance(context.exception, VariadicOverlap)

  def test_declaration_kept_whole(self) -> None:
    """A variadic declaration is held as written, with no concrete
    signature beside it."""
    ov = overload(str, ARGS[int])(_addAll)
    self.assertEqual([*ov], [])
    self.assertEqual(ov.getVariadics(), [(TypeSig(str, ARGS[int]), _addAll)])
