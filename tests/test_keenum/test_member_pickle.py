"""
TestMemberPickle subclasses 'KeeTest' and pins that 'KeeNum' and
'KeeFlags' members survive a 'pickle' round trip as themselves. A member
is a singleton whose equality is identity (for 'KeeNum') or
owner-and-index (for 'KeeFlags'), so the default protocol, which rebuilt
a fresh instance from the member's state, returned a phantom that was
not the member and compared unequal to it. The members therefore reduce
to a lookup of their name on their class, the same defence the standard
library 'enum' applies to its members.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag
from . import KeeTest
from .examples import RootRGB, MoreRGB


class Color(KeeNum):
  """Color is a small value enumeration used by the pickle probes."""

  RED = Kee[int](1)
  GREEN = Kee[int](2)


class Perm(KeeFlags):
  """Perm is a small bitmask-flag enumeration used by the pickle probes."""

  READ = KeeFlag()
  WRITE = KeeFlag()


def _roundTrip(obj: object, protocol: int = None) -> object:
  if protocol is None:
    return pickle.loads(pickle.dumps(obj))
  return pickle.loads(pickle.dumps(obj, protocol))


class TestMemberPickle(KeeTest):
  """
  TestMemberPickle provides tests for the pickle identity of 'KeeNum' and
  'KeeFlags' members.
  """

  def test_keenum_round_trip_is_member(self) -> None:
    """An unpickled 'KeeNum' member is the member itself."""
    self.assertIs(_roundTrip(Color.RED), Color.RED)
    self.assertIs(_roundTrip(Color.GREEN), Color.GREEN)

  def test_keenum_every_protocol(self) -> None:
    """Every pickle protocol returns the member itself."""
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
      self.assertIs(_roundTrip(Color.RED, protocol), Color.RED)

  def test_keenum_equal_and_dict_key(self) -> None:
    """An unpickled 'KeeNum' member compares equal to the canonical
    member and resolves the same mapping entry."""
    members = {Color.RED: 'red', Color.GREEN: 'green'}
    back = _roundTrip(Color.RED)
    self.assertEqual(back, Color.RED)
    self.assertEqual(members[back], 'red')

  def test_keenum_inside_container(self) -> None:
    """A 'KeeNum' member carried inside a pickled container survives as
    the canonical member."""
    config = {'color': Color.GREEN, 'all': [Color.RED, Color.GREEN]}
    back = _roundTrip(config)
    self.assertIs(back['color'], Color.GREEN)
    self.assertIs(back['all'][0], Color.RED)

  def test_keenum_subclass_member(self) -> None:
    """A derived enumeration shares the members of its parent and adds
    its own; a member reached through either class unpickles as the one
    shared member, and an added member as itself."""
    self.assertIs(MoreRGB.RED, RootRGB.RED)
    self.assertIs(_roundTrip(MoreRGB.RED), RootRGB.RED)
    self.assertIs(_roundTrip(RootRGB.RED), RootRGB.RED)
    self.assertIs(type(MoreRGB.CYAN), MoreRGB)
    self.assertIs(_roundTrip(MoreRGB.CYAN), MoreRGB.CYAN)

  def test_keenum_reduce_names_class_and_name(self) -> None:
    """The reduction is a lookup of the member name on the class."""
    func, args = Color.RED.__reduce__()[:2]
    self.assertIs(func, getattr)
    self.assertEqual(args, (Color, 'RED'))

  def test_keeflags_round_trip_is_member(self) -> None:
    """An unpickled 'KeeFlags' member is the member itself, the empty
    member and a combined member included."""
    self.assertIs(_roundTrip(Perm.READ), Perm.READ)
    self.assertIs(_roundTrip(Perm.NULL), Perm.NULL)
    self.assertIs(_roundTrip(Perm.READ_WRITE), Perm.READ_WRITE)

  def test_keeflags_every_protocol(self) -> None:
    """Every pickle protocol returns the member itself."""
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
      self.assertIs(_roundTrip(Perm.READ_WRITE, protocol), Perm.READ_WRITE)

  def test_keeflags_inside_container(self) -> None:
    """A 'KeeFlags' member carried inside a pickled container survives
    as the canonical member, so 'is' checks against it hold."""
    back = _roundTrip({'mode': Perm.WRITE})
    self.assertIs(back['mode'], Perm.WRITE)

  def test_keeflags_reduce_names_class_and_name(self) -> None:
    """The reduction is a lookup of the canonical name on the class."""
    func, args = Perm.READ_WRITE.__reduce__()[:2]
    self.assertIs(func, getattr)
    self.assertEqual(args, (Perm, 'READ_WRITE'))
