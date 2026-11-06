"""
TestContextInstance tests 'ContextInstance' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import ContextInstance, Object
from . import CoreTest


class TestContextInstance(CoreTest):
  """
  'self.instance' inside the hooks of an 'Object' must give the instance
  of the access in progress, and the same name read through the class
  must be harmless. 'ContextInstance' returns itself through the class
  and 'getContextInstance()' through an 'Object'. The tests pin both,
  with the frame pushed by hand.
  """

  def test_class_read_is_descriptor(self) -> None:
    self.assertIsInstance(Object.instance, ContextInstance)
    self.assertIsInstance(ContextInstance().__get__(None, Object),
                          ContextInstance)

  def test_instance_read_is_top_frame(self) -> None:
    desc = Object()
    first, second = object(), object()
    desc.createContext(first, type(first))
    self.assertIs(desc.instance, first)
    desc.createContext(second, type(second))
    self.assertIs(desc.instance, second)
    desc.exitContext()
    self.assertIs(desc.instance, first)
    desc.exitContext()
