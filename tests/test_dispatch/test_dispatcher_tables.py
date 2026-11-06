"""
TestDispatcherTables tests the tables 'Dispatcher' from 'worktoy.dispatch'
compiles its dispatch function from.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import Dispatcher, TypeSig, PermuterMethod
from worktoy.utilities.combinatorics import Arrangement
from . import DispatchTest


def _a(self: object, *args) -> str:
  """Function a."""
  return 'a'


def _b(self: object, *args) -> str:
  return 'b'


def _c(self: object, *args) -> str:
  return 'c'


class TestDispatcherTables(DispatchTest):
  """
  The dispatch function is compiled once from tables the registrations
  give: the exact entries with a nearer variadic signature covering a
  concrete one, the variadic tables by prefix, the bags of the flexible
  declarations, the orders of the cast passes, the tiers of the
  'isinstance' pass, and the function that documents the name. The
  tests pin each table on dispatchers fed by hand.
  """

  def test_functions_of_the_tests(self) -> None:
    self.assertEqual((_a(None), _b(None), _c(None)), ('a', 'b', 'c'))

  def test_covers_exactly(self) -> None:
    sig = TypeSig(int, ARGS[str])
    self.assertTrue(Dispatcher._coversExactly(sig, (int, str, str)))
    self.assertTrue(Dispatcher._coversExactly(sig, (int,)))
    self.assertFalse(Dispatcher._coversExactly(sig, (str,)))
    self.assertFalse(Dispatcher._coversExactly(sig, ()))
    self.assertFalse(Dispatcher._coversExactly(sig, (int, int)))

  def test_exact_entries_prefer_nearer_variadic(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int, int), _a, 2)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 1)
    dispatcher.addVariadicSigFunc(TypeSig(int, ARGS[int]), _c, 1)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (1, _c)})
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a, 0)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (0, _a)})
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 1)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (0, _a)})

  def test_exact_entries_keep_own(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int, int), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[str]), _c, 1)
    dispatcher.addSigFunc(TypeSig(str), _b, 2)
    self.assertEqual(dispatcher._getExactEntries(),
                     {(int, int): (0, _a), (str,): (1, _c)})

  def test_exact_variadics(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addVariadicSigFunc(TypeSig(int, ARGS[str]), _a, 1)
    dispatcher.addVariadicSigFunc(TypeSig(int, ARGS[str]), _b, 1)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _c, 0)
    dispatcher.addVariadicSigFunc(TypeSig(int, ARGS[str]), _c, 2)
    tailed, empty, lengths = dispatcher._getExactVariadics()
    self.assertEqual(lengths, (0, 1))
    self.assertEqual(tailed[(1, (int,), str)], ((1, -1), _b))
    self.assertEqual(empty[(1, (int,))], ((1, -1), _b))
    self.assertEqual(tailed[(0, (), int)], ((0, -2), _c))
    self.assertEqual(empty[(0, ())], ((0, -2), _c))

  def test_exact_flexes(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addFlexSigFunc(TypeSig(int, str, float, bytes), _a, 1)
    bag = TypeSig(bytes, float, str, int).getBag()
    self.assertEqual(dispatcher._getExactFlexes(),
                     {bag: (1, (int, str, float, bytes), _a)})

  def test_cast_order_farthest_first(self) -> None:
    pairs = [(TypeSig(int), _a), (TypeSig(str), _b), (TypeSig(float), _c)]
    ordered = Dispatcher._getCastOrder(pairs, [0, 2, 0])
    self.assertEqual(ordered, [pairs[1], pairs[0], pairs[2]])

  def test_variadic_order(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[str]), _b, 1)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[float]), _c, 0)
    nearest = [f for _, f in dispatcher._getVariadicOrder(True)]
    farthest = [f for _, f in dispatcher._getVariadicOrder(False)]
    self.assertEqual(nearest, [_c, _a, _b])
    self.assertEqual(farthest, [_b, _c, _a])

  def test_match_tiers(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int), _a, 1)
    dispatcher.addSigFunc(TypeSig(str), _b, 0)
    dispatcher.addFlexSigFunc(TypeSig(int, str, float, bytes), _c, 1)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[str]), _b, 0)
    tiers = dispatcher._getMatchTiers()
    self.assertEqual([tier[0] for tier in tiers], [0, 1])
    self.assertEqual(tiers[0][1], [(TypeSig(str), _b)])
    self.assertEqual(tiers[0][2], [])
    self.assertEqual([f for _, f in tiers[0][3]], [_b, _a])
    self.assertEqual(tiers[1][1], [(TypeSig(int), _a)])
    self.assertEqual(tiers[1][2], [(TypeSig(int, str, float, bytes), _c)])
    self.assertEqual(tiers[1][3], [])
    self.assertEqual(Dispatcher()._getMatchTiers(), [])

  def test_documented_function(self) -> None:
    dispatcher = Dispatcher()
    self.assertIsNone(dispatcher._getDocumentedFunction())
    dispatcher.setFinalizerFunction(_c)
    self.assertIs(dispatcher._getDocumentedFunction(), _c)
    dispatcher.setFallbackFunction(_b)
    self.assertIs(dispatcher._getDocumentedFunction(), _b)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a)
    self.assertIs(dispatcher._getDocumentedFunction(), _a)
    dispatcher.addFlexSigFunc(TypeSig(int, str, float, bytes), _b)
    self.assertIs(dispatcher._getDocumentedFunction(), _b)
    permuter = PermuterMethod(_c, Arrangement(('x',), (0,)))
    dispatcher.addSigFunc(TypeSig(int), permuter)
    self.assertIs(dispatcher._getDocumentedFunction(), _c)

  def test_declared_sigs(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a)
    dispatcher.addFlexSigFunc(TypeSig(int, str, float, bytes), _b)
    dispatcher.addSigFunc(TypeSig(int), _c)
    self.assertEqual(dispatcher._getDeclaredSigs(), [
      TypeSig(int), TypeSig(int, str, float, bytes), TypeSig(ARGS[int]),
    ])

  def test_cached_function_peek(self) -> None:
    class Owner:
      d = Dispatcher()

    with self.assertRaises(RecursionError) as context:
      Owner.__dict__['d']._getCachedFunction(_recursion=True)
    self.assertEqual(context.exception.args, ())
    compiled = Owner.__dict__['d']._getCachedFunction()
    peeked = Owner.__dict__['d']._getCachedFunction(_recursion=True)
    self.assertIs(peeked, compiled)
    self.assertIs(Owner.d, compiled)

  def test_exact_entries_ignore_farther_variadic(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int, int), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 1)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (0, _a)})

  def test_exact_entries_look_past_a_farther_variadic(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int, int), _a, 2)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 2)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _c, 1)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (1, _c)})

  def test_exact_entries_take_most_recent_of_three(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(int, int), _a, 1)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _b, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _c, 0)
    self.assertEqual(dispatcher._getExactEntries(), {(int, int): (0, _c)})

  def test_cast_order_of_two_distances(self) -> None:
    pairs = [(TypeSig(int), _a), (TypeSig(str), _b)]
    self.assertEqual(Dispatcher._getCastOrder(pairs, [1, 2]),
                     [pairs[1], pairs[0]])

  def test_variadic_order_of_three_at_one_distance(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[int]), _a, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[str]), _b, 0)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[float]), _c, 0)
    nearest = [f for _, f in dispatcher._getVariadicOrder(True)]
    farthest = [f for _, f in dispatcher._getVariadicOrder(False)]
    self.assertEqual(nearest, [_c, _b, _a])
    self.assertEqual(farthest, [_c, _b, _a])
