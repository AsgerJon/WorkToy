"""
PromiseThisReference promises 'THIS[Parent].name', the reference
through which a subclass adds callbacks to an inherited descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import TestCase, skipIf

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import ReferenceConflict, DanglingAlias

if sys.version_info >= (3, 9):
  from ._this_decorator_helpers import makeWatchedSpeaker


class PromiseThisReference(TestCase):
  """
  In the body of a subclass, 'THIS[Parent].volume' stands for the
  descriptor 'volume' that 'Parent' holds, as the subclass will hold it,
  so a callback registered through it serves the subclass, which gets a
  descriptor of its own, while the base keeps its descriptor as it was;
  the parent named may be any class above the one holding the
  descriptor, and a 'Field' takes it as a box does. Decorating
  'Parent.volume' directly from the subclass body registers on the
  parent's own descriptor instead, as that line says. From Python 3.9 it
  is written as
  a decorator, '@THIS[Parent].volume.onSet'; on 3.7 and 3.8 as a call
  after the method in the same body, '_watch =
  THIS[Parent].volume.onSet(_watch)'. A body declaring 'volume' itself
  and decorating 'THIS[Parent].volume' as well raises
  'ReferenceConflict', and a name no class holds raises 'DanglingAlias'.
  Source: the 'THIS' docstring, and the 1.1.0 changelog entries "A
  subclass expands on an inherited descriptor through THIS" and "THIS
  refuses a reference to a name the class body declares itself".
  """

  def makeSpeaker(self) -> type:
    class Speaker(BaseObject):
      volume = AttriBox[int](5)

    return Speaker

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_decorator(self) -> None:
    seen = []
    Speaker = self.makeSpeaker()
    LoudSpeaker = makeWatchedSpeaker(Speaker, seen)
    LoudSpeaker().volume = 7
    Speaker().volume = 3
    self.assertEqual(seen, [7])
    self.assertEqual(LoudSpeaker().volume, 5)

  def test_call(self) -> None:
    seen = []
    Speaker = self.makeSpeaker()

    class LoudSpeaker(Speaker):
      def _watchVolume(self, value: int) -> None:
        seen.append(value)

      _watchVolume = THIS[Speaker].volume.onSet(_watchVolume)

    LoudSpeaker().volume = 7
    Speaker().volume = 3
    self.assertEqual(seen, [7])

  def test_own_descriptor(self) -> None:
    Speaker = self.makeSpeaker()

    class Middle(Speaker):
      pass

    class LoudSpeaker(Middle):
      def _watchVolume(self, value: int) -> None:
        pass

      _watchVolume = THIS[Speaker].volume.onSet(_watchVolume)

    self.assertIn('volume', vars(LoudSpeaker))
    self.assertIsNot(vars(LoudSpeaker)['volume'], vars(Speaker)['volume'])

  def test_parent_descriptor_directly(self) -> None:
    seen = []
    Speaker = self.makeSpeaker()

    class Direct(Speaker):
      def _watchVolume(self, value: int) -> None:
        seen.append(value)

      _watchVolume = Speaker.volume.onSet(_watchVolume)

    self.assertNotIn('volume', vars(Direct))
    Direct().volume = 4
    self.assertEqual(seen, [4])

  def test_field(self) -> None:
    seen = []

    class Circle(BaseObject):
      radius = Field()

      @radius.GET
      def _getRadius(self) -> float:
        return 1.0

    class Watched(Circle):
      def _seen(self) -> None:
        seen.append('read')

      _seen = THIS[Circle].radius.onGet(_seen)

    _ = Watched().radius
    _ = Circle().radius
    self.assertEqual(seen, ['read'])

  def test_conflict(self) -> None:
    Speaker = self.makeSpeaker()
    with self.assertRaises(ReferenceConflict) as context:
      class Booming(Speaker):
        volume = AttriBox[int](11)

        def _watch(self, value: int) -> None:
          pass

        _watch = THIS[Speaker].volume.onSet(_watch)
    e = context.exception
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.className, 'Booming')
    self.assertEqual(e.fieldName, 'volume')
    self.assertEqual(e.holderName, 'Speaker')

  def test_dangling(self) -> None:
    Speaker = self.makeSpeaker()
    with self.assertRaises(DanglingAlias) as context:
      class Quiet(Speaker):
        def _watch(self, value: int) -> None:
          pass

        _watch = THIS[Speaker].mute.onSet(_watch)
    self.assertEqual(context.exception.realName, 'mute')
    self.assertIs(context.exception.owner, Speaker)
