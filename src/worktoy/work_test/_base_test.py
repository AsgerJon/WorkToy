"""
BaseTest subclasses unittest.TestCase to provide a base class shared by
testclasses across the 'tests' package. It implements module unloading in
the 'tearDownClass' method and adds 'assertIsSubclass' (and negation).
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import gc
from unittest import TestCase
from typing import TYPE_CHECKING

from .samplers import FloatSampler, IntSampler, GaussianSampler
from .samplers import SymbolicSampler, WordSampler, LoremSampler
from ..desc import Field, SymbolicName
from ..lorem_ipsum import StochasticWord, Sentence

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator, Optional, Union

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]

  StrTuple: TypeAlias = tuple[str, ...]
  MaybeStrTuple: TypeAlias = Optional[StrTuple]
  StrTupleField: TypeAlias = Union[StrTuple, Field]

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
      """Assert that 'subClass' is a subclass of 'superClass'."""
      self.assertTrue(issubclass(cls, base))

    def assertNotIsSubclass(self, cls: type, base: type, msg=None) -> None:
      """Assert that 'subClass' is not a subclass of 'superClass'."""
      self.assertFalse(issubclass(cls, base))
else:  # version >= 3.14
  _Temp = TestCase


class BaseTest(_Temp):
  """
  BaseTest provides a base class shared by the testing classes in the
  tests package. It implements module unloading in the 'tearDownClass'
  method and adds 'assertIsNotInstance' and 'assertIsNotSubclass'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __min_keys__: StrTuple = 'minVal', 'min', 'minimum', 'min_value', 'minval'
  __max_keys__: StrTuple = 'maxVal', 'max', 'maximum', 'max_value', 'maxval'
  __key_groups__: dict[str, StrTuple] = dict(
    minVal=__min_keys__,
    maxVal=__max_keys__,
    )

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  randomInteger = IntSampler()
  randomFloat = FloatSampler()
  randomGaussian = GaussianSampler()
  randomSymbolicName = SymbolicSampler()
  randomWord = WordSampler()
  randomLorem = LoremSampler()

  #  Virtual Variables
  attrErrTrace = Field()
  exceptions = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @attrErrTrace.GET
  def _getAttributeErrorTrace(self, ) -> str:
    return """object has no attribute"""

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
    After the super call, this method creates the stochastic word
    generator to the class.
    """
    super().setUpClass()
    cls.stochWord = StochasticWord()
    cls.loremSentence = Sentence()

  @classmethod
  def tearDownClass(cls) -> None:
    """
    This method deletes temporary files used by this class. It unloads the
    module and runs the garbage collector to ensure that all references to
    the module are removed to prevent metaclass leakage trolling in
    particular.
    """
    super().tearDownClass()
    sys.modules.pop(cls.__module__, None)
    gc.collect()

  assertIsNotSubclass = _Temp.assertNotIsSubclass
  assertIsNotInstance = _Temp.assertNotIsInstance
