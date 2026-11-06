"""
TestObjectArguments tests the constructor arguments of 'Object' from
'worktoy.core' and their placeholders.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core.sentinels import THIS, OWNER, DESC
from . import CoreTest, Agreeable


class TestObjectArguments(CoreTest):
  """
  An 'Object' keeps the arguments it was built with, for a box to build
  its value from later, and replaces 'THIS', 'OWNER' and 'DESC' among
  them with the instance, the owner and the descriptor of the access in
  progress. The tests pin the keeping, the replacement inside and outside
  an access, that only a bare placeholder is replaced, that an unhashable
  argument passes untouched, and that a base after 'Object' is still
  initialized.
  """

  def test_arguments_kept(self) -> None:
    desc = Object(1, 'two', key=3)
    self.assertEqual(desc.getPosArgs(), (1, 'two'))
    self.assertEqual(desc.getKeyArgs(), {'key': 3})
    self.assertEqual(Object().getPosArgs(), ())
    self.assertEqual(Object().getKeyArgs(), {})

  def test_unconstructed_object(self) -> None:
    desc = Object.__new__(Object)
    self.assertEqual(desc.getPosArgs(), ())
    self.assertEqual(desc.getKeyArgs(), {})
    self.assertFalse(desc.hasSentinelArgs())
    self.assertFalse(desc.hasContext())

  def test_placeholders_outside_access(self) -> None:
    desc = Object(THIS, OWNER, DESC, a=THIS)
    self.assertEqual(desc.getPosArgs(), (THIS, OWNER, desc))
    self.assertEqual(desc.getKeyArgs(), {'a': THIS})
    sentinels = desc.getContextualSentinels()
    self.assertIs(sentinels[THIS], THIS)
    self.assertIs(sentinels[OWNER], OWNER)
    self.assertIs(sentinels[DESC], desc)

  def test_placeholders_inside_access(self) -> None:
    desc = Object(THIS, OWNER, DESC, a=THIS, b=OWNER)
    instance = object()
    desc.createContext(instance, int)
    self.assertEqual(desc.getPosArgs(), (instance, int, desc))
    self.assertEqual(desc.getKeyArgs(), {'a': instance, 'b': int})
    desc.exitContext()
    self.assertEqual(desc.getPosArgs(), (THIS, OWNER, desc))

  def test_top_frame_wins(self) -> None:
    desc = Object(THIS, OWNER)
    desc.createContext('first', str)
    desc.createContext(2, int)
    self.assertEqual(desc.getPosArgs(), (2, int))
    desc.exitContext()
    self.assertEqual(desc.getPosArgs(), ('first', str))
    desc.exitContext()

  def test_placeholders_told_by_identity(self) -> None:
    agreeable = Agreeable()
    self.assertTrue(agreeable == THIS)
    self.assertFalse(Object(agreeable, k=agreeable).hasSentinelArgs())
    self.assertIs(Object(agreeable).getPosArgs()[0], agreeable)

  def test_frame_without_instance(self) -> None:
    desc = Object(THIS, OWNER)
    desc.createContext(None, int)
    self.assertEqual(desc.getPosArgs(), (THIS, int))
    desc.exitContext()

  def test_placeholder_inside_container_kept(self) -> None:
    desc = Object([THIS], (OWNER,), a={'k': DESC})
    desc.createContext(object(), int)
    self.assertEqual(desc.getPosArgs(), ([THIS], (OWNER,)))
    self.assertEqual(desc.getKeyArgs(), {'a': {'k': DESC}})
    desc.exitContext()

  def test_unhashable_argument_passed_through(self) -> None:
    items = [1, 2]
    desc = Object(items, k={'a': 1})
    self.assertIs(desc.getPosArgs()[0], items)
    self.assertIs(desc.filterSentinels(items), items)
    self.assertEqual(desc.getKeyArgs(), {'k': {'a': 1}})

  def test_has_sentinel_args(self) -> None:
    self.assertTrue(Object(1, THIS).hasSentinelArgs())
    self.assertTrue(Object(OWNER).hasSentinelArgs())
    self.assertTrue(Object(k=DESC).hasSentinelArgs())
    self.assertFalse(Object(1, [THIS]).hasSentinelArgs())
    self.assertFalse(Object().hasSentinelArgs())

  def test_following_base_initialized(self) -> None:
    class Base:
      def __init__(self) -> None:
        self.touched = True

    class Both(Object, Base):
      pass

    both = Both(1, 2, k=3)
    self.assertTrue(both.touched)
    self.assertEqual(both.getPosArgs(), (1, 2))
    self.assertEqual(both.getKeyArgs(), {'k': 3})

  def test_random_arguments_round_trip(self) -> None:
    self.randomInteger.size = 4
    for _ in range(5):
      row = self.randomInteger.row
      desc = Object(*row, **{'k%d' % i: v for i, v in enumerate(row)})
      with self.subTest(row=row):
        self.assertEqual(desc.getPosArgs(), row)
        self.assertEqual((*desc.getKeyArgs().values(),), row)
