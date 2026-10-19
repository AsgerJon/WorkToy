"""
TestTypeSigUmbrella provides test coverage gymnastics for the TypeSig class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.core.sentinels import THIS, OWNER
from worktoy.dispatch import TypeSig, overload
from worktoy.mcls import BaseObject
from . import DispatcherTest


class TestTypeSigUmbrella(DispatcherTest):
  """
  TestTypeSigUmbrella provides test coverage gymnastics for the TypeSig
  class.
  """

  def test_hash_is_the_hash_of_the_raw_types(self) -> None:
    """A 'TypeSig' hashes as the tuple of its raw types wherever it is
    hashed. 'THIS' is a class and hashes as one, so a signature holding
    it hashes before 'swapTHIS' as well as after, each time through the
    types it holds at that moment."""
    unresolved = TypeSig(THIS, int)
    self.assertEqual(hash(unresolved), hash((THIS, int)))

    class Owner:
      """placeholder concrete class"""

    unresolved.swapTHIS(Owner)
    self.assertEqual(hash(unresolved), hash((Owner, int)))
    self.assertEqual(hash(unresolved), hash(TypeSig(Owner, int)))

  def test_hash_plain_sig(self) -> None:
    """A 'TypeSig' built from concrete types is hashable on
    construction, no 'swapTHIS' required."""
    sig = TypeSig(int, str)
    self.assertEqual(hash(sig), hash(TypeSig(int, str)))

  def test_hash_inside_class_body(self) -> None:
    """Inside a class body built by 'BaseMeta', a signature holding
    'THIS' hashes as it does anywhere else, as the tuple of its raw
    types, with nothing read off the namespace or the call stack."""
    captured = {}

    class Probe(BaseObject):
      captured['withTHIS'] = hash(TypeSig(THIS, int))

    self.assertEqual(captured['withTHIS'], hash((THIS, int)))
    self.assertEqual(captured['withTHIS'], hash(TypeSig(THIS, int)))

  def test_call_substitutes_sentinels(self) -> None:
    """'TypeSig.__call__' returns a fresh 'TypeSig' with 'THIS' and
    'OWNER' substituted by the supplied values, leaving every
    other entry in the raw types untouched."""
    sig = TypeSig(THIS, OWNER, int)
    substituted = sig(this=42, owner=type)
    self.assertEqual(substituted.getRawTypes(), (42, type, int))

  def test_dispatch_without_frame_support(self) -> None:
    """Nothing in the hashing of a signature inspects the call stack, so
    a class overloading on 'THIS' is built, and dispatches, on an
    interpreter without frame support. 'inspect.currentframe' documents
    such an interpreter as one where 'sys._getframe' is missing and
    answers None there, so the attribute is removed for the duration of
    the class statement and the calls."""
    getFrame = sys._getframe
    del sys._getframe
    try:
      class Frameless(BaseObject):
        @overload(int)
        def __init__(self, value: int) -> None:
          self.value = value

        @overload(THIS)
        def __init__(self, other: Frameless) -> None:
          self.value = other.value

      first = Frameless(7)
      second = Frameless(first)
    finally:
      sys._getframe = getFrame
    self.assertEqual(second.value, 7)
    self.assertIsInstance(second, Frameless)
