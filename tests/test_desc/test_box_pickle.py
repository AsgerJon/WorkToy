"""
TestBoxPickle subclasses 'DescTest' and pins that a box placed on a class
pickles by reference, as the descriptor declared on its owner, so a
pickled box comes back as the very box and an object a box tagged still
names that box in '__field_box__' after a round trip. A box used to be
rebuilt from its state by the default protocol, so the tag of an
unpickled field object named a second box no class held.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.desc import AttriBox, FixBox
from worktoy.mcls import BaseObject

from . import DescTest


class Val(BaseObject):
  """Val is a field type whose instances carry the box tags."""

  def __init__(self, *args) -> None:
    self.args = args


class Holder(BaseObject):
  """Holder declares the boxes the tests pickle."""

  v = AttriBox[Val](1)
  n = AttriBox[int](2)
  f = FixBox[str]('fixed')


def _roundTrip(obj):
  return pickle.loads(pickle.dumps(obj))


class TestBoxPickle(DescTest):
  """
  TestBoxPickle provides tests for pickling boxes and tagged objects.
  """

  def test_box_pickles_by_reference(self) -> None:
    """A placed box unpickles as the box declared on its owner."""
    box = Holder.__dict__['v']
    self.assertIs(_roundTrip(box), box)
    self.assertIs(_roundTrip(Holder.__dict__['f']), Holder.__dict__['f'])

  def test_tag_survives(self) -> None:
    """The field object of an unpickled owner names the class-level box,
    and the box tags name the owner and the field as before."""
    holder = Holder()
    value = holder.v
    self.assertIs(value.__field_box__, Holder.__dict__['v'])
    back = _roundTrip(holder)
    self.assertIsNot(back, holder)
    self.assertIsNot(back.v, value)
    self.assertIs(back.v.__field_box__, Holder.__dict__['v'])
    self.assertIs(back.v.__field_owner__, Holder)
    self.assertEqual(back.v.__field_name__, 'v')
    self.assertEqual(back.v.args, (1,))
    self.assertEqual(back.n, 2)
    self.assertEqual(back.f, 'fixed')

  def test_tagged_object_alone(self) -> None:
    """A tagged object pickled on its own keeps the same identity of
    its box."""
    value = _roundTrip(Holder().v)
    self.assertIs(value.__field_box__, Holder.__dict__['v'])

  def test_unplaced_box_unchanged(self) -> None:
    """A box no class holds has no owner to be found through and still
    pickles as a new box, by the default protocol."""
    box = AttriBox[int](3)
    back = _roundTrip(box)
    self.assertIsNot(back, box)
    self.assertIsInstance(back, AttriBox)
    self.assertIs(back.getFieldType(), int)
    self.assertEqual(back.__pos_args__, (3,))
