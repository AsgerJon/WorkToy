"""
TestArgsCount tests 'argsCount' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import argsCount, ExceptionInfo
from worktoy.work_test.samplers import IntSampler
from . import UtilitiesTest


class TestArgsCount(UtilitiesTest):
  """
  'argsCount' answers how many arguments a callable takes by position,
  which is what an overload needs to know of a function before it can
  match a call to it. The count includes positional-only and
  positional-or-keyword parameters, leaves out keyword-only ones and
  the two variadics, and counts 'self' of a bound method, since the
  method is unwrapped before it is read.
  """

  def test_docstring_example(self) -> None:
    self.assertEqual(argsCount(lambda a, b, *args, c=0: None), 2)

  def test_positional_only_counted(self) -> None:
    #  The builtins declare positional-only parameters on every Python
    #  the library supports, where the '/' syntax does not.
    self.assertEqual(argsCount(len), 1)
    self.assertEqual(argsCount(divmod), 2)

  def test_keyword_only_ignored(self) -> None:
    self.assertEqual(argsCount(lambda a, *, b, c=0: None), 1)

  def test_variadics_ignored(self) -> None:
    self.assertEqual(argsCount(lambda a, b, *args, **kwargs: None), 2)
    self.assertEqual(argsCount(lambda *args, **kwargs: None), 0)

  def test_no_parameters(self) -> None:
    self.assertEqual(argsCount(lambda: None), 0)

  def test_bound_method_counts_self(self) -> None:
    self.assertEqual(argsCount(self.test_no_parameters), 1)
    self.assertEqual(argsCount(self.assertEqual), 4)

  def test_unbound_function_of_class(self) -> None:
    self.assertEqual(argsCount(TestArgsCount.test_no_parameters), 1)

  def test_class_counts_init_without_self(self) -> None:
    self.assertEqual(argsCount(ExceptionInfo), 1)

  def test_random_lambda_lengths(self) -> None:
    lambdas = (
      lambda: None,
      lambda a: None,
      lambda a, b: None,
      lambda a, b, c: None,
      lambda a, b, c, d: None,
      lambda a, b, c, d, e: None,
    )
    self.randomInteger = IntSampler(0, 5, seed=11, size=8)
    for n in self.randomInteger.row:
      with self.subTest(n=n):
        self.assertEqual(argsCount(lambdas[n]), n)
