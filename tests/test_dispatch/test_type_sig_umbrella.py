"""
TestTypeSigUmbrella provides test coverage gymnastics for the TypeSig class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS, OWNER
from worktoy.dispatch import TypeSig
from . import DispatcherTest


class TestTypeSigUmbrella(DispatcherTest):
  """
  TestTypeSigUmbrella provides test coverage gymnastics for the TypeSig
  class.
  """

  def test_hash_rejects_unresolved_this(self) -> None:
    """A 'TypeSig' carrying the 'THIS' sentinel must refuse to hash
    until 'swapTHIS' has resolved the sentinel to a concrete class.
    After resolution the signature hashes like any other."""
    unresolved = TypeSig(THIS, int)
    with self.assertRaises(TypeError) as context:
      hash(unresolved)
    self.assertIn('THIS', str(context.exception))
    self.assertIn('swapTHIS', str(context.exception))

    class Owner:
      """placeholder concrete class"""

    unresolved.swapTHIS(Owner)
    self.assertEqual(hash(unresolved), hash(TypeSig(Owner, int)))

  def test_hash_plain_sig(self) -> None:
    """A 'TypeSig' built from concrete types is hashable on
    construction, no 'swapTHIS' required."""
    sig = TypeSig(int, str)
    self.assertEqual(hash(sig), hash(TypeSig(int, str)))

  def test_hash_uses_active_namespace_context(self) -> None:
    """When called from inside a class body whose namespace
    exposes '__hash_value__' and '__metaclass__',
    'TypeSig.__hash__' walks the frame stack via
    '_findActiveNamespace', finds the namespace, and substitutes
    'THIS' with the predicted class hash. The resulting hash
    matches what we get by hashing the substituted tuple
    directly."""
    from worktoy.mcls import BaseObject

    captured = {}

    class Probe(BaseObject):
      captured['withTHIS'] = hash(TypeSig(THIS, int))

    expected = hash((Probe.__namespace__.__hash_value__, int))
    self.assertEqual(captured['withTHIS'], expected)

  def test_call_substitutes_sentinels(self) -> None:
    """'TypeSig.__call__' returns a fresh 'TypeSig' with 'THIS' and
    'OWNER' substituted by the supplied values, leaving every
    other entry in the raw types untouched."""
    sig = TypeSig(THIS, OWNER, int)
    substituted = sig(this=42, owner=type)
    self.assertEqual(substituted._getRawTypes(), (42, type, int))

  def test_find_active_namespace_currentframe_returns_none(self) -> None:
    """On Python implementations without stack-frame support,
    'inspect.currentframe' is documented as possibly returning
    'None'. '_findActiveNamespace' must short-circuit and return
    'None' rather than crashing on the missing frame. This case is
    not naturally reachable on CPython, so we contrive it by
    temporarily replacing the module-level 'currentframe'
    reference with one that returns 'None'."""
    from worktoy.dispatch import _type_sig as typeSigModule
    originalCurrentframe = typeSigModule.currentframe
    typeSigModule.currentframe = lambda: None
    try:
      result = TypeSig._findActiveNamespace()
    finally:
      typeSigModule.currentframe = originalCurrentframe
    self.assertIsNone(result)

  def test_find_active_namespace_outside_class_body(self) -> None:
    """When called from a regular function frame, with no
    class-body frame anywhere up the call stack, the walk
    eventually exhausts 'frame.f_back' and the method falls out of
    the 'while' loop, hitting the trailing 'return None'. This
    test forces the walk to descend through several plain function
    frames before the exhaustion path is taken."""

    def deep1() -> object:
      return TypeSig._findActiveNamespace()

    def deep2() -> object:
      return deep1()

    def deep3() -> object:
      return deep2()

    self.assertIsNone(deep3())
