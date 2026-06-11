"""
TestShadowReads pins the namespace shadow space: a class-body name
claimed by a space hook remains readable later in the same body. The
namespace records every assignment in a shadow mapping and answers
reads from it when the name is absent from the namespace itself.
Without the shadow, reading a claimed name escapes to the module
scope, silently binding whatever global happens to share the name.

The fixtures alias an overloaded method by assigning its name to a
second attribute. Since every 'overload' declaration rebinds the name
to a fresh wrapper carrying only its own signature, the alias copies
every registration accumulated under the source name, not just the
wrapper that happened to be assigned last.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from .. import MCLSTest

#  Module-level decoy sharing its name with the overloaded method
#  below. Without the shadow space, the alias assignments in the class
#  bodies would silently bind this string instead of the overloads.
compute = 'global decoy'

finalizeLog = []


class AliasCalc(BaseObject):
  """AliasCalc overloads 'compute' for 'int' and 'str' and aliases the
  full dispatcher as 'area'."""

  @overload(int)
  def compute(self, value: int) -> int:
    return value + 1

  @overload(str)
  def compute(self, value: str) -> str:
    return str.upper(value)

  area = compute


class AliasFull(BaseObject):
  """AliasFull registers a concrete signature, a variadic signature, a
  fallback and a finalizer under 'compute', then aliases the lot as
  'total'."""

  @overload(int)
  def compute(self, value: int) -> str:
    return 'int'

  @overload(str, *ARGS[int])
  def compute(self, value: str, *more) -> str:
    return 'variadic:%d' % len(more)

  @overload.fallback
  def compute(self, *args) -> str:
    return 'fallback'

  @overload.finalize
  def compute(self, *args) -> None:
    finalizeLog.append(args)

  total = compute


class TestShadowReads(MCLSTest):
  """
  TestShadowReads provides tests for reading hook-claimed names from
  the class body through the namespace shadow space.
  """

  def test_alias_dispatches_all_signatures(self) -> None:
    """
    Testing that an alias of an overloaded name receives every
    registered signature rather than only the last declaration.
    """
    calc = AliasCalc()
    self.assertEqual(calc.area(1), 2)
    self.assertEqual(calc.area('hi'), 'HI')
    self.assertEqual(calc.compute(1), 2)
    self.assertEqual(calc.compute('hi'), 'HI')

  def test_alias_beats_global_decoy(self) -> None:
    """
    Testing that the class body resolved the claimed name through the
    shadow space rather than escaping to the module-level decoy.
    """
    self.assertEqual(compute, 'global decoy')
    self.assertTrue(callable(AliasCalc.area))

  def test_alias_copies_variadic_fallback_finalizer(self) -> None:
    """
    Testing that an alias carries over variadic signatures, the
    fallback, and the finalizer registered under the source name.
    """
    full = AliasFull()
    before = len(finalizeLog)
    self.assertEqual(full.total(1), 'int')
    self.assertEqual(full.total('a', 2, 3), 'variadic:2')
    self.assertEqual(full.total(3.5), 'fallback')
    self.assertEqual(len(finalizeLog), before + 3)
