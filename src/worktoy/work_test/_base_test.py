"""
BaseTest is the 'unittest.TestCase' subclass shared by the worktoy tests.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import gc
from unittest import TestCase
from typing import TYPE_CHECKING

from . import SubTest
from .samplers import FloatSampler, IntSampler, GaussianSampler
from .samplers import SymbolicSampler, WordSampler, LoremSampler
from ..desc import Field, SymbolicName
from ..lorem_ipsum import StochasticWord, Sentence
from ..mcls import BaseMeta
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator, Optional

  MaybeStr: TypeAlias = Optional[str]

  StrTuple: TypeAlias = tuple[str, ...]
  MaybeStrTuple: TypeAlias = Optional[StrTuple]

  IntTuple: TypeAlias = tuple[int, ...]
  IntTuples: TypeAlias = tuple[IntTuple, ...]

  TypicalExceptions: TypeAlias = Iterator[type[Exception]]
  ExcType: TypeAlias = type[BaseException]
  SymbolicNames: TypeAlias = tuple[SymbolicName, ...]

#  So Python 3.14 saw 'assertIsSubclass' and 'assertNotIsSubclass' added to
#  'unittest.TestCase', but since we support back to 3.7, but also up to
#  3.14, we need the following 'try-except-else':

try:
  _ = TestCase.assertIsSubclass
except AttributeError:  # pragma: no cover
  class _Temp(TestCase):
    def assertIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Asserts that 'cls' is a subclass of 'base'."""
      self.assertTrue(issubclass(cls, base))

    def assertNotIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Asserts that 'cls' is not a subclass of 'base'."""
      self.assertFalse(issubclass(cls, base))
else:  # version >= 3.14
  _Temp = TestCase


class BaseTest(_Temp, metaclass=BaseMeta):
  """
  BaseTest provides a base class shared by the testing classes in the
  tests package. It implements module unloading in the 'tearDownClass'
  method and adds 'assertIsNotInstance' and 'assertIsNotSubclass'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __fallback_line_length__: int = 48
  __fallback_new_line__: str = os.linesep

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  randomInteger = IntSampler()
  randomFloat = FloatSampler()
  randomGaussian = GaussianSampler()
  randomSymbolicName = SymbolicSampler()
  randomWord = WordSampler()
  randomLorem = LoremSampler()
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

  @classmethod
  def setUpClass(cls) -> None:
    """
    The 'setUpClass' method runs the super call, then attaches a shared
    'StochasticWord' and 'Sentence' to the class for the test methods to
    draw on.
    """
    super().setUpClass()
    cls.stochWord = StochasticWord()
    cls.loremSentence = Sentence()

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

  assertIsNotSubclass = _Temp.assertNotIsSubclass
  assertIsNotInstance = _Temp.assertNotIsInstance

  @classmethod
  def argReport(cls, *args, **kwargs) -> str:
    """
    The 'argReport' method builds a string report of the given arguments,
    used in the test cases to provide informative error messages when a
    test fails. The report includes the type and a truncated string
    representation of each argument. A representation longer than 48
    characters is truncated to 45 characters followed by an ellipsis.
    """
    lineLength: int = kwargs.get('chars', cls.__fallback_line_length__)
    newLine: str = kwargs.get('newLine', cls.__fallback_new_line__)
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

  def tearDown(self, ) -> None:
    """
    The 'tearDown' method runs the super call, then peeks at any sub-test
    recorded on this instance through the 'subTest' descriptor and fails
    the test if that sub-test holds any fails or errors.
    """
    super().tearDown()
    cls = type(self)
    try:
      sub = cls.subTest.__get__(self, cls, _recursion=True)
    except RecursionError:
      return
    if not (sub.fails or sub.errors):
      return
    lines = []
    for fail in sub.fails:
      lines.append('FAIL: %s' % fail)
    for error in sub.errors:
      lines.append('ERROR: %r' % error)
    self.fail(str.join('\n', lines))
