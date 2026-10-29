"""
TestMetaclassHelpers subclasses 'MCLSTest' and pins that 'AbstractMetaclass'
calls its own helpers, '_notifySubclassHook' and '_skipHash', through the
metaclass, so a class attribute of the same name cannot answer in their
place.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestMetaclassHelpers(MCLSTest):
  """
  TestMetaclassHelpers provides tests for the metaclass helpers that a
  class attribute shares a name with.
  """

  def test_subclass_hook_still_asked(self) -> None:
    """This method tests that a method named '_notifySubclassHook' in a
    class body does not stop the bases' '__subclasshook__' from being
    asked. 'Base' hears of 'Observed' and of 'Next'."""
    calls = []

    class Base(BaseObject):
      @classmethod
      def __subclasshook__(cls, sub: type) -> Any:
        calls.append(sub.__name__)
        return NotImplemented

    class Observed(Base):
      def _notifySubclassHook(self, *args: Any) -> None:
        pass  # pragma: no cover

    class Next(Observed):
      pass

    self.assertEqual(calls, ['Observed', 'Next'])

  def test_skip_hash_attribute_ignored(self) -> None:
    """This method tests that a class attribute named '_skipHash' does not
    take part in hashing the class. The class hashes as any other."""

    class Odd(BaseObject):
      _skipHash = None

    class Child(Odd):
      pass

    self.assertIsInstance(hash(Odd), int)
    self.assertIsInstance(hash(Child), int)
