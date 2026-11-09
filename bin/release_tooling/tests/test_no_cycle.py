"""
TestNoCycle tests every button while no level is locked.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import ReleaseToolingTest

DEVS = ('dev', 'dev-minor', 'dev-major')


class TestNoCycle(ReleaseToolingTest):
  """
  After a full release, with 'LEVEL=none', every dev button opens a cycle
  of its level, locks that level and publishes the dev0 of its target,
  each needing its safety; every rc and lts button is refused, since an
  rc needs a dev cycle before it and a release needs an rc. The counters
  read as after 1.1.0, so micro targets 1.1.1, minor 1.2.0, major 2.0.0.
  """

  def test_presses(self) -> None:
    self.assertPresses(self.info(), {
      'dev': ('armed', '1.1.1-dev0', dict(level='micro', dev=1)),
      'dev-minor': ('armed', '1.2.0-dev0', dict(level='minor', dev=1)),
      'dev-major': ('armed', '2.0.0-dev0', dict(level='major', dev=1)),
      'rc': ('refused', DEVS),
      'rc-minor': ('refused', DEVS),
      'rc-major': ('refused', DEVS),
      'lts-micro': ('refused', DEVS),
      'lts-minor': ('refused', DEVS),
      'lts-major': ('refused', DEVS),
    })

  def test_after_a_minor_release(self) -> None:
    #  After 1.2.0 the counters read MINOR=2 MICRO=1: micro targets 1.2.1.
    info = self.info(minor=2, micro=1)
    self.assertPresses(info, {
      'dev': ('armed', '1.2.1-dev0', dict(level='micro', dev=1)),
      'dev-minor': ('armed', '1.3.0-dev0', dict(level='minor', dev=1)),
      'dev-major': ('armed', '2.0.0-dev0', dict(level='major', dev=1)),
      'rc': ('refused', DEVS),
      'rc-minor': ('refused', DEVS),
      'rc-major': ('refused', DEVS),
      'lts-micro': ('refused', DEVS),
      'lts-minor': ('refused', DEVS),
      'lts-major': ('refused', DEVS),
    })
