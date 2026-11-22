"""
RefusedThisReference holds the refusals that belong with
'design.promises.desc.promise_this_reference'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import TestCase

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import ReferenceConflict, DanglingAlias

if sys.version_info >= (3, 9):
  from ...promises.desc._this_decorator_helpers import makeWatchedSpeaker


class RefusedThisReference(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A body declaring 'volume' itself and decorating
  'THIS[Parent].volume' as well raises 'ReferenceConflict', and a name no
  class holds raises 'DanglingAlias'. Source: the 'THIS' docstring, and the
  1.1.0 changelog entries "A subclass expands on an inherited descriptor
  through THIS" and "THIS refuses a reference to a name the class body
  declares itself".
  """

  def makeSpeaker(self) -> type:
    class Speaker(BaseObject):
      volume = AttriBox[int](5)

    return Speaker

  def test_conflict(self) -> None:
    Speaker = self.makeSpeaker()
    with self.assertRaises(Exception) as refused:
      class Booming(Speaker):
        volume = AttriBox[int](11)

        def _watch(self, value: int) -> None:
          pass

        _watch = THIS[Speaker].volume.onSet(_watch)
    self.assertIsInstance(refused.exception, ReferenceConflict)

  def test_dangling(self) -> None:
    Speaker = self.makeSpeaker()
    with self.assertRaises(Exception) as refused:
      class Quiet(Speaker):
        def _watch(self, value: int) -> None:
          pass

        _watch = THIS[Speaker].mute.onSet(_watch)
    self.assertIsInstance(refused.exception, DanglingAlias)
