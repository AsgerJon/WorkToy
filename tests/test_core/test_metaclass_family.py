"""
TestMetaclassFamily subclasses 'CoreTest' and pins that 'SentinelMeta'
and 'MetaFlow' both subclass 'MetaType' and derive from it, as
'AbstractMetaclass' does, so every metaclass of the library but the
'ValidSlice' validator of 'utilities' is one family. The two used to
subclass 'type' directly, so a sentinel or a control-flow signal declared
with a class keyword reached the refusal of 'object.__init_subclass__'
that '_Chill' ends for every other worktoy class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core.control_flow import ControlFlow, MetaFlow, SkipSet
from worktoy.core.sentinels import ARGS, Sentinel, SentinelMeta, THIS
from worktoy.core.sentinels._args import _MetaARGS
from worktoy.core._meta_type import _Chill
from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute.meta import IllegalInstantiation, ControlClassError

from . import CoreTest


class TestMetaclassFamily(CoreTest):
  """
  TestMetaclassFamily provides tests for the metaclass family of 'core'.
  """

  def test_subclass_and_derive(self) -> None:
    """Each metaclass subclasses 'MetaType' and derives from it."""
    for mcls in (SentinelMeta, _MetaARGS, MetaFlow, AbstractMetaclass):
      with self.subTest(mcls=mcls.__name__):
        self.assertTrue(issubclass(mcls, MetaType))
        self.assertIs(type(mcls), MetaType)

  def test_sentinel_keyword_absorbed(self) -> None:
    """A sentinel declared with a class keyword builds, the chain of
    '__init_subclass__' ending at '_Chill'."""

    class KEYWORDED(Sentinel, flag=True):
      """A sentinel declared with a keyword."""

    self.assertTrue(issubclass(KEYWORDED, Sentinel))
    self.assertIn(_Chill, Sentinel.__mro__)
    self.assertEqual(str(KEYWORDED), "<Sentinel: 'KEYWORDED'>")

  def test_signal_keyword_absorbed(self) -> None:
    """A signal declared with a class keyword builds the same way, and
    the '_root' keyword still reaches 'MetaFlow'."""

    class Halt(ControlFlow, flag=True):
      pass

    self.assertTrue(issubclass(Halt, ControlFlow))
    self.assertIn(_Chill, ControlFlow.__mro__)
    self.assertIs(MetaFlow.getRootClass(), ControlFlow)
    self.assertEqual(str(Halt), '<ControlFlow: Halt>')

  def test_behaviour_kept(self) -> None:
    """Rendering, the instantiation refusal, the subscript of 'ARGS',
    the class-body guard of a signal and the signal itself are as
    before."""
    self.assertEqual(str(THIS), "<Sentinel: 'THIS'>")
    with self.assertRaises(IllegalInstantiation):
      THIS()
    self.assertIs(ARGS[int].__inner_type__, int)
    self.assertEqual(str(ControlFlow), '<ControlFlow: [Root]>')
    with self.assertRaises(ControlClassError):
      class Chatty(ControlFlow):
        tone = 'loud'
    with self.assertRaises(SkipSet):
      raise SkipSet

  def test_hash_and_identity_kept(self) -> None:
    """A sentinel hashes through 'SentinelMeta' as before and remains
    the one object for its name."""
    self.assertEqual(hash(THIS), hash(THIS))
    self.assertIs(SentinelMeta._getNamedSentinel('THIS'), THIS)
    self.assertEqual(len({THIS, THIS}), 1)
