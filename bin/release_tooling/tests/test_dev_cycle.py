"""
TestDevCycle tests every button while a dev cycle is open.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import ReleaseToolingTest


class TestDevCycle(ReleaseToolingTest):
  """
  With a level locked and no rc published yet, a dev press of the locked
  level is free and publishes the next devN; a dev press of a higher
  level needs its safety, relocks to that level and publishes its dev0; a
  dev press of a lower level is refused. The rc of the locked level needs
  its safety, publishes rc0 and so closes the dev cycle; every other rc
  is refused, and so is every lts, since a release needs an rc first.
  The counters read as after 1.1.0, with dev0 and dev1 published.
  """

  def test_micro_locked(self) -> None:
    accepted = ('dev', 'dev-minor', 'dev-major', 'rc')
    self.assertPresses(self.info(level='micro', dev=2), {
      'dev': ('free', '1.1.1-dev2', dict(dev=3)),
      'dev-minor': ('armed', '1.2.0-dev0', dict(level='minor', dev=1)),
      'dev-major': ('armed', '2.0.0-dev0', dict(level='major', dev=1)),
      'rc': ('armed', '1.1.1-rc0', dict(rc=1)),
      'rc-minor': ('refused', accepted),
      'rc-major': ('refused', accepted),
      'lts-micro': ('refused', accepted),
      'lts-minor': ('refused', accepted),
      'lts-major': ('refused', accepted),
    })

  def test_minor_locked(self) -> None:
    accepted = ('dev-minor', 'dev-major', 'rc-minor')
    self.assertPresses(self.info(level='minor', dev=2), {
      'dev': ('refused', accepted),
      'dev-minor': ('free', '1.2.0-dev2', dict(dev=3)),
      'dev-major': ('armed', '2.0.0-dev0', dict(level='major', dev=1)),
      'rc': ('refused', accepted),
      'rc-minor': ('armed', '1.2.0-rc0', dict(rc=1)),
      'rc-major': ('refused', accepted),
      'lts-micro': ('refused', accepted),
      'lts-minor': ('refused', accepted),
      'lts-major': ('refused', accepted),
    })

  def test_major_locked(self) -> None:
    accepted = ('dev-major', 'rc-major')
    self.assertPresses(self.info(level='major', dev=2), {
      'dev': ('refused', accepted),
      'dev-minor': ('refused', accepted),
      'dev-major': ('free', '2.0.0-dev2', dict(dev=3)),
      'rc': ('refused', accepted),
      'rc-minor': ('refused', accepted),
      'rc-major': ('armed', '2.0.0-rc0', dict(rc=1)),
      'lts-micro': ('refused', accepted),
      'lts-minor': ('refused', accepted),
      'lts-major': ('refused', accepted),
    })
