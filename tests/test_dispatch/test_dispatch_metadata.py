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


class Flexible(BaseObject):
  """Flexible declares a method flexibly, which registers a wrapper around
  the function, ahead of a plain declaration of it, and another flexibly
  alone."""

  @overload(str)
  @overload.flex(str, int)
  def f(self, text: str, size: int = 12) -> str:
    """Labels."""
    return '%s:%d' % (text, size)

  @overload.flex(int, float)
  def g(self, a: int, b: float) -> float:
    """Scales."""
    return a * b


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

  def test_flexible_declaration(self) -> None:
    """A flexible declaration registers a wrapper around the function,
    and the dispatch is documented by the function, not by the class of
    the wrapper, whether the flexible declaration comes first in a stack
    or stands alone; the wrapper still restores the argument order."""
    self.assertEqual(Flexible.f.__doc__, 'Labels.')
    self.assertEqual(Flexible.g.__doc__, 'Scales.')
    self.assertEqual(Flexible().f.__doc__, 'Labels.')
    self.assertEqual(Flexible.f.__module__, Flexible.__module__)
    self.assertEqual(Flexible.g.__qualname__, 'Flexible.g')
    flexible = Flexible()
    self.assertEqual(flexible.f('x'), 'x:12')
    self.assertEqual(flexible.f('x', 3), 'x:3')
    self.assertEqual(flexible.f(3, 'x'), 'x:3')
    self.assertEqual(flexible.g(2, 1.5), 3.0)
    self.assertEqual(flexible.g(1.5, 2), 3.0)
