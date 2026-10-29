"""
TestShadowReads pins the namespace shadow space: a class-body name
claimed by a space hook remains readable later in the same body. The
namespace records every assignment in a shadow mapping and answers reads
from it when the name is absent from the namespace itself. Without the
shadow, reading a claimed name escapes to the module scope, silently
finding whatever global happens to share the name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from .. import MCLSTest

#  Module-level decoy sharing its name with the overloaded method below.
#  Without the shadow space, the read in the class body would find this
#  string instead of the overload.
compute = 'global decoy'


class ShadowCalc(BaseObject):
  """ShadowCalc overloads 'compute' for 'int' and 'str' and reads the
  name back between the two declarations."""

  @overload(int)
  def compute(self, value: int) -> int:
    return value + 1

  computeRead = isinstance(compute, overload)

  @overload(str)
  def compute(self, value: str) -> str:
    return str.upper(value)


class TestShadowReads(MCLSTest):
  """
  TestShadowReads provides tests for reading hook-claimed names from
  the class body through the namespace shadow space.
  """

  def test_claimed_name_read_in_body(self) -> None:
    """This method tests that reading an overloaded name later in its
    class body does not find the module-level name of the same spelling.
    The read gives the 'overload' object."""
    self.assertIs(ShadowCalc.computeRead, True)
    self.assertEqual(compute, 'global decoy')

  def test_read_keeps_every_overload(self) -> None:
    """This method tests that reading an overloaded name in its class
    body does not cost the name an overload declared before or after the
    read."""
    calc = ShadowCalc()
    self.assertEqual(calc.compute(1), 2)
    self.assertEqual(calc.compute('hi'), 'HI')
