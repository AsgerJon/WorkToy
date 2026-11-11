"""
PromiseFixBox promises 'FixBox' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import FixBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import WriteOnceError, ProtectedError


class PromiseFixBox(TestCase):
  """
  A 'FixBox' is an 'AttriBox' whose first stored value is final: a later
  assignment raises 'WriteOnceError', a 'TypeError', even of the same
  value, and a deletion
  raises 'ProtectedError'. A read stores the default it builds, so a
  value meant to be set at run time is assigned before anything reads
  it. Source: the 'FixBox' docstring and its example.
  """

  def test_first_value_final(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    config.port = 9000
    self.assertEqual(config.port, 9000)
    with self.assertRaises(WriteOnceError) as context:
      config.port = 1
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIs(e.desc, vars(Config)['port'])
    self.assertEqual(e.oldValue, 9000)
    self.assertEqual(e.newValue, 1)
    with self.assertRaises(ProtectedError):
      del config.port
    with self.assertRaises(WriteOnceError):
      config.port = 9000

  def test_read_fixes_default(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    self.assertEqual(config.port, 8080)
    with self.assertRaises(WriteOnceError) as context:
      config.port = 1
    self.assertEqual(context.exception.oldValue, 8080)
