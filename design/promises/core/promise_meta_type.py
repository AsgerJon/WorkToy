"""
PromiseMetaType promises 'MetaType' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import MetaType


class PromiseMetaType(TestCase):
  """
  'MetaType' is the metaclass every worktoy class and metaclass is built
  on. A class it builds takes keyword arguments in its class statement,
  and a base whose '__init_subclass__' takes one of them receives it,
  without the "takes no keyword arguments" error for the rest. The class
  keeps the namespace its body ran in as '__namespace__', and its
  '__annotations__' are its own, not those of a base. A metaclass a
  project builds on 'MetaType' together with a metaclass of another
  library runs the '__init__' of both, in either order, and a namespace
  of the project's own sees the names of the class body alone. Source:
  the 'MetaType' docstring, and the 1.1.0 changelog entries "A metaclass
  of another library listed after a worktoy one runs its __init__" and
  "A namespace of a project's metaclass sees the class body alone".
  """

  def test_class_keywords(self) -> None:
    class Plugin:
      tags = []

      def __init_subclass__(cls, tag=None, **kwargs) -> None:
        Plugin.tags.append(tag)
        super().__init_subclass__(**kwargs)

    class Thing(Plugin, metaclass=MetaType, tag='reader', unused=True):
      pass

    self.assertEqual(Plugin.tags, ['reader'])
    self.assertIsInstance(Thing, MetaType)

  def test_namespace_kept(self) -> None:
    class Settings(metaclass=MetaType):
      width = 80

    self.assertEqual(Settings.__namespace__['width'], 80)

  def test_own_annotations(self) -> None:
    class Shape(metaclass=MetaType):
      sides: int

    class Square(Shape):
      side: float

    self.assertEqual(list(Shape.__annotations__), ['sides'])
    self.assertEqual(list(Square.__annotations__), ['side'])

  def test_combined_metaclasses(self) -> None:
    class Recorder(type):
      seen = []

      def __init__(cls, name, bases, space, **kwargs) -> None:
        Recorder.seen.append(name)
        super().__init__(name, bases, space, **kwargs)

    class WorktoyFirst(MetaType, Recorder):
      pass

    class RecorderFirst(Recorder, MetaType):
      pass

    class One(metaclass=WorktoyFirst):
      pass

    class Two(metaclass=RecorderFirst):
      pass

    self.assertEqual(Recorder.seen, ['One', 'Two'])

  def test_own_namespace_sees_body_alone(self) -> None:
    class Recording(dict):
      def __init__(self) -> None:
        dict.__init__(self)
        self.bound = []

      def __setitem__(self, key, value) -> None:
        self.bound.append(key)
        dict.__setitem__(self, key, value)

    class RecordingMeta(MetaType):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> Recording:
        return Recording()

    class Plain(metaclass=RecordingMeta):
      x = 1

    bound = Plain.__namespace__.bound
    self.assertIn('x', bound)
    self.assertNotIn('__namespace__', bound)
    self.assertNotIn('__annotations__', bound)
