"""
RefusedClassHooks holds the refusals that belong with
'design.promises.mcls.promise_class_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import UnboundClassHook


class RefusedClassHooks(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'len' and 'iter' of a class without the hook raise
  'TypeError', as for a plain class. A hook that is no classmethod raises
  'UnboundClassHook'. Source: the 'AbstractMetaclass' docstring and the
  'METACALL' docstring.
  """

  def test_plain_defaults_1(self) -> None:
    class Plain(BaseObject):
      pass

    with self.assertRaises(Exception) as refused:
      len(Plain)
    self.assertIsInstance(refused.exception, TypeError)

  def test_plain_defaults_2(self) -> None:
    class Plain(BaseObject):
      pass

    with self.assertRaises(Exception) as refused:
      iter(Plain)
    self.assertIsInstance(refused.exception, TypeError)

  def test_unbound_hook(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Counted(BaseObject):
        def __class_len__(cls) -> int:
          return 1
    self.assertIsInstance(refused.exception, UnboundClassHook)
