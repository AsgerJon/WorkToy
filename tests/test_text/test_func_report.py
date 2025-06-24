"""
TestFuncReport tests the 'funcReport' function from the 'worktoy.text'
module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.static import Dispatch

from typing import TYPE_CHECKING

from worktoy.text import funcReport, monoSpace

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestFuncReport(TestCase):
  """
  TestFuncReport tests the 'funcReport' function from the 'worktoy.text'
  module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_bad_func(self) -> None:
    """
    Testing against function without docstring
    """

    def bad() -> None: pass

    with self.assertRaises(SyntaxError) as context:
      _ = funcReport(bad)
    e = context.exception
    expected = """No docstring found"""
    self.assertIn(expected, str(e))

  def test_bad_func_non_strict(self) -> None:
    """
    Testing against function without docstring, but non-strict mode
    """

    def bad() -> None: pass

    report = funcReport(bad, strict=False)

    self.assertIn('def bad() -> None:', report)

  def test_self_report(self) -> None:
    """
    Passing 'funcReport' itself to 'funcReport'!
    """
    report = funcReport(funcReport)
    title = """def funcReport(func: function, **kwargs) -> str:"""
    self.assertIn(title, report)
    self.assertIn(monoSpace(funcReport.__doc__), monoSpace(report))

  def test_abstract_metaclass_prepare_report(self) -> None:
    """
    Testing against the __prepare__ method of AbstractMetaclass
    """
    func = AbstractMetaclass.__prepare__
    report = funcReport(func)
    self.assertIn('name', report)
    self.assertIn('bases', report)

  def test_verbatim_function(self) -> None:
    """
    Testing ad hoc created functions
    """

    def verbatim(*args, **kwargs) -> None:
      """
      This is a verbatim function.
      """
      pass

    report = funcReport(verbatim)

  def test_no_return_type(self) -> None:
    """
    Testing a function without a return type annotation
    """

    def no_return_type():
      """
      This function has no return type annotation.
      """
      pass

    with self.assertRaises(SyntaxError) as context:
      _ = funcReport(no_return_type)
    e = context.exception
    expected = """No return type hint found"""
    self.assertIn(expected, str(e))

  def test_no_return_type_non_strict(self) -> None:
    """
    Testing a function without a return type annotation, but non-strict mode
    """

    def no_return_type():
      """
      This function has no return type annotation.
      """
      pass

    report = funcReport(no_return_type, strict=False)
    self.assertIn('def no_return_type()', report)
