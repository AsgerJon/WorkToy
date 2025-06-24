"""
TestAbstractNamespace provides the basic unit tests for the
'AbstractNamespace' class from the 'worktoy.mcls' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass, AbstractNamespace
from worktoy.mcls.hooks import AbstractHook
from worktoy.waitaminute import DuplicateHookError, HookException
from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestAbstractNamespace(TestCase):
  """
  Much of the functionality of the 'AbstractNamespace' class is depended
  upon by the combined functionality of the metaclass systems. This
  functionality is thoroughly tested elsewhere. This test class covers the
  remaining functionality. Thus, this test class is mostly testing subtle
  edge cases.
  """

  @classmethod
  def tearDownClass(cls):
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_duplicate_hook(self) -> None:
    """
    Tests that a 'DuplicateHookError' is raised when adding a hook to a
    namespace already containing a hook with the same name.
    """

    hookA, hookB = AbstractHook(), AbstractHook()

    class BaseNamespace(AbstractNamespace):
      """Base namespace for testing duplicate hooks."""
      breh = hookA

    setattr(hookB, '__field_name__', 'breh')

    with self.assertRaises(DuplicateHookError) as context:
      BaseNamespace.addHook(hookA)  # For coverage, doesn't raise
      BaseNamespace.addHook(hookB)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.owner, BaseNamespace)
    self.assertEqual(e.name, 'breh')
    self.assertIs(e.existingHook, hookA)
    self.assertIs(e.newHook, hookB)

  def test_hook_exception(self) -> None:
    """
    Tests that a 'HookException' is raised when a hook raises an exception
    during the different hook phases.
    """

    class Yikes(Exception):
      """A custom exception to be raised by the hook."""

    class SusHook(AbstractHook):
      """A hook that raises an exception."""

      def getItemHook(self, key: str, value: Any, ) -> bool:
        """
        Raises 'Yikes'
        """
        raise Yikes

    class SusSpace(AbstractNamespace):
      """A namespace that uses the 'SusHook'."""
      sus = SusHook()

    class SusMeta(AbstractMetaclass):
      """A metaclass that uses the 'SusSpace'."""

      @classmethod
      def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> SusSpace:
        """
        Prepares the namespace for the metaclass.
        """
        return SusSpace(mcls, name, bases, **kwargs)

    with self.assertRaises(HookException) as context:
      class SusClass(metaclass=SusMeta):
        """A class that uses the 'SusMeta'."""

    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e.initialException, Yikes)
    self.assertIsInstance(e.namespaceObject, SusSpace)
    self.assertEqual(e.itemKey, '__name__')
    self.assertEqual(str(e.errorValue), str(KeyError('__name__')))
    self.assertIsInstance(e.hookFunction, SusHook)
