"""
TestDispatchMetadata subclasses 'DispatcherTest' and pins that the
compiled dispatch function a class exposes carries the docstring of the
first registered function and the module of its owner, so 'help' and
the documentation tools see what the author wrote. The function used to
carry only its name and qualified name, so every overloaded method
documented nothing and reported the dispatcher's own file as its module.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import DispatcherTest


class Doc(BaseObject):
  """Doc overloads a documented method and an undocumented one."""

  @overload(int)
  def f(self, a: int) -> int:
    """Doubles."""
    return a * 2

  @overload(str)
  def f(self, a: str) -> str:
    return a

  @overload(ARGS[int])
  def g(self, *a: int) -> int:
    """Sums."""
    return sum(a)

  @overload.fallback
  def h(self, *a) -> None:
    """Catches all."""


class TestDispatchMetadata(DispatcherTest):
  """
  TestDispatchMetadata provides tests for the metadata of a compiled
  dispatch function.
  """

  def test_doc_and_module(self) -> None:
    """The docstring is the first registered function's, the module is
    the owner's, and the names stay."""
    self.assertEqual(Doc.f.__doc__, 'Doubles.')
    self.assertEqual(Doc.f.__module__, Doc.__module__)
    self.assertEqual(Doc.f.__name__, 'f')
    self.assertEqual(Doc.f.__qualname__, 'Doc.f')
    self.assertEqual(Doc().f.__doc__, 'Doubles.')

  def test_variadic_and_fallback_only(self) -> None:
    """With no concrete function, the first variadic one documents the
    dispatch, and failing that the fallback."""
    self.assertEqual(Doc.g.__doc__, 'Sums.')
    self.assertEqual(Doc.h.__doc__, 'Catches all.')
    self.assertEqual(Doc.g.__module__, Doc.__module__)
