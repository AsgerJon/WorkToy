"""
TestDispatcherRegistry tests the registrations of 'Dispatcher' from
'worktoy.dispatch': placement, the add methods, the roles, the method
kind, the clone and the texts.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType, MethodType

from worktoy.core.sentinels import THIS, ARGS
from worktoy.dispatch import Dispatcher, TypeSig, PermuterMethod
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from worktoy.waitaminute.desc import WriteOnceError
from worktoy.waitaminute.dispatch import DuplicateSignature
from . import DispatchTest


def _one(self: object, n: int) -> tuple:
  return 'one', n


def _two(self: object, s: str) -> tuple:
  return 'two', s


class TestDispatcherRegistry(DispatchTest):
  """
  A dispatcher takes its registrations one at a time from the namespace
  building it, refuses two functions at one signature, a flexible
  declaration where its classes are declared already, a second fallback
  or finalizer, and a method kind set after anything is registered. The
  tests pin each registration and refusal, the placement replacing
  'THIS', the clone with its copies, and the texts.
  """

  @staticmethod
  def _placed() -> tuple:
    """A plain class holding a fresh dispatcher at 'd', and that
    dispatcher, which a read of 'Owner.d' would compile into a function."""
    class Owner:
      d = Dispatcher()
    return Owner, Owner.__dict__['d']

  def test_functions_of_the_tests(self) -> None:
    self.assertEqual(_one(None, 1), ('one', 1))
    self.assertEqual(_two(None, 's'), ('two', 's'))

  def test_unplaced_dispatcher(self) -> None:
    dispatcher = Dispatcher()
    self.assertTrue(str(dispatcher).startswith('<Dispatcher object at'))
    self.assertIsNone(dispatcher.getFieldOwner())
    with self.assertRaises(MissingVariable) as context:
      dispatcher._getFieldName()
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, dispatcher)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Dispatcher.__field_name__: str'", str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      dispatcher._getFieldOwner()
    self.assertEqual(context.exception.varName, '__field_owner__')
    self.assertIs(context.exception.instance, dispatcher)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'Dispatcher.__field_owner__: type'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      dispatcher.__get__(None, int)
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, dispatcher)
    self.assertEqual(context.exception.expectedTypes, (str,))

  def test_placement(self) -> None:
    Owner, d = self._placed()
    self.assertIs(d.getFieldOwner(), Owner)
    self.assertEqual(d._getFieldName(), 'd')
    self.assertIs(d._getFieldOwner(), Owner)
    d.addSigFunc(TypeSig(int), _one)
    d.addVariadicSigFunc(TypeSig(ARGS[str]), _two)
    text = str(d)
    self.assertIn("Dispatcher at 'Owner.d'", text)
    self.assertIn('<TypeSig: [int]>', text)
    self.assertIn('<TypeSig: [ARGS[str]]>', text)
    self.assertEqual(repr(d), text)

  def test_placement_resolves_this(self) -> None:
    dispatcher = Dispatcher()
    dispatcher.addSigFunc(TypeSig(THIS), _one)
    dispatcher.addVariadicSigFunc(TypeSig(ARGS[THIS]), _one)
    dispatcher.addFlexSigFunc(TypeSig(THIS, int, str, float), _one)
    dispatcher.__set_name__(int, 'd')
    declared = [sig.getRawTypes() for sig in dispatcher._getDeclaredSigs()]
    self.assertEqual(declared,
                     [(int,), (int, int, str, float), (ARGS[int],)])
    self.assertEqual(dispatcher._getDeclaredSigs()[0].getDeclaredTypes(),
                     (THIS,))

  def test_add_sig_func(self) -> None:
    Owner, d = self._placed()
    self.assertIs(d.addSigFunc(TypeSig(int), _one), _one)
    self.assertEqual(d._getSigFuncList(), [(TypeSig(int), _one)])
    self.assertEqual(d._getSigDistances(), [0])
    d.addSigFunc(TypeSig(str), _two, 1)
    self.assertEqual(d._getSigDistances(), [0, 1])
    self.assertEqual(d._getSigFuncMap(),
                     {TypeSig(int): _one, TypeSig(str): _two})
    with self.assertRaises(DuplicateSignature) as context:
      d.addSigFunc(TypeSig(int), _two, 2)
    self.assertEqual(context.exception.sig, TypeSig(int))
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertIn('<TypeSig: [int]>', str(context.exception))
    self.assertIn('_one', str(context.exception))

  def test_registration_clears_compiled_function(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _one)
    self.assertEqual(Owner().d(1), ('one', 1))
    self.assertIsNotNone(d.__compiled_func__)
    d.addSigFunc(TypeSig(str), _two)
    self.assertIsNone(d.__compiled_func__)
    self.assertEqual(Owner().d('s'), ('two', 's'))

  def test_concrete_against_flexible(self) -> None:
    Owner, d = self._placed()
    d.addFlexSigFunc(TypeSig(int, str, float, bytes), _one)
    with self.assertRaises(DuplicateSignature) as context:
      d.addSigFunc(TypeSig(bytes, int, str, float), _two)
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertEqual(context.exception.sig, TypeSig(bytes, int, str, float))
    self.assertIn('[bytes, int, str, float]', str(context.exception))
    d.addSigFunc(TypeSig(bytes, int, str, float), _one)
    d.addSigFunc(TypeSig(str, int, float, bytes), _two, 1)
    self.assertEqual(len(d._getSigFuncList()), 2)

  def test_add_flex_sig_func(self) -> None:
    Owner, d = self._placed()
    self.assertIs(d.addFlexSigFunc(TypeSig(int, str, float, bytes), _one),
                  _one)
    self.assertEqual(d._getFlexDistances(), [0])
    with self.assertRaises(DuplicateSignature) as context:
      d.addFlexSigFunc(TypeSig(bytes, int, str, float), _two, 1)
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertEqual(context.exception.sig, TypeSig(bytes, int, str, float))
    self.assertIn('_two', str(context.exception))
    d.addSigFunc(TypeSig(int, int, str, str), _two)
    with self.assertRaises(DuplicateSignature) as context:
      d.addFlexSigFunc(TypeSig(str, str, int, int), _one)
    self.assertIs(context.exception.existing, _two)
    self.assertIs(context.exception.duplicate, _one)
    self.assertEqual(context.exception.sig, TypeSig(str, str, int, int))
    self.assertIn('[str, str, int, int]', str(context.exception))
    d.addFlexSigFunc(TypeSig(str, str, int, int), _two)
    d.addFlexSigFunc(TypeSig(float, float, int, int), _one, 1)
    d.addSigFunc(TypeSig(float, float, int, int), _two, 0)
    self.assertEqual(len(d._getFlexFuncs()), 3)

  def test_add_variadic_sig_func(self) -> None:
    Owner, d = self._placed()
    sig = TypeSig(int, ARGS[str])
    self.assertIs(d.addVariadicSigFunc(sig, _one), _one)
    d.addVariadicSigFunc(sig, _two, 1)
    self.assertEqual(d._getVariadicFuncs(), [(sig, _one), (sig, _two)])
    self.assertEqual(d._getVariadicDistances(), [0, 1])

  def test_fallback_and_finalizer(self) -> None:
    Owner, d = self._placed()
    with self.assertRaises(TypeException) as context:
      d.setFallbackFunction(5)
    self.assertEqual(context.exception.varName, '__fallback_func__')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes,
                     (FunctionType, MethodType))
    self.assertIn("'__fallback_func__'", str(context.exception))
    self.assertIs(d.setFallbackFunction(_one), _one)
    self.assertIs(d._getFallbackFunction(), _one)
    with self.assertRaises(DuplicateSignature) as context:
      d.setFallbackFunction(_two)
    self.assertEqual(context.exception.sig, 'fallback')
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertIn('fallback function', str(context.exception))
    with self.assertRaises(TypeException) as context:
      d.setFinalizerFunction('x')
    self.assertEqual(context.exception.varName, '__finalizer_func__')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes,
                     (FunctionType, MethodType))
    self.assertIn("'__finalizer_func__'", str(context.exception))
    self.assertIs(d.setFinalizerFunction(_two), _two)
    with self.assertRaises(DuplicateSignature) as context:
      d.setFinalizerFunction(_one)
    self.assertEqual(context.exception.sig, 'finalizer')
    self.assertIs(context.exception.existing, _two)
    self.assertIs(context.exception.duplicate, _one)
    self.assertIn('finalizer function', str(context.exception))

  def test_has_registrations(self) -> None:
    self.assertFalse(Dispatcher()._hasRegistrations())
    sigged = Dispatcher()
    sigged.addSigFunc(TypeSig(int), _one)
    self.assertTrue(sigged._hasRegistrations())
    fallen = Dispatcher()
    fallen.setFallbackFunction(_one)
    self.assertTrue(fallen._hasRegistrations())
    final = Dispatcher()
    final.setFinalizerFunction(_one)
    self.assertTrue(final._hasRegistrations())

  def test_method_kind(self) -> None:
    dispatcher = Dispatcher()
    self.assertIsNone(dispatcher.getMethodKind())
    with self.assertRaises(TypeError) as context:
      dispatcher.setMethodKind('classmethod')
    self.assertIn("not 'classmethod'", str(context.exception))
    dispatcher.setMethodKind(classmethod)
    self.assertIs(dispatcher.getMethodKind(), classmethod)
    dispatcher.setMethodKind(None)
    dispatcher.setMethodKind(staticmethod)
    dispatcher.addSigFunc(TypeSig(int), _one)
    with self.assertRaises(WriteOnceError) as context:
      dispatcher.setMethodKind(None)
    self.assertIs(context.exception.desc, dispatcher)
    self.assertIs(context.exception.oldValue, staticmethod)
    self.assertIsNone(context.exception.newValue)
    self.assertIn("'staticmethod'", str(context.exception))
    self.assertIn("'None'", str(context.exception))

  def test_adapt_to_kind(self) -> None:
    plain = Dispatcher()
    self.assertIs(plain._adaptToKind(_one), _one)
    def alone(n: int) -> tuple:
      return 'alone', n

    static = Dispatcher()
    static.setMethodKind(staticmethod)
    adapted = static._adaptToKind(alone)
    self.assertIsNot(adapted, alone)
    self.assertIs(static._adaptToKind(alone), adapted)
    self.assertEqual(adapted('receiver', 'n'), ('alone', 'n'))
    permuter = PermuterMethod(alone, Arrangement(('n',), (0,)))
    rebuilt = static._adaptToKind(permuter)
    self.assertIsInstance(rebuilt, PermuterMethod)
    self.assertIs(rebuilt.__wrapped__, adapted)
    self.assertEqual(rebuilt.arrangement, permuter.arrangement)

  def test_write_and_delete_refused(self) -> None:
    Owner, d = self._placed()
    owner = Owner()
    with self.assertRaises(ReadOnlyError) as context:
      owner.d = 5
    self.assertIs(context.exception.desc, d)
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.newVal, 5)
    self.assertIn("'Owner.d'", str(context.exception))
    self.assertIn("'5'", str(context.exception))
    with self.assertRaises(ProtectedError) as context:
      del owner.d
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, d)
    self.assertIsNone(context.exception.oldVal)
    self.assertIn("'Owner.d'", str(context.exception))

  def test_clone(self) -> None:
    original = Dispatcher()
    original.setMethodKind(staticmethod)
    original.addSigFunc(TypeSig(THIS), _one)
    original.addVariadicSigFunc(TypeSig(ARGS[str]), _two, 1)
    original.addFlexSigFunc(TypeSig(int, str, float, bytes), _one)
    original.setFallbackFunction(_one)
    original.setFinalizerFunction(_two)
    original.__set_name__(int, 'd')
    copy = original.clone()
    self.assertIsNone(copy.getFieldOwner())
    self.assertIsNone(copy.__compiled_func__)
    self.assertIs(copy.getMethodKind(), staticmethod)
    self.assertIs(copy.__static_adapters__, original.__static_adapters__)
    sigPairs = zip(copy._getDeclaredSigs(), original._getDeclaredSigs())
    for mine, theirs in sigPairs:
      with self.subTest(sig=str(theirs)):
        self.assertIsNot(mine, theirs)
        self.assertEqual(mine.getRawTypes(), theirs.getRawTypes())
        self.assertEqual(mine.getDeclaredTypes(), theirs.getDeclaredTypes())
    self.assertEqual(copy._getSigDistances(), [0])
    self.assertEqual(copy._getVariadicDistances(), [1])
    self.assertEqual(copy._getFlexDistances(), [0])
    self.assertIs(copy._getFallbackFunction(),
                  original._getFallbackFunction())
    self.assertIs(copy._getFinalizerFunction(),
                  original._getFinalizerFunction())
    copy.restoreTHIS()
    self.assertEqual(copy._getSigFuncList()[0][0].getRawTypes(), (THIS,))
    self.assertEqual(original._getSigFuncList()[0][0].getRawTypes(), (int,))
    copy.swapAllTHIS(str)
    self.assertEqual(copy._getSigFuncList()[0][0].getRawTypes(), (str,))

  def test_clone_of_bare_dispatcher(self) -> None:
    copy = Dispatcher().clone()
    self.assertEqual(copy._getSigFuncList(), [])
    self.assertIsNone(copy.__variadic_funcs__)
    self.assertIsNone(copy.__flex_funcs__)
    self.assertIsNone(copy.__fallback_func__)
    self.assertIsNone(copy.__finalizer_func__)
    self.assertIsNone(copy.getMethodKind())

  def test_flexible_and_concrete_at_other_distances(self) -> None:
    nearer, nd = self._placed()
    nd.addSigFunc(TypeSig(bytes, bytes, int, int), _two, 0)
    nd.addFlexSigFunc(TypeSig(int, int, bytes, bytes), _one, 1)
    farther, fd = self._placed()
    fd.addSigFunc(TypeSig(bytes, bytes, int, int), _two, 2)
    fd.addFlexSigFunc(TypeSig(int, int, bytes, bytes), _one, 1)
    self.assertEqual(len(nd._getFlexFuncs()), 1)
    self.assertEqual(len(fd._getFlexFuncs()), 1)

  def test_conflict_found_past_an_entry_of_another_distance(self) -> None:
    Owner, d = self._placed()
    d.addFlexSigFunc(TypeSig(int, str, float, bytes), _one, 1)
    d.addFlexSigFunc(TypeSig(int, int, str, str), _one, 0)
    with self.assertRaises(DuplicateSignature) as context:
      d.addSigFunc(TypeSig(str, str, int, int), _two, 0)
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertEqual(context.exception.sig, TypeSig(str, str, int, int))
    self.assertIn('[str, str, int, int]', str(context.exception))
    Other, od = self._placed()
    od.addSigFunc(TypeSig(int, str, float, bytes), _one, 1)
    od.addSigFunc(TypeSig(int, int, str, str), _one, 0)
    with self.assertRaises(DuplicateSignature) as context:
      od.addFlexSigFunc(TypeSig(str, str, int, int), _two, 0)
    self.assertIs(context.exception.existing, _one)
    self.assertIs(context.exception.duplicate, _two)
    self.assertEqual(context.exception.sig, TypeSig(str, str, int, int))
    self.assertIn('_two', str(context.exception))

  def test_bags_compared_whole_not_as_subsets(self) -> None:
    Owner, d = self._placed()
    d.addFlexSigFunc(TypeSig(int, str, float, bytes), _one)
    d.addSigFunc(TypeSig(int, str, float, bytes, list), _two)
    d.addFlexSigFunc(TypeSig(int, str, float, bytes, list, dict), _two)
    d.addSigFunc(TypeSig(int, str, float, list, dict), _one)
    d.addFlexSigFunc(TypeSig(int, str, float, list), _two)
    self.assertEqual(len(d._getFlexFuncs()), 3)
    self.assertEqual(len(d._getSigFuncList()), 2)

  def test_restore_this_on_every_kind_of_signature(self) -> None:
    original = Dispatcher()
    original.addSigFunc(TypeSig(THIS), _one)
    original.addFlexSigFunc(TypeSig(THIS, int, str, float), _one)
    original.addVariadicSigFunc(TypeSig(ARGS[THIS]), _one)
    original.__set_name__(int, 'd')
    copy = original.clone()
    copy.restoreTHIS()
    self.assertEqual([sig.getRawTypes() for sig in copy._getDeclaredSigs()],
                     [(THIS,), (THIS, int, str, float), (ARGS[THIS],)])
    declared = [sig.getRawTypes() for sig in original._getDeclaredSigs()]
    self.assertEqual(declared,
                     [(int,), (int, int, str, float), (ARGS[int],)])
