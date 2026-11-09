"""
TestRcCycle tests every button while a release candidate cycle is open.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import ReleaseToolingTest


class TestRcCycle(ReleaseToolingTest):
  """
  Once the rc0 of the locked level is out, the rc of that level is free
  and publishes the next rcN, and the lts of that level needs its safety,
  publishes the release, unlocks the level and moves the counters as the
  lts buttons always have: MICRO up for micro; MINOR up and MICRO to 1 for
  minor; MAJOR up, MINOR to 0 and MICRO to 1 for major; RC and DEV to 0.
  Every dev and every button of another level is refused, since an rc
  freezes the scope. The counters read as after 1.1.0, with dev0, dev1
  and rc0 published.
  """

  def test_micro_locked(self) -> None:
    accepted = ('rc', 'lts-micro')
    release = dict(micro=2, rc=0, dev=0, level='none')
    self.assertPresses(self.info(level='micro', dev=2, rc=1), {
      'dev': ('refused', accepted),
      'dev-minor': ('refused', accepted),
      'dev-major': ('refused', accepted),
      'rc': ('free', '1.1.1-rc1', dict(rc=2)),
      'rc-minor': ('refused', accepted),
      'rc-major': ('refused', accepted),
      'lts-micro': ('armed', '1.1.1', release),
      'lts-minor': ('refused', accepted),
      'lts-major': ('refused', accepted),
    })

  def test_minor_locked(self) -> None:
    accepted = ('rc-minor', 'lts-minor')
    release = dict(minor=2, micro=1, rc=0, dev=0, level='none')
    self.assertPresses(self.info(level='minor', dev=2, rc=1), {
      'dev': ('refused', accepted),
      'dev-minor': ('refused', accepted),
      'dev-major': ('refused', accepted),
      'rc': ('refused', accepted),
      'rc-minor': ('free', '1.2.0-rc1', dict(rc=2)),
      'rc-major': ('refused', accepted),
      'lts-micro': ('refused', accepted),
      'lts-minor': ('armed', '1.2.0', release),
      'lts-major': ('refused', accepted),
    })

  def test_major_locked(self) -> None:
    accepted = ('rc-major', 'lts-major')
    release = dict(major=2, minor=0, micro=1, rc=0, dev=0, level='none')
    self.assertPresses(self.info(level='major', dev=2, rc=1), {
      'dev': ('refused', accepted),
      'dev-minor': ('refused', accepted),
      'dev-major': ('refused', accepted),
      'rc': ('refused', accepted),
      'rc-minor': ('refused', accepted),
      'rc-major': ('free', '2.0.0-rc1', dict(rc=2)),
      'lts-micro': ('refused', accepted),
      'lts-minor': ('refused', accepted),
      'lts-major': ('armed', '2.0.0', release),
    })
