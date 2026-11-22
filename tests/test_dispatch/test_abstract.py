"""
TestAbstract tests the 'abstract' record of 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import abstract, overload
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import BareOverload
from worktoy.waitaminute.meta import MixedMethodKind
from . import DispatchTest


def _dots(self, index: int, role: int) -> int: ...


def _passed(self) -> None:
  pass


def _documented(self) -> int:
  """The number of rows."""


def _returnsNone(self) -> None:
  return None


def _returns(self) -> int:
  return 3


def _raises(self) -> int:
  raise NotImplementedError


def _docReturn(self) -> str:
  """text"""
  return 'text'


def _generates(self):
  yield


async def _awaits(self): ...


class TestAbstract(DispatchTest):
  """
  '@abstract' over a blank function gives a record of that function,
  which keeps its name, its docstring and the shape of its parameters,
  and does nothing when called. A function with a body is refused, and
  so is anything that is no ordinary function. The record may stand
  under '@classmethod' or '@staticmethod', and at any position among the
  '@overload' decorators of a stack. The tests pin the blank check, the
  shape of a function and whether one shape fits another, each position
  beside '@overload', and where a record may not go.
  """

  @staticmethod
  def _blank() -> FunctionType:
    def one(self, index: int) -> int: ...

    return one

  @staticmethod
  def _pair() -> FunctionType:
    def two(self, index: int, text: str) -> int: ...

    return two

  def test_blank_bodies(self) -> None:
    for func in (_dots, _passed, _documented, _returnsNone):
      with self.subTest(func=func.__name__):
        record = abstract(func)
        self.assertIsInstance(record, abstract)
        self.assertIs(record.__wrapped__, func)
        self.assertEqual(record.__name__, func.__name__)
        self.assertEqual(record.__qualname__, func.__qualname__)
        self.assertEqual(record.__module__, func.__module__)
        self.assertEqual(record.__doc__, func.__doc__)
        self.assertIsNone(record())
        self.assertIsNone(record(self, 1, 2, key=3))
        self.assertIsNone(func(*[None] * func.__code__.co_argcount))
    self.assertEqual(abstract(_documented).__doc__, 'The number of rows.')
    self.assertEqual(str(abstract(_dots)), "abstract '_dots'")
    self.assertEqual(repr(abstract(_dots)), "abstract '_dots'")

  def test_body_refused(self) -> None:
    self.assertEqual(_returns(None), 3)
    self.assertEqual(_docReturn(None), 'text')
    with self.assertRaises(NotImplementedError):
      _raises(None)
    for func in (_returns, _raises, _docReturn):
      with self.subTest(func=func.__name__):
        with self.assertRaises(TypeError) as context:
          abstract(func)
        expected = "The function '%s' under '@abstract' has a body."
        self.assertIn(expected % func.__name__, str(context.exception))

  def test_generator_and_coroutine_refused(self) -> None:
    self.assertEqual([*_generates(None)], [None])
    for func in (_generates, _awaits):
      with self.subTest(func=func.__name__):
        with self.assertRaises(TypeError) as context:
          abstract(func)
        expected = ("The function '%s' under '@abstract' is a generator "
                    "or a coroutine function.")
        self.assertIn(expected % func.__name__, str(context.exception))

  def test_not_a_function(self) -> None:
    for wrong in (3, len, classmethod(3)):
      with self.subTest(wrong=wrong):
        with self.assertRaises(TypeException) as context:
          abstract(wrong)
        self.assertEqual(context.exception.varName, 'func')
        self.assertEqual(context.exception.expectedTypes, (FunctionType,))
        self.assertIn("'func'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      abstract(abstract(_dots))
    self.assertEqual(context.exception.varName, 'func')
    self.assertIsInstance(context.exception.actualObject, abstract)
    self.assertIs(context.exception.actualType, abstract)
    self.assertIn("'func'", str(context.exception))

  def test_kinds(self) -> None:
    made = abstract(classmethod(_documented))
    self.assertIsInstance(made, classmethod)
    self.assertIsInstance(made.__func__, abstract)
    self.assertIs(made.__func__.__wrapped__, _documented)
    unit = abstract(staticmethod(_passed))
    self.assertIsInstance(unit, staticmethod)
    self.assertIsInstance(unit.__func__, abstract)
    with self.assertRaises(MixedMethodKind) as context:
      abstract(classmethod(staticmethod(_passed)))
    self.assertIsNone(context.exception.className)
    self.assertEqual(context.exception.overloadName, '_passed')
    self.assertEqual(context.exception.kinds, (classmethod, staticmethod))
    self.assertIn("'_passed'", str(context.exception))

  def test_shape(self) -> None:
    def starred(self, a, *args, key, **kwargs): ...

    def bare(*args): ...

    def empty(): ...

    shapeOf = abstract.shapeOf
    self.assertEqual(shapeOf(_dots, None), (2, False, (), False))
    self.assertEqual(shapeOf(_dots, classmethod), (2, False, (), False))
    self.assertEqual(shapeOf(_dots, staticmethod), (3, False, (), False))
    self.assertEqual(shapeOf(starred, None), (1, True, ('key',), True))
    self.assertEqual(shapeOf(bare, None), (0, True, (), False))
    self.assertEqual(shapeOf(bare, staticmethod), (0, True, (), False))
    self.assertEqual(shapeOf(empty, None), (-1, False, (), False))
    self.assertEqual(shapeOf(empty, staticmethod), (0, False, (), False))
    record = abstract(_dots)
    self.assertEqual(record.getShape(None), (2, False, (), False))
    self.assertEqual(record.getShape(staticmethod), (3, False, (), False))

  def test_fits(self) -> None:
    fits = abstract.fits
    plain = (2, False, (), False)
    self.assertTrue(fits(plain, (2, False, (), False)))
    self.assertFalse(fits(plain, (1, False, (), False)))
    self.assertFalse(fits(plain, (3, False, (), False)))
    self.assertTrue(fits(plain, (0, True, (), False)))
    self.assertTrue(fits(plain, (2, True, (), False)))
    self.assertFalse(fits(plain, (3, True, (), False)))
    self.assertFalse(fits(plain, (-1, False, (), False)))
    #  Two equal counts that are two objects, as large numbers are.
    large = (int('100000'), False, (), False)
    self.assertTrue(fits((100000, False, (), False), large))
    starred = (1, True, (), False)
    self.assertTrue(fits(starred, (1, True, (), False)))
    self.assertTrue(fits(starred, (0, True, (), False)))
    self.assertFalse(fits(starred, (2, True, (), False)))
    self.assertFalse(fits(starred, (1, False, (), False)))
    keyed = (0, False, ('role',), False)
    self.assertTrue(fits(keyed, (0, False, ('role',), False)))
    self.assertTrue(fits(keyed, (0, False, (), True)))
    self.assertFalse(fits(keyed, (0, False, (), False)))
    self.assertFalse(fits(keyed, (0, False, ('other',), False)))
    doubled = (0, False, (), True)
    self.assertTrue(fits(doubled, (0, False, (), True)))
    self.assertFalse(fits(doubled, (0, False, ('role',), False)))
    self.assertTrue(fits((0, False, (), False), (0, False, ('more',), True)))

  def test_describe(self) -> None:
    describe = abstract.describe
    self.assertEqual(describe(None, (2, False, (), False)),
                     'a method taking 2 by position')
    self.assertEqual(describe(classmethod, (0, False, (), False)),
                     'a classmethod taking 0 by position')
    self.assertEqual(
        describe(staticmethod, (1, True, ('urgent', 'late'), True)),
        "a staticmethod taking 1 or more by position, 'urgent' by "
        "keyword, 'late' by keyword, any keyword")

  def test_any_position_beside_overload(self) -> None:
    lower = self._blank()
    below = overload(str)(abstract(lower))
    upper = self._blank()
    above = abstract(overload(str)(upper))
    middle = self._blank()
    between = overload(bytes)(abstract(overload(str)(middle)))
    for record, func in ((below, lower), (above, upper), (between, middle)):
      with self.subTest(func=func):
        self.assertIsInstance(record, overload)
        held = [held for _, held in record]
        self.assertTrue(all(isinstance(one, abstract) for one in held))
        self.assertTrue(all(one is held[0] for one in held))
        self.assertIs(held[0].__wrapped__, func)
        self.assertIs(record._getLatestFunc(), held[0])
    self.assertEqual([sig.getRawTypes() for sig, _ in below], [(str,)])
    self.assertEqual([sig.getRawTypes() for sig, _ in above], [(str,)])
    self.assertEqual([sig.getRawTypes() for sig, _ in between],
                     [(str,), (bytes,)])
    wrapped = classmethod(overload(int)(self._blank()))
    self.assertIs(abstract(wrapped), wrapped)
    self.assertIsInstance(wrapped.__func__._getLatestFunc(), abstract)
    self.assertIs(wrapped.__func__.getMethodKind(), None)
    with self.assertRaises(TypeException) as context:
      abstract(below)
    self.assertEqual(context.exception.varName, 'func')
    self.assertIn("'func'", str(context.exception))

  def test_flexible_and_variadic(self) -> None:
    lower = abstract(self._pair())
    below = overload.flex(int, str)(lower)
    self.assertEqual([sig.getRawTypes() for sig, _ in below],
                     [(int, str), (str, int)])
    self.assertTrue(all(held is lower for _, held in below))
    self.assertIs(below._getLatestFunc(), lower)
    above = abstract(overload.flex(int, str)(self._pair()))
    self.assertEqual([sig.getRawTypes() for sig, _ in above],
                     [(int, str), (str, int)])
    held = [held for _, held in above]
    self.assertIsInstance(held[0], abstract)
    self.assertIs(held[0], held[1])

    def four(self, n: int, s: str, x: float, b: bytes) -> None: ...

    def many(self, s: str, *n: int) -> None: ...

    wide = abstract(overload.flex(int, str, float, bytes)(four))
    self.assertEqual([*wide], [])
    self.assertEqual(len(wide.getFlexes()), 1)
    self.assertIsInstance(wide.getFlexes()[0][1], abstract)
    self.assertIs(wide.getFlexes()[0][1].__wrapped__, four)
    tail = abstract(overload(str, ARGS[int])(many))
    self.assertEqual(len(tail.getVariadics()), 1)
    self.assertIsInstance(tail.getVariadics()[0][1], abstract)
    self.assertIs(tail.getVariadics()[0][1].__wrapped__, many)

  def test_fallback_and_finalizer_refused(self) -> None:
    def rest(self, *args) -> None: ...

    attempts = (
      ('fallback', lambda: overload.fallback(abstract(rest))),
      ('finalizer', lambda: overload.finalize(abstract(rest))),
      ('fallback', lambda: abstract(overload.fallback(rest))),
      ('finalizer', lambda: abstract(overload.finalize(rest))),
    )
    for role, attempt in attempts:
      with self.subTest(role=role):
        with self.assertRaises(TypeError) as context:
          attempt()
        expected = "The %s 'rest' is declared abstract." % role
        self.assertIn(expected, str(context.exception))

  def test_bare_overload(self) -> None:
    record = abstract(self._blank())
    with self.assertRaises(BareOverload) as context:
      overload(record)
    self.assertEqual(context.exception.decorator, 'overload')
    self.assertIs(context.exception.func, record)
    self.assertIn("'@overload'", str(context.exception))
    with self.assertRaises(BareOverload) as context:
      overload.flex(record)
    self.assertEqual(context.exception.decorator, 'overload.flex')
    self.assertIs(context.exception.func, record)
    self.assertIn("'@overload.flex'", str(context.exception))

  def test_only_where_a_space_hook_took_it(self) -> None:
    class Deaf(type):
      """A metaclass whose namespace takes no record."""

    record = abstract(self._blank())
    self.assertIs(abstract.__abc_only__, False)
    self.assertIs(record.__abc_only__, False)
    for mcls in (type, Deaf):
      with self.subTest(mcls=mcls):
        with self.assertRaises(TypeError) as context:
          record.requireHost(mcls, 'Plain', 'take')
        self.assertIn("The class body of 'Plain' declares 'take' abstract",
                      str(context.exception))
        self.assertIn("'%s'" % mcls.__name__, str(context.exception))
    with self.assertRaises(TypeError) as context:
      record.__set_name__(int, 'take')
    self.assertIn("The class body of 'int' declares 'take' abstract",
                  str(context.exception))
    self.assertIsNone(abstract.__declaring_class__)
    self.assertIsNone(record.__declaring_class__)
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        take = abstract(self._blank())
    exception = context.exception.__cause__ or context.exception
    self.assertIn("The class body of 'Plain' declares 'take' abstract",
                  str(exception))
    #  What a space hook does for a record of its class body.
    record.__abc_only__ = True
    self.assertIsNone(record.requireHost(Deaf, 'Hosted', 'take'))

    class Hosted(metaclass=Deaf):
      take = record

    self.assertIs(Hosted.__dict__['take'], record)
    self.assertIsNone(Hosted().take())
    self.assertIs(record.__declaring_class__, Hosted)
    self.assertIs(abstract(self._blank()).__abc_only__, False)
