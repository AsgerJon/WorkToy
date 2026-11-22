"""
RefusedFixBox holds the refusals that belong with
'design.promises.desc.promise_fix_box'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import FixBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import WriteOnceError, ProtectedError


class RefusedFixBox(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A later assignment to a 'FixBox' raises 'WriteOnceError', a
  'TypeError', even of the same value, and a deletion raises
  'ProtectedError'. Source: the 'FixBox' docstring and its example.
  """

  def test_first_value_final_1(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    config.port = 9000
    with self.assertRaises(Exception) as refused:
      config.port = 1
    self.assertIsInstance(refused.exception, WriteOnceError)

  def test_first_value_final_2(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    config.port = 9000
    with self.assertRaises(Exception) as refused:
      del config.port
    self.assertIsInstance(refused.exception, ProtectedError)

  def test_first_value_final_3(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    config.port = 9000
    with self.assertRaises(Exception) as refused:
      config.port = 9000
    self.assertIsInstance(refused.exception, WriteOnceError)

  def test_read_fixes_default(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    self.assertEqual(config.port, 8080)
    with self.assertRaises(Exception) as refused:
      config.port = 1
    self.assertIsInstance(refused.exception, WriteOnceError)
