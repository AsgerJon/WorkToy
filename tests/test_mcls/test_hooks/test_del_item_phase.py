"""
TestDelItemPhase subclasses 'SpaceHookTest' and pins the 'delItemPhase'
of 'AbstractSpaceHook': a 'del' in a class body runs it on every hook
with the name and the value being removed, before the namespace removes
the name. The default does nothing and returns False; a hook returning
True claims the deletion, and the namespace then leaves the name alone.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseMeta, BaseSpace
from worktoy.mcls.space_hooks import AbstractSpaceHook

from . import SpaceHookTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class RecordingHook(AbstractSpaceHook):
  """RecordingHook notes every deletion it is told of."""

  seen = []

  def delItemPhase(self, key: str, val: Any = None) -> bool:
    RecordingHook.seen.append((self.space.getClassName(), key, val))
    return key == 'kept'


class RecordingSpace(BaseSpace):
  """RecordingSpace declares the recording hook."""

  recordingHook = RecordingHook()


class RecordingMeta(BaseMeta):
  """RecordingMeta prepares a 'RecordingSpace'."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> RecordingSpace:
    return RecordingSpace(mcls, name, bases, **kwargs)


class TestDelItemPhase(SpaceHookTest):
  """
  TestDelItemPhase provides tests for the deletion phase of the hooks.
  """

  def setUp(self) -> None:
    super().setUp()
    RecordingHook.seen.clear()

  def test_phase_runs_with_name_and_value(self) -> None:
    """A deletion runs the phase with the name and the value removed, and
    the name is gone afterwards."""

    class Host(metaclass=RecordingMeta):
      gone = 1
      del gone

    self.assertEqual(RecordingHook.seen, [('Host', 'gone', 1)])
    self.assertNotIn('gone', Host.__dict__)

  def test_claimed_deletion_keeps_the_name(self) -> None:
    """A hook returning True claims the deletion, and the name stays."""

    class Host(metaclass=RecordingMeta):
      kept = 2
      del kept

    self.assertEqual(RecordingHook.seen, [('Host', 'kept', 2)])
    self.assertEqual(Host.__dict__['kept'], 2)

  def test_default_phase_is_inert(self) -> None:
    """The default 'delItemPhase' returns False."""
    self.assertIs(AbstractSpaceHook().delItemPhase('x', 1), False)
