"""
TestOverridePrecedence subclasses 'OverloadTest' and pins that an overload
declared in a subclass takes precedence over the overload it overrides in
a parent class. Precedence must not depend on which dispatch pass happens
to match the call. A long call to a variadic overload is matched by
walking the variadic signatures rather than by an exact lookup. A call
whose argument is an instance of a further subclass is matched by
'isinstance' rather than by an exact lookup. The override must win in
both cases, just as it wins the exact lookup.

Casting is the one place the parent goes first. When no signature
matches without a cast, inherited signatures are tried before the ones
a subclass added, so adding a signature in a subclass never redirects a
call the parent already handled. An overridden signature is gone
entirely, however, and never receives a cast call in place of its
override.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Reader(BaseObject):
  """Reader declares a variadic overload taking one or more integers."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, *ARGS[int])
  def read(self, *codes: int) -> str:
    return 'reader'


class Scanner(Reader):
  """Scanner overrides the variadic overload of 'Reader' with an equal
  signature, so every call that 'Reader.read' accepts must now reach
  'Scanner.read' instead."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, *ARGS[int])
  def read(self, *codes: int) -> str:
    return 'scanner'


class DeepScanner(Scanner):
  """DeepScanner declares nothing and inherits both variadic
  registrations, the overriding one from 'Scanner' and the overridden
  one from 'Reader'."""


class Node(BaseObject):
  """Node declares an overload taking another instance of its own class
  through the 'THIS' sentinel."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def link(self, other: Node) -> str:
    return 'node'


class Branch(Node):
  """Branch overrides the 'THIS' overload of 'Node'. The two signatures
  are not equal once 'THIS' is resolved, since one names 'Node' and the
  other 'Branch'. A 'Branch' argument matches both, and the override
  must take it."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def link(self, other: Branch) -> str:
    return 'branch'


class Leaf(Branch):
  """Leaf declares nothing. Its instances are 'Branch' instances that no
  signature names exactly, so they are matched through 'isinstance'."""


class Meter(BaseObject):
  """Meter measures a 'float', and so also an 'int' cast to one."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float)
  def measure(self, x: float) -> str:
    return 'meter'


class Gauge(Meter):
  """Gauge adds a signature for a 'complex', to which an 'int' casts as
  well. The added signature must not take the 'int' calls that 'Meter'
  already handles through its cast to 'float'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(complex)
  def measure(self, z: complex) -> str:
    return 'gauge'


class Tally(BaseObject):
  """Tally adds up any number of values given as 'float', and so also
  any number of 'int' values cast to 'float'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(*ARGS[float])
  def add(self, *values: float) -> str:
    return 'tally'


class Ledger(Tally):
  """Ledger adds a variadic signature for 'complex' values, to which
  'int' values cast as well. Calls of 'int' values of any length must
  keep reaching the signature inherited from 'Tally'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(*ARGS[complex])
  def add(self, *values: complex) -> str:
    return 'ledger'


class TestOverridePrecedence(OverloadTest):
  """
  TestOverridePrecedence pins that a subclass overload beats the parent
  overload it overrides in every dispatch pass, and that the parent
  overload still receives the calls the override does not accept.
  """

  def setUp(self) -> None:
    """
    The long call exceeds the number of variadic lengths the overload
    decorator expands into exact signatures, so it can only be matched
    by walking the variadic signatures.
    """
    super().setUp()
    self.longCall = (*range(overload.__variadic_fastpath_limit__ + 2),)

  def test_variadic_override_short_call(self) -> None:
    """
    Testing that a short call reaches the variadic override. Short calls
    are matched by the exact signatures the decorator expanded, which
    the override already displaces.
    """
    self.assertEqual(Reader().read(1, 2), 'reader')
    self.assertEqual(Scanner().read(1, 2), 'scanner')

  def test_variadic_override_long_call(self) -> None:
    """
    Testing that a call too long for the expanded signatures still
    reaches the variadic override rather than the overridden parent
    version.
    """
    self.assertEqual(Reader().read(*self.longCall), 'reader')
    self.assertEqual(Scanner().read(*self.longCall), 'scanner')

  def test_variadic_override_inherited(self) -> None:
    """
    Testing that a class inheriting both variadic registrations sends
    calls of every length to the nearer one, 'Scanner.read'.
    """
    self.assertEqual(DeepScanner().read(1, 2), 'scanner')
    self.assertEqual(DeepScanner().read(*self.longCall), 'scanner')

  def test_this_override_exact_argument(self) -> None:
    """
    Testing that a 'Branch' argument reaches the override. The argument
    type matches the resolved signature of the override exactly.
    """
    self.assertEqual(Branch().link(Branch()), 'branch')

  def test_this_override_subclass_argument(self) -> None:
    """
    Testing that a 'Leaf' argument reaches the override as well. No
    signature names 'Leaf', so both the override and the overridden
    'Node' version match through 'isinstance', and the override must
    win.
    """
    self.assertEqual(Branch().link(Leaf()), 'branch')

  def test_this_override_inherited(self) -> None:
    """
    Testing that 'Leaf', which inherits both registrations, sends a
    'Leaf' argument to the nearer one, 'Branch.link'.
    """
    self.assertEqual(Leaf().link(Leaf()), 'branch')

  def test_this_parent_argument(self) -> None:
    """
    Testing that a plain 'Node' argument, which the override does not
    accept, still reaches the overridden 'Node' version.
    """
    self.assertEqual(Branch().link(Node()), 'node')

  def test_cast_prefers_inherited_signature(self) -> None:
    """
    Testing that an 'int', which matches no signature without a cast,
    reaches the 'float' signature 'Gauge' inherits rather than the
    'complex' signature it added. Arguments matching a signature without
    a cast still reach it directly.
    """
    self.assertEqual(Gauge().measure(1), 'meter')
    self.assertEqual(Gauge().measure(1.5), 'meter')
    self.assertEqual(Gauge().measure(1j), 'gauge')

  def test_variadic_cast_prefers_inherited_signature(self) -> None:
    """
    Testing that 'int' values, which match no variadic signature without
    a cast, reach the 'float' signature 'Ledger' inherits rather than the
    'complex' one it added. This holds for short calls, matched through
    the expanded signatures, and for long calls, matched by walking the
    variadic signatures. 'complex' values still reach the added
    signature directly.
    """
    self.assertEqual(Ledger().add(1, 2), 'tally')
    self.assertEqual(Ledger().add(*self.longCall), 'tally')
    self.assertEqual(Ledger().add(1j, 2j), 'ledger')
    longComplex = [complex(n) for n in self.longCall]
    self.assertEqual(Ledger().add(*longComplex), 'ledger')

  def test_variadic_override_cast_call(self) -> None:
    """
    Testing that calls reaching the variadic signatures only through a
    cast, of short and long length alike, still reach the override. The
    overridden signature of 'Reader' is equal to the override and so is
    gone from 'Scanner' altogether, even from the cast passes that try
    inherited signatures first.
    """
    longStrings = [str(n) for n in self.longCall]
    self.assertEqual(Scanner().read('1', '2'), 'scanner')
    self.assertEqual(Scanner().read(*longStrings), 'scanner')
