"""
BaseTest is the 'unittest.TestCase' subclass shared by the worktoy tests.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import traceback
from functools import wraps
from inspect import iscoroutinefunction
from types import FunctionType
from unittest import TestCase
from typing import TYPE_CHECKING

from . import SubTest
from .samplers import FloatSampler, IntSampler, GaussianSampler
from .samplers import SymbolicSampler, WordSampler, LoremSampler
from ..desc import Field, AttriBox
from ..mcls import BaseMeta
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, TypeAlias, Iterator

  TypicalExceptions: TypeAlias = Iterator[type[Exception]]

#  Python 3.14 added 'assertIsSubclass' and 'assertNotIsSubclass' to
#  'unittest.TestCase'; the versions back to 3.7 get them from the shim.

try:
  _ = TestCase.assertIsSubclass
except AttributeError:  # pragma: no cover, no mutate
  class _Temp(TestCase):
    def assertIsSubclass(self, cls: type, base: type, msg=None) -> None:
      self.assertTrue(issubclass(cls, base), msg)

    def assertNotIsSubclass(self, cls: type, base: type, msg=None) -> None:
      self.assertFalse(issubclass(cls, base), msg)
else:  # version >= 3.14
  _Temp = TestCase


def _reportingCleanups(own: Callable) -> Callable:
  """
  The report of the failed 'subTest' blocks of a test runs among the
  cleanups of the test. A test class may write a 'doCleanups' of its
  own, as 'unittest' allows, and need not hand on from it; the report
  must run all the same.

  Implementation
  --------------

  The returned 'doCleanups' calls 'own' and then 'TestCase.doCleanups',
  which runs what 'own' left on the list of cleanups: all of it when
  'own' did not hand on, nothing when it did. Then it registers
  'BaseTest._reportSubTests' as a cleanup and runs the list once more,
  so the report comes after every cleanup of the test, a block that
  failed inside one included. What the report raises is collected as a
  failure of the test, where an exception raised in 'doCleanups' itself
  would leave 'TestCase.run'. 'addCleanup' and 'doCleanups' are called
  on 'TestCase', past any override of the test class. The function is
  marked '__reports__', so 'BaseTest.__class_init__' builds no second
  one around it.

  Parameters
  ----------

  own : Callable
    Called as '(self)': the 'doCleanups' the test class would use
    otherwise, its own or the one of 'unittest'.

  Returns
  -------

  Callable
    Called as '(self)': the 'doCleanups' the test class is given.
  """

  def doCleanups(self: Any) -> bool:
    own(self)
    TestCase.doCleanups(self)
    TestCase.addCleanup(self, self._reportSubTests)
    return TestCase.doCleanups(self)

  doCleanups.__reports__ = True
  return doCleanups


def _reportingDebug(own: Callable) -> Callable:
  """
  'debug' runs a test with no result to collect into, so the report of
  the failed 'subTest' blocks must be raised by 'debug' itself, after
  the test, whether the test class wrote a 'debug' of its own or not.

  Implementation
  --------------

  The returned 'debug' calls 'own' and then 'BaseTest._reportSubTests'.
  What the test itself raises leaves 'own' first, as 'debug' is for.
  The function is marked '__reports__', as the 'doCleanups' of
  '_reportingCleanups' is.

  Parameters
  ----------

  own : Callable
    Called as '(self)': the 'debug' the test class would use otherwise,
    its own or the one of 'unittest'.

  Returns
  -------

  Callable
    Called as '(self)': the 'debug' the test class is given.
  """

  def debug(self: Any) -> None:
    own(self)
    self._reportSubTests()

  debug.__reports__ = True
  return debug


def _reportingTest(own: Callable) -> Callable:
  """
  The failed 'subTest' blocks of a test method are best reported by the
  test method itself, as it ends. The report then hangs on nothing the
  test class may replace, not 'doCleanups' and not 'run', and it comes
  as well when the test method is called by hand.

  Implementation
  --------------

  The returned function calls 'own', then 'BaseTest._reportSubTests',
  and returns what 'own' returned. What 'own' raises leaves it first, a
  skip included; the blocks recorded before are then left to the report
  among the cleanups. 'functools.wraps' gives the function the name, the
  docstring and the attributes of 'own', the marks of 'unittest.skip'
  and 'unittest.expectedFailure' among them, so a failed block of a test
  marked as an expected failure is that failure. The function is marked
  '__reports__'.

  Parameters
  ----------

  own : Callable
    Called as '(self)': a test method as the class body wrote it.

  Returns
  -------

  Callable
    Called as '(self)': the test method the class is given.
  """

  @wraps(own)
  def test(self: Any, *args, **kwargs) -> Any:
    out = own(self, *args, **kwargs)
    self._reportSubTests()
    return out

  test.__reports__ = True
  return test


class BaseTest(_Temp, metaclass=BaseMeta):
  """
  Every test of the suite wants the same things ready: random data of
  the usual kinds that belongs to that test alone, a sub-test block that
  runs every target and reports each failure with its label and line,
  the subclass assertions on every Python the library supports, a
  report of its arguments for a message, and a class body with the
  checks of a worktoy class. 'BaseTest' is the base every test class of
  the suite is based on, directly or through a local base, and the base
  a project's tests use for the same reasons.

    class TestDice(BaseTest):

      def setUp(self) -> None:
        self.randomInteger = IntSampler(1, 6, seed=7)

      def test_faces(self) -> None:
        for face in self.randomInteger.row:
          with self.subTest(face=face):
            self.assertIn(face, range(1, 7))

  Implementation
  --------------

  'BaseTest' is a 'unittest.TestCase' built by 'BaseMeta', so a test
  body runs through the namespace of a worktoy class, and a test base
  may bring a metaclass of its own based on 'BaseMeta'. The six samplers,
  'randomInteger' and the rest, are 'AttriBox'es, so 'unittest' building
  one instance of a test class per test method gives each test samplers
  of its own, built at the first read, and a sampler narrowed or seeded
  in 'setUp' keeps its settings for that test alone; 'seedSamplers'
  seeds all six with one seed. 'subTest' is the 'SubTest' descriptor,
  which builds one accumulator per test instance; '_reportSubTests'
  reads it without building one and fails the test once, with
  'FAIL [label]: message' or 'ERROR [label]: repr' per recorded block,
  each followed by the traceback of what the block raised.
  '__class_init__' gives every test class test methods that run it as
  they end, and a 'doCleanups' and a 'debug' that run it for what a
  'tearDown' or a cleanup recorded, so a 'tearDown', a 'doCleanups', a
  'debug' or a 'run' of a test class need not hand on for it.
  'exceptions' yields the common builtin exception classes. 'argReport'
  puts each argument on a line of its own as '<type: value>'.
  'assertIsNotSubclass' and 'assertIsNotInstance' are the negative
  assertions under the names the suite uses; below Python 3.14 the
  subclass pair comes from the shim above the class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __fallback_line_length__: int = 48
  __fallback_new_line__: str = os.linesep

  #  Public Variables
  randomInteger = AttriBox[IntSampler]()
  randomFloat = AttriBox[FloatSampler]()
  randomGaussian = AttriBox[GaussianSampler]()
  randomSymbolicName = AttriBox[SymbolicSampler]()
  randomWord = AttriBox[WordSampler]()
  randomLorem = AttriBox[LoremSampler]()
  subTest = SubTest()

  #  Virtual Variables
  exceptions = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @exceptions.GET
  def _getTypicalExceptions(self, ) -> TypicalExceptions:
    yield from (
        ValueError,
        KeyError,
        IndexError,
        RuntimeError,
        OSError,
        PermissionError,
        TypeError,
        FileExistsError,
        FileNotFoundError,
    )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  assertIsNotSubclass = _Temp.assertNotIsSubclass
  assertIsNotInstance = _Temp.assertNotIsInstance

  @classmethod
  def argReport(cls, *args, **kwargs) -> str:
    """
    A failing assertion on several values is read best with each value
    on a line of its own, named by its type and short enough to take in
    at a glance, and a test should not have to build such a message by
    hand.

    Implementation
    --------------

    Each positional argument becomes '<type: value>', the value as 'str'
    gives it. A line as long as the limit or longer is cut to three
    characters fewer and closed with an ellipsis, so it is as long as
    the limit. The lines are joined by the line separator, each after
    the first indented by two spaces. The text passes through 'textFmt',
    so a run of whitespace inside a value shows as one space, and a
    '<br>' or a '<tab>' in a value is expanded.

    Parameters
    ----------

    *args
      The values to report.

    **kwargs
      chars : int, optional
        The limit of a line. Defaults to 48.
      newLine : str, optional
        The line separator. Defaults to 'os.linesep'.

    Returns
    -------

    str
      The report, empty when no argument is given.
    """
    if 'chars' in kwargs:
      lineLength: int = kwargs['chars']
    else:
      lineLength: int = cls.__fallback_line_length__
    if 'newLine' in kwargs:
      newLine: str = kwargs['newLine']
    else:
      newLine: str = cls.__fallback_new_line__
    argTypes = (*(type(arg).__name__ for arg in args),)
    argStr = (*(arg if isinstance(arg, str) else str(arg) for arg in args),)
    argSpec = """<%s: %s>"""
    argInfo = []
    for type_, info in zip(argTypes, argStr):
      argInfo.append(argSpec % (type_, info))
    argLines = []
    for line in argInfo:
      if len(line) < lineLength:
        argLines.append(line)
      else:
        argLines.append('%s...' % line[:lineLength - 3])
    argStr = '<br><tab>'.join(argLines)
    return textFmt(argStr, newLineSymbol=newLine)

  def seedSamplers(self, seed: int) -> None:
    """
    A test drawing random data must be able to draw the same data again,
    at the next run and on another machine, or a failure seen once
    cannot be looked at twice. The test has six samplers, and one line
    should seed them all.

    Implementation
    --------------

    The seed is assigned to 'seed' of each of the six samplers,
    'randomInteger' first, which seeds the generator of that sampler. A
    test calling the method in its 'setUp' repeats its draws at every
    run.

    Parameters
    ----------

    seed : int
      The seed every sampler receives.

    Raises
    ------

    TypeException
      'seed' is no 'int'. The first sampler refuses it, so none is
      seeded.
    """
    samplers = (
        self.randomInteger,
        self.randomFloat,
        self.randomGaussian,
        self.randomSymbolicName,
        self.randomWord,
        self.randomLorem,
    )
    for sampler in samplers:
      sampler.seed = seed

  @staticmethod
  def _formatRaised(exception: BaseException) -> str:
    """
    A failed block is caught where it happens, and its report must still
    name the line that raised, as the traceback of an uncaught exception
    does.

    Implementation
    --------------

    'traceback.format_exception' renders the exception with the
    traceback it carries, and the trailing whitespace is dropped.

    Parameters
    ----------

    exception : BaseException
      What a block raised.

    Returns
    -------

    str
      The traceback as the interpreter prints it.
    """
    lines = traceback.format_exception(
        type(exception), exception, exception.__traceback__,
    )
    return str.join('', lines).rstrip()

  @classmethod
  def __class_init__(cls, name: str, bases: tuple, space, **kw) -> None:
    """
    The report of the failed 'subTest' blocks must run for every test
    class, whatever metaclass builds it and whatever the class does with
    'tearDown', 'doCleanups' or 'debug'. A metaclass of 'BaseTest' could
    see to that only for the classes it builds itself, and a test base
    with a metaclass of its own, based on 'BaseMeta', could then not be
    built at all.

    Implementation
    --------------

    'AbstractMetaclass.__init__' calls this hook for 'BaseTest' and for
    every class based on it, under 'BaseMeta' and under any metaclass
    based on 'BaseMeta'. For 'doCleanups' and for 'debug', the hook
    takes what the class resolves the name to. Unless that is marked
    '__reports__' already, as it is when a test class inherits it from
    another, the class is given the method that '_reportingCleanups' or
    '_reportingDebug' builds around it. That covers a method written in
    the class body and one of a mixin listed ahead of 'BaseTest'.

    Every test method is given the report as well: a plain function at
    a name beginning with 'test', as 'unittest' names a test method,
    held by the nearest class along the resolution order holding the
    name, is replaced on the class by what '_reportingTest' builds
    around it. A coroutine function is left as it is, since calling it
    runs nothing yet, and so is a classmethod or a staticmethod. A test
    method reporting as it ends hangs on neither 'doCleanups' nor 'run',
    so one of those replaced on a class later, or written without
    handing on, loses no report of a block in a test method. A test
    base that writes a '__class_init__' of its own hands on to this
    one.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : tuple
      The bases of the class.

    space : BaseSpace
      The namespace the class body ran in.

    **kw
      The class keywords.
    """
    builders = (
      ('doCleanups', _reportingCleanups),
      ('debug', _reportingDebug),
    )
    for key, builder in builders:
      own = type.__getattribute__(cls, key)
      if not getattr(own, '__reports__', False):
        type.__setattr__(cls, key, builder(own))
    seen = []
    for base in cls.__mro__:
      for key, own in (*vars(base).items(),):
        if key in seen or not key.startswith('test'):
          continue
        seen.append(key)
        if not isinstance(own, FunctionType):
          continue
        if getattr(own, '__reports__', False) or iscoroutinefunction(own):
          continue
        type.__setattr__(cls, key, _reportingTest(own))

  def _reportSubTests(self, ) -> None:
    """
    A failed 'subTest' block is swallowed where it happens, so that the
    rest of the test runs, and the test must still fail for it
    afterwards. One failure must carry every block recorded since the
    last report, and tell of each what is needed to find it: its label,
    what it raised and the line that raised it. A test that recorded
    nothing, or never opened a block, must pass through untouched. And
    since the report is asked for at more than one moment of a test,
    nothing may be reported twice.

    Implementation
    --------------

    The accumulator is read through the 'subTest' descriptor in the way
    that builds none, and a test without one returns at once, as does
    one whose accumulator holds no fail and no error. Otherwise the
    message gets 'FAIL [label]: message' for each fail and
    'ERROR [label]: repr' for each error, each followed by its traceback
    from '_formatRaised'; the accumulator is removed from the instance,
    and 'fail' raises the message. Every test method a test class is
    given calls this method as it ends, the 'doCleanups' it is given
    runs it after the cleanups of the test, and the 'debug' it is given
    calls it at its end; '__class_init__' gives the class the three.

    Raises
    ------

    AssertionError
      A block failed or raised since the last report. The exception is
      the 'failureException' of the test.
    """
    cls = type(self)
    try:
      sub = cls.subTest.__get__(self, cls, _recursion=True)
    except RecursionError:
      return
    if not (sub.fails or sub.errors):
      return
    lines = []
    for label, fail in zip(sub.failLabels, sub.fails):
      lines.append('FAIL [%s]: %s' % (label, fail))
      lines.append(self._formatRaised(fail))
    for label, error in zip(sub.errorLabels, sub.errors):
      lines.append('ERROR [%s]: %r' % (label, error))
      lines.append(self._formatRaised(error))
    delattr(self, cls.subTest.__private_name__)
    self.fail(str.join('\n', lines))
