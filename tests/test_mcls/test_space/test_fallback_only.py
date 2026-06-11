"""
TestFallbackOnly pins the behaviour of a name whose only registration in
the class body is an 'overload.fallback' declaration. The overload
machinery claims such a declaration out of the namespace during class
creation, so the class must receive a dispatcher under that name or the
method vanishes from the class entirely: the constructor below would
otherwise be discarded without any error, leaving instances built by the
permissive default constructor instead.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from .. import MCLSTest


class FallbackInit(BaseObject):
  """FallbackInit declares its constructor only as an overload fallback,
  with no concrete signatures alongside it."""

  @overload.fallback
  def __init__(self, *args) -> None:
    self.values = args


class FallbackMethod(BaseObject):
  """FallbackMethod declares a named method only as an overload
  fallback, with no concrete signatures alongside it."""

  @overload.fallback
  def compute(self, *args) -> tuple:
    return args


class TestFallbackOnly(MCLSTest):
  """
  TestFallbackOnly provides tests for classes registering a method only
  as an overload fallback. The fallback must receive every call, since
  no concrete signature exists to dispatch to.
  """

  def test_fallback_init_runs(self) -> None:
    """
    Testing that a constructor declared only as a fallback still runs
    on instantiation.
    """
    obj = FallbackInit(69, 420)
    self.assertEqual(obj.values, (69, 420))

  def test_fallback_method_present(self) -> None:
    """
    Testing that a named method declared only as a fallback exists on
    the class rather than being silently dropped.
    """
    self.assertTrue(hasattr(FallbackMethod, 'compute'))

  def test_fallback_method_runs(self) -> None:
    """
    Testing that a named method declared only as a fallback receives
    calls and returns its result.
    """
    obj = FallbackMethod()
    self.assertEqual(obj.compute(1, 2, 3), (1, 2, 3))
