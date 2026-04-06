"""
TestSymbolicSampler subclasses 'BaseTest' and provides tests for the
'SymbolicSampler' class from the 'worktoy.work_test.samplers' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.work_test.samplers import SymbolicSampler
from . import SamplerTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSymbolicSampler(SamplerTest):
  """
  TestSymbolicSampler subclasses 'BaseTest' and provides tests for the
  'SymbolicSampler' class from the 'worktoy.work_test.samplers' package.
  """

  def test_init(self, ) -> None:
    """
    This method tests the constructor overloads of the 'SymbolicSampler'
    class:

    @overload(int)
    def __init__(self, wordCount: int, **kwargs) -> None:

    @overload()
    def __init__(self, **kwargs) -> None:
    """

    intSampler = SymbolicSampler(4)
    self.assertEqual(intSampler.wordCount, 4)
    kwargSampler = SymbolicSampler(wordCount=5)
    self.assertEqual(kwargSampler.wordCount, 5)
    intKwargSampler = SymbolicSampler(6, lmao=True)
    self.assertEqual(intKwargSampler.wordCount, 6)
    defaultSampler = SymbolicSampler()
    expectedCount = SymbolicSampler.__fallback_count__
    self.assertEqual(defaultSampler.wordCount, expectedCount)

  def test_coverage(self, ) -> None:
    """
    This method covers the legacy creator function pattern currently
    obsolete because the generalized fallback constructor provided by
    'BaseSampler'.
    In the legacy getter pattern, the getter looks for a value at a
    specific private variable. If 'None', the getter will raise
    'RecursionError' if called with keyword argument '_recursion' set to
    'True'. This both prevents infinite recursion *and* allows inspection
    of the presence the private variable. By default, no 'RecursionError'
    is raised. Instead, the getter will call the associated creator
    function and then recursively call itself with '_recursion' set to
    'True'.
    The generalized fallback constructor currently implemented by
    'BaseSampler' prevents certain branches in the legacy pattern
    described above. This is because the fallback constructor automatically
    sets the private variable to the fallback value during handling of
    keyword arguments.
    As of writing, both patterns are being considered so both remain in
    the codebase, necessitating the coverage gymnastics provided by this
    method.
    """

    class FooSampler(SymbolicSampler):
      """
      By reimplementing the keyword argument constructor overload,
      the generalized fallback pattern is disabled, allowing coverage of
      the legacy pattern.
      """

      @overload()
      def __init__(self, **kwargs) -> None:
        pass

    fooSampler = FooSampler()
    expectedCount = FooSampler.__fallback_count__
    self.assertEqual(fooSampler.wordCount, expectedCount)
