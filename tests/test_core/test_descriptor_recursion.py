"""TestDescriptorRecursion stress-tests the stack-based context
machinery in 'Object' by re-entering the same descriptor object
through nested attribute access. Each frame must see its own
'(instance, owner)' regardless of how deeply the stack grows, and
the stack must unwind cleanly even when an exception propagates."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject
from . import CoreTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, List


class Probe(BaseObject):
  """Descriptor that records its 'self.instance' at each call level
  and, if the active instance has a non-None '_next', triggers itself
  again on that next link. After the recursive call returns, the
  descriptor verifies its 'self.instance' is still the same object
  it observed before the recursion. If the context stack misbehaves,
  the assertion fires inside this method, not the test."""

  __log__: List[Any] = []
  __raise_at__ = None

  def __instance_get__(self, *args, **kwargs) -> Any:
    here = self.instance
    Probe.__log__.append(here)
    if Probe.__raise_at__ is not None:
      if len(Probe.__log__) == Probe.__raise_at__:
        raise RuntimeError(
          'Forced raise at depth %d' % Probe.__raise_at__
        )
    nextTarget = getattr(here, '_next', None)
    if nextTarget is not None:
      _ = nextTarget.probe
    return here


class Link:
  """A linked-list node hosting the shared 'Probe' descriptor."""

  probe = Probe()

  def __init__(self, label: str, nxt: 'Link' = None) -> None:
    self.label = label
    self._next = nxt


class TestDescriptorRecursion(CoreTest):
  """Stress-tests the stack-based context machinery against nasty
  re-entrant access patterns to the same descriptor object."""

  def setUp(self) -> None:
    Probe.__log__ = []
    Probe.__raise_at__ = None

  def tearDown(self) -> None:
    """No matter what each test did, the descriptor's context stack
    must be empty when the dust settles."""
    self.assertFalse(Link.probe.hasContext())

  def test_two_link_chain(self) -> None:
    """Outer call must observe its own instance after inner returns."""
    b = Link('b')
    a = Link('a', nxt=b)
    result = a.probe
    self.assertIs(result, a)
    seen = [link.label for link in Probe.__log__]
    self.assertEqual(seen, ['a', 'b'])

  def test_deep_chain(self) -> None:
    """A 50-deep chain pushes and pops 50 frames without corruption."""
    chain = None
    for i in range(50):
      chain = Link(str(i), nxt=chain)
    _ = chain.probe
    self.assertEqual(len(Probe.__log__), 50)

  def test_exception_unwinds_stack(self) -> None:
    """An exception raised mid-chain must still leave the stack
    empty, because 'with' guarantees '__exit__' is called on every
    frame on the way back up."""
    c = Link('c')
    b = Link('b', nxt=c)
    a = Link('a', nxt=b)
    Probe.__raise_at__ = 2
    with self.assertRaises(RuntimeError):
      _ = a.probe
    self.assertFalse(Link.probe.hasContext())

  def test_repeated_independent_calls(self) -> None:
    """Multiple top-level descriptor accesses, each unrelated to
    the next, must each leave the stack at zero depth."""
    a = Link('a')
    b = Link('b')
    _ = a.probe
    self.assertFalse(Link.probe.hasContext())
    _ = b.probe
    self.assertFalse(Link.probe.hasContext())
    _ = a.probe
    self.assertFalse(Link.probe.hasContext())
    self.assertEqual(len(Probe.__log__), 3)

  def test_manual_push_pop_balance(self) -> None:
    """Direct 'createContext' / 'exitContext' calls must balance
    even when interleaved in a non-stack-friendly-looking order
    (here, three pushes then three pops)."""
    a = Link('a')
    b = Link('b')
    c = Link('c')
    Link.probe.createContext(a, Link)
    Link.probe.createContext(b, Link)
    Link.probe.createContext(c, Link)
    self.assertIs(Link.probe.getContextInstance(), c)
    Link.probe.exitContext()
    self.assertIs(Link.probe.getContextInstance(), b)
    Link.probe.exitContext()
    self.assertIs(Link.probe.getContextInstance(), a)
    Link.probe.exitContext()
    self.assertFalse(Link.probe.hasContext())
