"""
TestTypeSig tests 'TypeSig' from 'worktoy.dispatch', apart from the
validation of declared entries.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS, OWNER, ARGS
from worktoy.dispatch import TypeSig
from . import DispatchTest


class TestTypeSig(DispatchTest):
  """
  A dispatcher keys its lookup by the classes of the arguments, so a
  signature must hash and compare by its classes in order, an 'ARGS'
  entry by its inner type, and must be able to stand in for a class that
  does not exist yet through 'THIS'. The tests pin the entries, the
  signature of a call, the unpacking of a bare 'ARGS', equality, hash,
  iteration, membership, the texts, the copy with 'THIS' and 'OWNER'
  replaced, the swap and restore of 'THIS', and the bag.
  """

  def test_entries(self) -> None:
    sig = TypeSig(int, str)
    self.assertEqual(sig.getRawTypes(), (int, str))
    self.assertEqual(sig.getDeclaredTypes(), (int, str))
    self.assertEqual(len(sig), 2)
    self.assertEqual([*sig], [int, str])
    self.assertEqual(len(TypeSig()), 0)

  def test_from_args_uses_exact_classes(self) -> None:
    self.assertEqual(TypeSig.fromArgs(1, 'a', True), TypeSig(int, str, bool))
    self.assertNotEqual(TypeSig.fromArgs(True), TypeSig(int))
    self.assertEqual(TypeSig.fromArgs(), TypeSig())

  def test_star_args(self) -> None:
    self.assertEqual(TypeSig.starARGS(int, ARGS), (int, ARGS[object]))
    self.assertEqual(TypeSig.starARGS(int, ARGS[str]), (int, ARGS[str]))
    self.assertEqual(TypeSig.starARGS(ARGS, int), (ARGS[object], int))
    self.assertEqual(TypeSig.starARGS(), ())

  def test_equality(self) -> None:
    self.assertEqual(TypeSig(int, str), TypeSig(int, str))
    self.assertNotEqual(TypeSig(int, str), TypeSig(str, int))
    self.assertNotEqual(TypeSig(int), TypeSig(int, int))
    self.assertEqual(TypeSig(int, ARGS[str]), TypeSig(int, ARGS[str]))
    self.assertNotEqual(TypeSig(int, ARGS[str]), TypeSig(int, ARGS[int]))
    self.assertNotEqual(TypeSig(int), TypeSig(bool))
    self.assertIs(TypeSig(int).__eq__((int,)), NotImplemented)
    self.assertFalse(TypeSig(int) == (int,))

  def test_hash(self) -> None:
    self.assertEqual(hash(TypeSig(int, str)), hash((int, str)))
    self.assertEqual(len({TypeSig(int), TypeSig(int), TypeSig(str)}), 2)
    self.assertEqual(len({TypeSig(ARGS[int]), TypeSig(ARGS[int])}), 1)

  def test_contains_by_identity(self) -> None:
    sig = TypeSig(int, str)
    self.assertIn(int, sig)
    self.assertNotIn(bool, sig)
    self.assertNotIn(float, sig)

  def test_text(self) -> None:
    self.assertEqual(str(TypeSig(int, str)), '<TypeSig: [int, str]>')
    self.assertEqual(repr(TypeSig(int, str)), 'TypeSig(int, str)')
    self.assertEqual(str(TypeSig(int, ARGS[str])),
                     '<TypeSig: [int, ARGS[str]]>')
    self.assertEqual(repr(TypeSig()), 'TypeSig()')

  def test_copy_with_placeholders_replaced(self) -> None:
    sig = TypeSig(THIS, OWNER, int, ARGS[THIS])
    copied = sig(int, str)
    self.assertEqual(copied.getRawTypes(), (int, str, int, ARGS[int]))
    self.assertEqual(copied.getDeclaredTypes(), copied.getRawTypes())
    self.assertIsNot(copied, sig)
    self.assertEqual(sig.getRawTypes(), (THIS, OWNER, int, ARGS[THIS]))
    kept = sig()
    self.assertEqual(kept.getRawTypes(), (THIS, OWNER, int, ARGS[THIS]))
    self.assertEqual(sig(owner=str).getRawTypes(),
                     (THIS, str, int, ARGS[THIS]))

  def test_swap_and_restore_this(self) -> None:
    sig = TypeSig(THIS, int, ARGS[THIS])
    before = hash(sig)
    sig.swapTHIS(str)
    self.assertEqual(sig.getRawTypes(), (str, int, ARGS[str]))
    self.assertEqual(sig.getDeclaredTypes(), (THIS, int, ARGS[THIS]))
    self.assertNotEqual(hash(sig), before)
    sig.restoreTHIS()
    self.assertEqual(sig.getRawTypes(), (THIS, int, ARGS[THIS]))
    self.assertEqual(hash(sig), before)

  def test_bag_ignores_order(self) -> None:
    self.assertEqual(TypeSig(int, int, str).getBag(),
                     TypeSig(str, int, int).getBag())
    self.assertNotEqual(TypeSig(int, str).getBag(),
                        TypeSig(int, int).getBag())
    self.assertEqual(TypeSig(int, str).getBag(),
                     frozenset({(int, 1), (str, 1)}))
    sig = TypeSig(THIS)
    bag = sig.getBag()
    sig.swapTHIS(int)
    self.assertNotEqual(sig.getBag(), bag)

  def test_type_names(self) -> None:
    self.assertEqual(TypeSig._getTypeName(int), 'int')
    self.assertEqual(TypeSig._getTypeName(ARGS[int]), 'ARGS[int]')
    self.assertEqual(TypeSig._renderSignature((int, ARGS[int])),
                     '(int, ARGS[int])')

  def test_random_signatures(self) -> None:
    classes = (int, str, float, bytes, list)
    self.randomInteger.size = 4
    for _ in range(6):
      picks = tuple(classes[i % 5] for i in self.randomInteger.row)
      with self.subTest(picks=[c.__name__ for c in picks]):
        self.assertEqual(TypeSig(*picks), TypeSig(*picks))
        fromArgs = TypeSig.fromArgs(*(c() for c in picks))
        self.assertEqual(fromArgs, TypeSig(*picks))
        self.assertEqual(hash(TypeSig(*picks)), hash(picks))

  def test_equality_checks_every_entry(self) -> None:
    self.assertNotEqual(TypeSig(ARGS[int], str), TypeSig(ARGS[int], int))
    self.assertEqual(TypeSig(ARGS[int], str), TypeSig(ARGS[int], str))

  def test_static_helpers_reachable_on_signature(self) -> None:
    sig = TypeSig(int)
    self.assertEqual(sig.starARGS(int, ARGS), (int, ARGS[object]))
    self.assertEqual(sig._renderSignature((int, str)), '(int, str)')
    self.assertEqual(sig._getTypeName(str), 'str')
