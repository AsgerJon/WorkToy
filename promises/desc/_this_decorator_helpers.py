"""
The private file '_this_decorator_helpers' builds the classes that use
'@THIS[Parent].name.onSet' as a decorator, which Python accepts from
3.9 on (PEP 614). It is imported only there, so the promises keep
running on the older versions.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS


def makeWatchedSpeaker(Speaker: type, seen: list) -> type:
  """
  The 'makeWatchedSpeaker' function builds a subclass of 'Speaker' that
  watches the inherited 'volume' through the decorator form.
  """

  class LoudSpeaker(Speaker):
    @THIS[Speaker].volume.onSet
    def _watchVolume(self, value: int) -> None:
      seen.append(value)

  return LoudSpeaker
