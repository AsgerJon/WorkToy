"""
TestOverloadRecord tests the 'overload' record of 'worktoy.dispatch':
what one holds and reports, apart from the decorators that build it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from functools import partial

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.meta import MixedMethodKind
from . import DispatchTest


def _first(self: object, n: int) -> str:
  """The first function."""
  return 'first'


def _second(self: object, s: str) -> str:
  return 'second'


class TestOverloadRecord(DispatchTest):
  """
  An 'overload' object records the signatures of one function and the
  kind of method it is, for the namespace that builds the dispatcher.
  The tests pin the static helpers that take method kinds apart and
  agree on one, the empty record, the registration of signatures with
  the latest function, the kinds a stack may declare, the names read off
  the function, the two refusals of a misplaced record, and the texts.
  """

  def test_functions_of_the_tests(self) -> None:
    self.assertEqual((_first(None, 1), _second(None, 's')),
                     ('first', 'second'))

  def test_peel_method_kinds(self) -> None:
    class Sub(classmethod):
      pass

    self.assertEqual(overload.peelMethodKinds(_first), ((), _first))
    self.assertEqual(overload.peelMethodKinds(classmethod(_first)),
                     ((classmethod,), _first))
    stacked = staticmethod(classmethod(_first))
    self.assertEqual(overload.peelMethodKinds(stacked),
                     ((staticmethod, classmethod), _first))
    self.assertEqual(overload.peelMethodKinds(Sub(_first)),
                     ((classmethod,), _first))
    self.assertEqual(overload.peelMethodKinds(5), ((), 5))

  def test_agree_method_kind(self) -> None:
    self.assertIsNone(overload.agreeMethodKind((), 'f'))
    self.assertIs(overload.agreeMethodKind((classmethod,), 'f'), classmethod)
    twice = (staticmethod, staticmethod)
    self.assertIs(overload.agreeMethodKind(twice, 'f'), staticmethod)
    with self.assertRaises(MixedMethodKind) as context:
      overload.agreeMethodKind((classmethod, staticmethod), 'f', 'Owner')
    self.assertEqual(context.exception.className, 'Owner')
    self.assertEqual(context.exception.overloadName, 'f')
    self.assertEqual(context.exception.kinds, (classmethod, staticmethod))
    self.assertIn("'Owner.f'", str(context.exception))
    self.assertIn("a 'classmethod' and as a 'staticmethod'",
                  str(context.exception))
    self.assertIsInstance(context.exception, SyntaxError)

  def test_function_name(self) -> None:
    self.assertEqual(overload._getFunctionName(_first), '_first')
    bound = partial(_first, None)
    self.assertEqual(overload._getFunctionName(bound), repr(bound))

  def test_empty_record(self) -> None:
    record = overload(_root=True)
    self.assertIsInstance(record, overload)
    self.assertIsNone(record.getMethodKind())
    self.assertEqual(record.getVariadics(), [])
    self.assertEqual(record.getFlexes(), [])
    self.assertFalse(record.isFallback())
    self.assertIsNone(record.getFallback())
    self.assertFalse(record.isFinalizer())
    self.assertIsNone(record.getFinalizer())
    self.assertEqual([*record], [])
    self.assertEqual(str(record),
                     'overload with no function registered so far')
    with self.assertRaises(RuntimeError) as context:
      record._getLatestFunc()
    self.assertIn('no function has been registered', str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      _ = record.__name__
    self.assertEqual(context.exception.varName, '__name__')
    self.assertIs(context.exception.instance, record)
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'overload.__name__'!")

  def test_signatures_registered_with_latest_function(self) -> None:
    record = overload(_root=True)
    record._addSigFunc(TypeSig(int), _first)
    self.assertEqual([*record], [(TypeSig(int), _first)])
    self.assertIs(record._getLatestFunc(), _first)
    record._extendLatest(TypeSig(str))
    self.assertEqual([*record],
                     [(TypeSig(int), _first), (TypeSig(str), _first)])
    record._addSigFunc(TypeSig(int, ARGS[str]), _second)
    self.assertEqual(record.getVariadics(),
                     [(TypeSig(int, ARGS[str]), _second)])
    self.assertIs(record._getLatestFunc(), _second)
    record._addSigFunc(TypeSig(int), _second)
    self.assertEqual([*record],
                     [(TypeSig(int), _second), (TypeSig(str), _first)])

  def test_kinds_taken_along_a_stack(self) -> None:
    record = overload(_root=True)
    record._addSigFunc(TypeSig(int), _first)
    record._takeMethodKinds(())
    self.assertIsNone(record.getMethodKind())
    record._takeMethodKinds((classmethod,))
    self.assertIs(record.getMethodKind(), classmethod)
    record._takeMethodKinds(())
    self.assertIs(record.getMethodKind(), classmethod)
    with self.assertRaises(MixedMethodKind) as context:
      record._takeMethodKinds((staticmethod,))
    self.assertEqual(context.exception.overloadName, '_first')
    self.assertEqual(context.exception.kinds, (staticmethod, classmethod))
    self.assertIsNone(context.exception.className)
    self.assertIn("'_first'", str(context.exception))
    self.assertIn("a 'staticmethod' and as a 'classmethod'",
                  str(context.exception))

  def test_names_read_off_function(self) -> None:
    record = overload(int)(_first)
    self.assertEqual(record.__name__, '_first')
    self.assertEqual(record.__doc__, overload.__doc__)
    with self.assertRaises(MissingVariable) as context:
      _ = record.nothing
    self.assertEqual(context.exception.varName, 'nothing')
    self.assertIs(context.exception.instance, record)
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'overload.nothing'!")

  def test_place_in_plain_class_refused(self) -> None:
    record = overload(int)(_first)
    with self.assertRaises(TypeError) as context:
      record.__set_name__(int, 'take')
    self.assertIn("The class body of 'int' leaves the 'overload' of 'take'",
                  str(context.exception))
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        take = overload(int)(_first)
    exception = context.exception.__cause__ or context.exception
    self.assertIn("The class body of 'Plain' leaves the 'overload'",
                  str(exception))
    self.assertIn("of 'take'", str(exception))

  def test_call_refused(self) -> None:
    record = overload(int)(_first)
    with self.assertRaises(TypeError) as context:
      record(None, 1)
    self.assertIn("The 'overload' of '_first' was called",
                  str(context.exception))

  def test_text(self) -> None:
    record = overload(int)(_first)
    text = str(record)
    self.assertIn("overload of function: '_first'", text)
    self.assertIn('<TypeSig: [int]>', text)
    self.assertEqual(repr(record), text)
    record = overload.finalize(overload.fallback(overload(int, ARGS[str])(
        overload.flex(str, int, float, bytes)(overload(str)(_first)))))
    text = str(record)
    parts = (
      '<TypeSig: [str]>',
      '<TypeSig: [str, int, float, bytes]> in any order',
      '<TypeSig: [int, ARGS[str]]>', 'the fallback', 'the finalizer',
    )
    for part in parts:
      with self.subTest(part=part):
        self.assertIn(part, text)
