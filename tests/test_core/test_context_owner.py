"""
TestContextOwner tests 'ContextOwner' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import ContextOwner, Object
from . import CoreTest


class TestContextOwner(CoreTest):
  """
  'self.owner' inside the hooks of an 'Object' must give the owner of
  the access in progress. 'ContextOwner' returns itself through the
  class and 'getContextOwner()' through an 'Object'. The tests pin both,
  with the frame pushed by hand.
  """

  def test_class_read_is_descriptor(self) -> None:
    self.assertIsInstance(Object.owner, ContextOwner)
    self.assertIsInstance(ContextOwner().__get__(None, Object), ContextOwner)

  def test_instance_read_is_top_frame(self) -> None:
    desc = Object()
    desc.createContext(1, int)
    self.assertIs(desc.owner, int)
    desc.createContext('a', str)
    self.assertIs(desc.owner, str)
    desc.exitContext()
    self.assertIs(desc.owner, int)
    desc.exitContext()
