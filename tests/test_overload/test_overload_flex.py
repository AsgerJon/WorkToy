"""
TestOverloadFlex subclasses 'OverloadTest' and provides tests for the
'overload.flex' method on the 'overload' class in the 'worktoy.dispatch'
package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tests.test_overload import OverloadTest
from tests.test_utilities import Diagnostic, \
  DiagnosticSpace, \
  DiagnosticMetaclass
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  pass


class _Foo(BaseObject):
  """Three-attribute test class exercising flex permutation across
  arities, both at construction time and via an overloaded instance
  method."""

  name = AttriBox[str]()
  num = AttriBox[int]()
  ratio = AttriBox[float]()

  @overload(int)
  def __init__(self, z: int) -> None:
    self.name, self.num = 'Harry', z

  @overload.flex(str, int)
  def __init__(self, *args) -> None:
    self.name, self.num = args

  @overload.flex(str, int, float)
  def __init__(self, *args) -> None:
    self.name, self.num, self.ratio = args

  @overload(str)
  def update(self, name: str) -> None:
    self.name = name

  @overload(int)
  def update(self, num: int) -> None:
    self.num = num

  @overload(float)
  def update(self, ratio: float) -> None:
    self.ratio = ratio

  @overload.flex(str, int)
  def update(self, *args) -> None:
    self.name, self.num = args

  @overload.flex(str, int, float)
  def update(self, *args) -> None:
    self.name, self.num, self.ratio = args


class TestOverloadFlex(OverloadTest):
  """
  TestOverloadFlex subclasses 'AttriBox' and provides tests for the
  'overload.flex' method on the 'overload' class in the 'worktoy.dispatch'
  package.
  """

  #  ________________________________________________________________
  #  Canonical order - no permutation required
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_canonical_order(self) -> None:
    """Args already in declared (str, int) order pass straight through."""
    foo = _Foo('Tom', 69)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)

  #  ________________________________________________________________
  #  Reversed order - the regression case
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_reversed_order_is_permuted(self) -> None:
    """(int, str) is permuted to (str, int) before the body sees it.

    Regression test: 'PermuterMethod.invoke' previously forwarded *args
    verbatim without calling 'self.route(*args)', causing the AttriBox
    on 'num' to receive the str and raise."""
    foo = _Foo(420, 'Dick')
    self.assertEqual(foo.name, 'Dick')
    self.assertEqual(foo.num, 420)

  def test_reversed_order_distinct_values(self) -> None:
    """Sanity: name and num are not coincidentally equal - confirms the
    permutation actually swapped, rather than both attrs receiving the
    same arg."""
    foo = _Foo(1337, 'Harry')
    self.assertNotEqual(foo.name, foo.num)
    self.assertEqual(foo.name, 'Harry')
    self.assertEqual(foo.num, 1337)

  #  ________________________________________________________________
  #  Non-flex branch unaffected
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_int_only_overload(self) -> None:
    """Single-int call routes to the plain @overload branch, not flex."""
    foo = _Foo(69)
    self.assertEqual(foo.name, 'Harry')
    self.assertEqual(foo.num, 69)

  #  ________________________________________________________________
  #  Three-arg flex - permutation across str/int/float
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_three_arg_canonical(self) -> None:
    """(str, int, float) - no permutation needed."""
    foo = _Foo('Tom', 69, 0.5)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.5)

  def test_three_arg_fully_reversed(self) -> None:
    """(float, int, str) - every position wrong."""
    foo = _Foo(0.5, 69, 'Tom')
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.5)

  def test_three_arg_int_str_float(self) -> None:
    """(int, str, float) - only the first two positions swapped."""
    foo = _Foo(69, 'Tom', 0.5)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.5)

  def test_three_arg_float_str_int(self) -> None:
    """(float, str, int) - non-trivial three-cycle."""
    foo = _Foo(0.5, 'Tom', 69)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.5)

  #  ________________________________________________________________
  #  Overloaded instance method - single-arg dispatch
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_update_str_only(self) -> None:
    """Single-arg str overload touches only 'name'."""
    foo = _Foo('Tom', 69)
    foo.update('Dick')
    self.assertEqual(foo.name, 'Dick')
    self.assertEqual(foo.num, 69)

  def test_update_int_only(self) -> None:
    """Single-arg int overload touches only 'num'."""
    foo = _Foo('Tom', 69)
    foo.update(420)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 420)

  def test_update_float_only(self) -> None:
    """Single-arg float overload touches only 'ratio'."""
    foo = _Foo('Tom', 69, 0.1)
    foo.update(0.9)
    self.assertEqual(foo.name, 'Tom')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.9)

  #  ________________________________________________________________
  #  Overloaded instance method - flex permutation
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_update_two_arg_permuted(self) -> None:
    """Bound-method flex regression: (int, str) must be permuted before
    the body sees it. This is the exact path that broke before
    'PermuterMethod.invoke' was taught to call 'self.route(*args)'."""
    foo = _Foo('Tom', 69)
    foo.update(1337, 'Harry')
    self.assertEqual(foo.name, 'Harry')
    self.assertEqual(foo.num, 1337)

  def test_update_three_arg_permuted(self) -> None:
    """Three-arg flex through the bound-method path."""
    foo = _Foo('Tom', 69, 0.1)
    foo.update(0.9, 1337, 'Harry')
    self.assertEqual(foo.name, 'Harry')
    self.assertEqual(foo.num, 1337)
    self.assertAlmostEqual(foo.ratio, 0.9)

  def test_update_preserves_untouched_attrs(self) -> None:
    """Single-arg update must not clobber attributes outside its
    signature - guards against an over-eager body or a bound-instance
    leak into the args tuple."""
    foo = _Foo('Tom', 69, 0.5)
    foo.update('Dick')
    self.assertEqual(foo.num, 69)
    self.assertAlmostEqual(foo.ratio, 0.5)

  #  ________________________________________________________________
  #  Inspection of __str__
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_str(self, ) -> None:
    """
    This method creates a diagnosing 'AbstractSpaceHook' subclass.
    """

    diagnostics = Diagnostic()
    self.assertIsNone(diagnostics.method())
    self.assertIsNone(diagnostics.method(69))
    self.assertIsNone(diagnostics.method('69', 420))
    self.assertIsNone(diagnostics.method(1337, '80085'))

    dispatchSignatures = str.split(
      str(Diagnostic.__dict__['method']), os.linesep,
    )[1:]
    self.assertTrue(Diagnostic.testing)
    self.assertTrue(Diagnostic.__namespace__['testing'])
    for diagnostic in Diagnostic.overloadDiagnostics:
      for line in str.split(str(diagnostic), os.linesep)[1:]:
        self.assertIn(line, dispatchSignatures)

    class Sus(metaclass=DiagnosticMetaclass):
      pass

    space: DiagnosticSpace = getattr(Sus, '__namespace__')
    object.__setattr__(space, '__overload_diagnostics__', None)
    with self.assertRaises(RecursionError):
      _ = space._getOverloadDiagnostics(_recursion=True)
