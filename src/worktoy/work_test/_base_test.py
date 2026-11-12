"""
BaseTest is the 'unittest.TestCase' subclass shared by the worktoy tests.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import gc
import os
import sys
import traceback
from unittest import TestCase
from typing import TYPE_CHECKING

from . import SubTest, TestMeta
from .samplers import FloatSampler, IntSampler, GaussianSampler
from .samplers import SymbolicSampler, WordSampler, LoremSampler
from ..desc import Field, AttriBox
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Iterator

  TypicalExceptions: TypeAlias = Iterator[type[Exception]]

#  Python 3.14 added 'assertIsSubclass' and 'assertNotIsSubclass' to
#  'unittest.TestCase'; the versions back to 3.7 get them from the shim.

try:
  _ = TestCase.assertIsSubclass
except AttributeError:  # pragma: no cover, no mutate
  class _Temp(TestCase):
    def assertIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Asserts that 'cls' is a subclass of 'base'."""
      self.assertTrue(issubclass(cls, base), msg)

    def assertNotIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Asserts that 'cls' is not a subclass of 'base'."""
      self.assertFalse(issubclass(cls, base), msg)
else:  # version >= 3.14
  _Temp = TestCase


class BaseTest(_Temp, metaclass=TestMeta):
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

  'BaseTest' is a 'unittest.TestCase' built by 'TestMeta', which is a
  'BaseMeta', so a test body runs through the namespace of a worktoy
  class. The six samplers,
  'randomInteger' and the rest, are 'AttriBox'es, so 'unittest' building
  one instance of a test class per test method gives each test samplers
  of its own, built at the first read, and a sampler narrowed or seeded
  in 'setUp' keeps its settings for that test alone; 'seedSamplers'
  seeds all six with one seed. 'subTest' is the
  'SubTest' descriptor, which builds one accumulator per test instance;
  '_reportSubTests' reads it without building one and fails the test
  once, with 'FAIL [label]: message' or 'ERROR [label]: repr' per
  recorded block, each followed by the traceback of what the block
  raised. 'TestMeta' has it run among the cleanups of every test and at
  the end of 'debug', so a 'tearDown' of a test class need not hand on
  for it.
  'tearDownClass' unloads the module of the test class and runs the
  garbage collector after its tests, for the reason its docstring
  gives. 'exceptions' yields the common builtin exception classes.
  'argReport'
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
    The 'argReport' method builds a string report of the given arguments,
    used in the test cases to provide informative error messages when a
    test fails. The report puts each argument on a line of its own as
    '<type: value>'. A line of 48 characters or more, a limit the 'chars'
    keyword replaces, is cut to three characters fewer and closed with an
    ellipsis; the 'newLine' keyword replaces the line separator.
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
    The 'seedSamplers' method seeds the six samplers of this test with
    one seed, so a test reruns with the same draws by calling it in its
    'setUp'. A seed that is no 'int' is refused by the first sampler
    with 'TypeException' before any sampler is seeded.
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
    The '_formatRaised' method renders the traceback of a recorded
    exception as the interpreter would, so the report of a sub-test
    block names the line that raised.
    """
    lines = traceback.format_exception(
        type(exception), exception, exception.__traceback__,
    )
    return str.join('', lines).rstrip()

  @classmethod
  def tearDownClass(cls) -> None:
    """
    Unloads the test module and runs the garbage collector to evict
    the class object before the next test class is built.

    This is here because 'unittest' pins every test class it discovers
    for the entire run via 'TestLoader' and 'TestResult', and that
    pinning causes real, observable metaclass context leakage between
    otherwise-independent test classes. Run TestA and TestB in
    isolation: both pass. Run them in sequence: TestB inherits stale
    descriptor state, mismatched owners, or cached registry entries
    that 'unittest' has refused to release. Popping the module from
    sys.modules and forcing a GC pass drops the refcount on the
    outgoing class so its metaclass finalizers actually fire before
    the next class's body executes. The bug only exists in the
    intersection of two innocent tests, which is why this looks
    paranoid until you have spent a weekend debugging it.

    Blame: 'unittest'. The metaclass machinery is fine.
    """
    super().tearDownClass()
    sys.modules.pop(cls.__module__, None)
    gc.collect()

  def _reportSubTests(self, ) -> None:
    """
    The '_reportSubTests' method peeks at any sub-test recorded on this
    instance through the 'subTest' descriptor and fails the test if that
    sub-test holds any fails or errors, naming each with its label and
    the traceback of what it raised. The records it reports are dropped
    from the instance first, so a second call reports nothing twice.
    'TestMeta' registers the method as a cleanup of every test, and
    calls it at the end of 'debug'.
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
