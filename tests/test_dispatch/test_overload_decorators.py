"""
TestOverloadDecorators tests the decorators of 'overload' from
'worktoy.dispatch': the call, 'flex', 'fallback' and 'finalize'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from worktoy.core.sentinels import ARGS, DELETED
from worktoy.dispatch import overload, TypeSig, PermuterMethod
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import BareOverload
from worktoy.waitaminute.meta import MixedMethodKind
from . import DispatchTest


def _pair(self: object, a: str, b: int) -> tuple:
  return a, b


def _quad(self: object, s: str, i: int, f: float, b: bytes) -> tuple:
  return s, i, f, b


class TestOverloadDecorators(DispatchTest):
  """
  '@overload(...)' checks its signature where it is written and returns
  a decorator, which returns a record, new or the one below it in a
  stack; 'flex', 'fallback' and 'finalize' declare the other roles the
  same way. The tests pin each decorator on a function and on a record,
  the method kinds taken from the layers, the refusals of a bare
  decorator, a keyword, an invalid entry and an uncallable, and the
  two shapes of a flexible declaration.
  """

  def test_functions_of_the_tests(self) -> None:
    self.assertEqual(_quad(None, 's', 1, 1.5, b'b'), ('s', 1, 1.5, b'b'))

  def test_decorator_builds_record(self) -> None:
    decorator = overload(int)
    self.assertTrue(callable(decorator))
    record = decorator(_pair)
    self.assertIsInstance(record, overload)
    self.assertEqual([*record], [(TypeSig(int), _pair)])
    self.assertIsNone(record.getMethodKind())

  def test_stacked_decorators_share_record(self) -> None:
    inner = overload(int)(_pair)
    outer = overload(str)(inner)
    self.assertIs(outer, inner)
    self.assertEqual([*outer],
                     [(TypeSig(int), _pair), (TypeSig(str), _pair)])

  def test_variadic_signature(self) -> None:
    record = overload(int, ARGS)(_pair)
    self.assertEqual([*record], [])
    self.assertEqual(record.getVariadics(),
                     [(TypeSig(int, ARGS[object]), _pair)])

  def test_method_kinds_from_layers(self) -> None:
    self.assertIs(overload(int)(classmethod(_pair)).getMethodKind(),
                  classmethod)
    self.assertIs(overload(int)(staticmethod(_pair)).getMethodKind(),
                  staticmethod)
    between = overload(str)(classmethod(overload(int)(_pair)))
    self.assertIs(between.getMethodKind(), classmethod)
    self.assertEqual(len([*between]), 2)
    with self.assertRaises(MixedMethodKind) as context:
      overload(str)(staticmethod(overload(int)(classmethod(_pair))))
    self.assertIsNone(context.exception.className)
    self.assertEqual(context.exception.overloadName, '_pair')
    self.assertEqual(context.exception.kinds, (staticmethod, classmethod))
    self.assertIn("'_pair'", str(context.exception))
    with self.assertRaises(MixedMethodKind) as context:
      overload(int)(staticmethod(classmethod(_pair)))
    self.assertIsNone(context.exception.className)
    self.assertEqual(context.exception.overloadName, '_pair')
    self.assertEqual(context.exception.kinds, (staticmethod, classmethod))
    self.assertIn("a 'staticmethod' and as a 'classmethod'",
                  str(context.exception))

  def test_keyword_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      overload(int, key=1)
    self.assertEqual(str(context.exception),
                     "overload() got an unexpected keyword argument 'key'")

  def test_bare_decorator_refused(self) -> None:
    record = overload(int)(_pair)
    cases = (
      (overload, _pair, 'overload'),
      (overload, classmethod(_pair), 'overload'),
      (overload, record, 'overload'),
      (overload.flex, _pair, 'overload.flex'),
      (overload.flex, staticmethod(record), 'overload.flex'),
    )
    for decorator, entry, name in cases:
      with self.subTest(decorator=name, entry=type(entry).__name__):
        with self.assertRaises(BareOverload) as context:
          decorator(entry)
        self.assertEqual(context.exception.decorator, name)
        self.assertIs(context.exception.func, entry)
        self.assertIn("'@%s'" % name, str(context.exception))
    with self.assertRaises(TypeException) as context:
      overload(int, _pair)
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertIs(context.exception.actualObject, _pair)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[1]'", str(context.exception))

  def test_entries_checked_at_declaration(self) -> None:
    with self.assertRaises(TypeError) as context:
      overload(None)
    self.assertIn("position 0 of the signature is 'None'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      overload(5)
    self.assertEqual(context.exception.varName, 'types[0]')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[0]'", str(context.exception))
    with self.assertRaises(TypeError) as context:
      overload(DELETED)
    self.assertIn("the sentinel 'DELETED'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      overload.flex(int, ARGS[str])
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertEqual(context.exception.actualObject, ARGS[str])
    self.assertIs(context.exception.actualType, ARGS)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[1]'", str(context.exception))

  def test_uncallable_refused(self) -> None:
    for entry in (5, classmethod(5)):
      with self.subTest(entry=entry):
        with self.assertRaises(TypeException) as context:
          overload(int)(entry)
        self.assertEqual(context.exception.varName, 'func')
        self.assertEqual(context.exception.actualObject, 5)
        self.assertIs(context.exception.actualType, int)
        self.assertEqual(context.exception.expectedTypes, (FunctionType,))
        self.assertIn("'func'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      overload.fallback(5)
    self.assertEqual(context.exception.varName, 'func')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertEqual(context.exception.expectedTypes, (FunctionType,))
    self.assertIn("'function'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      overload.finalize(staticmethod(5))
    self.assertEqual(context.exception.varName, 'func')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertEqual(context.exception.expectedTypes, (FunctionType,))
    self.assertIn("'func'", str(context.exception))

  def test_flex_of_few_classes_registers_every_order(self) -> None:
    record = overload.flex(str, int)(_pair)
    pairs = [*record]
    self.assertEqual([sig for sig, _ in pairs],
                     [TypeSig(str, int), TypeSig(int, str)])
    for sig, load in pairs:
      with self.subTest(sig=str(sig)):
        self.assertIsInstance(load, PermuterMethod)
        self.assertIs(load.__wrapped__, _pair)
    self.assertEqual(pairs[0][1](None, 'a', 1), ('a', 1))
    self.assertEqual(pairs[1][1](None, 1, 'a'), ('a', 1))
    self.assertEqual(record.getFlexes(), [])
    self.assertIs(record._getLatestFunc(), _pair)
    stacked = overload(float)(record)
    self.assertIs(stacked, record)
    self.assertIs(dict([*record])[TypeSig(float)], _pair)

  def test_flex_of_many_classes_registers_once(self) -> None:
    record = overload.flex(str, int, float, bytes)(_quad)
    self.assertEqual([*record], [])
    self.assertEqual(record.getFlexes(),
                     [(TypeSig(str, int, float, bytes), _quad)])
    self.assertIs(record._getLatestFunc(), _quad)
    self.assertIs(overload.flex(bytes, str, int, float)(record), record)
    self.assertEqual(len(record.getFlexes()), 2)

  def test_flex_on_record_and_with_kind(self) -> None:
    record = overload.flex(str, int)(overload(float)(_pair))
    self.assertEqual(len([*record]), 3)
    kinded = overload.flex(str, int)(classmethod(_pair))
    self.assertIs(kinded.getMethodKind(), classmethod)

  def test_fallback_and_finalizer(self) -> None:
    record = overload.fallback(_pair)
    self.assertTrue(record.isFallback())
    self.assertIs(record.getFallback(), _pair)
    self.assertIs(record._getLatestFunc(), _pair)
    self.assertFalse(record.isFinalizer())
    record = overload.finalize(classmethod(_pair))
    self.assertTrue(record.isFinalizer())
    self.assertIs(record.getFinalizer(), _pair)
    self.assertIs(record.getMethodKind(), classmethod)
    stacked = overload.finalize(overload.fallback(overload(int)(_pair)))
    self.assertEqual([*stacked], [(TypeSig(int), _pair)])
    self.assertIs(stacked.getFallback(), _pair)
    self.assertIs(stacked.getFinalizer(), _pair)
    with self.assertRaises(MixedMethodKind) as context:
      overload.fallback(staticmethod(overload(int)(classmethod(_pair))))
    self.assertIsNone(context.exception.className)
    self.assertEqual(context.exception.overloadName, '_pair')
    self.assertEqual(context.exception.kinds, (staticmethod, classmethod))
    self.assertIn("'_pair'", str(context.exception))

  def test_stack_on(self) -> None:
    record, func = overload._stackOn(_pair)
    self.assertIsInstance(record, overload)
    self.assertIs(func, _pair)
    again, latest = overload._stackOn(record)
    self.assertIs(again, record)
    self.assertIs(latest, _pair)

  def test_refuse_bare_passes_signatures(self) -> None:
    overload._refuseBare('overload', int, str)
    overload._refuseBare('overload', int)
    overload._refuseBare('overload')

  def test_three_classes_still_expand(self) -> None:
    def triple(self: object, a: str, b: int, c: float) -> tuple:
      return a, b, c

    record = overload.flex(str, int, float)(triple)
    self.assertEqual(len([*record]), 6)
    self.assertEqual(record.getFlexes(), [])
    func = dict([*record])[TypeSig(float, str, int)]
    self.assertEqual(func(None, 1.5, 'a', 1), ('a', 1, 1.5))

  def test_function_among_classes_is_no_bare_decorator(self) -> None:
    with self.assertRaises(TypeException) as context:
      overload(_pair, int)
    self.assertEqual(context.exception.varName, 'types[0]')
    self.assertIs(context.exception.actualObject, _pair)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[0]'", str(context.exception))

  def test_static_helpers_reachable_on_record(self) -> None:
    record = overload(int)(_pair)
    self.assertEqual(record.peelMethodKinds(_pair), ((), _pair))
    record._refuseUncallable(_pair)
    record._refuseKeywords()
    self.assertIsNone(record.agreeMethodKind((), 'x'))
