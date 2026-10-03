"""
TestClassKeywords tests that a class deriving from a 'worktoy' metaclass
takes class keywords whether or not it is based on 'Object'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.work_test import BaseTest
from .. import MCLSTest


class TestClassKeywords(MCLSTest):
  """
  TestClassKeywords tests the class keywords of classes built by a
  'worktoy' metaclass. The namespace records them and its hooks read them,
  as 'trustMeBro' is read by 'NamespaceHook', '__class_init__' receives
  them, and so does the '__init_subclass__' of a base defining one.
  'MetaType' keeps them only from 'object.__init_subclass__', which refuses
  every keyword, so a class deriving from a 'worktoy' metaclass without
  being based on 'Object', such as a 'KeeFlags' class, a 'BaseTest' class
  or a class declaring only 'metaclass=BaseMeta', takes the keywords as a
  'BaseObject' does.
  """

  def test_bare_base_meta(self) -> None:
    """
    Testing that a class declaring only 'metaclass=BaseMeta' takes
    'trustMeBro=True' and may then define '__del__'.
    """

    class Plain(metaclass=BaseMeta, trustMeBro=True):
      __del__ = lambda self: None

    self.assertIn('__del__', Plain.__dict__)

  def test_strict_mro_keyword(self) -> None:
    """
    Testing that a class declaring only 'metaclass=BaseMeta' takes the
    '_strictMRO' keyword its namespace reads.
    """

    class Strict(metaclass=BaseMeta, _strictMRO=True):
      pass

    self.assertEqual(Strict.__name__, 'Strict')

  def test_kee_flags(self) -> None:
    """
    Testing that a 'KeeFlags' class takes 'trustMeBro=True', as the
    'DelException' raised for its '__del__' advises, and still builds its
    members.
    """

    class Perm(KeeFlags, trustMeBro=True):
      READ = KeeFlag()
      WRITE = KeeFlag()
      __del__ = lambda self: None

    self.assertIn('__del__', Perm.__dict__)
    self.assertEqual(len(Perm), 4)

  def test_base_test(self) -> None:
    """
    Testing that a 'BaseTest' class takes 'trustMeBro=True'.
    """

    class Tested(BaseTest, trustMeBro=True):
      __del__ = lambda self: None

    self.assertIn('__del__', Tested.__dict__)

  def test_class_init_without_object(self) -> None:
    """
    Testing that '__class_init__' receives the class keywords of a class
    not based on 'Object', as it does for a 'BaseObject'.
    """

    class Plain(metaclass=BaseMeta, flavour='vanilla'):
      __received__ = None

      @classmethod
      def __class_init__(cls, name, bases, space, **kwargs) -> None:
        type.__setattr__(cls, '__received__', dict(kwargs))

    self.assertEqual(Plain.__received__, {'flavour': 'vanilla'})

  def test_namespace_records_keywords(self) -> None:
    """
    Testing that the namespace records the class keywords, where its hooks
    and the class read them.
    """

    class Recorded(BaseObject, flavour='vanilla'):
      pass

    space = Recorded.__namespace__
    self.assertEqual(space.getKwargs(), {'flavour': 'vanilla'})
    self.assertEqual(Recorded.__keyword_arguments__, {'flavour': 'vanilla'})

  def test_init_subclass_receives_keywords(self) -> None:
    """
    Testing that a base defining its own '__init_subclass__' still
    receives the class keywords, with or without 'Object' among the bases
    after it, and when the base defining it is further up the method
    resolution order.
    """

    class Watcher:
      __received__ = None

      def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__()
        cls.__received__ = dict(kwargs)

    class Middle(Watcher):
      pass

    class Watched(Watcher, metaclass=BaseMeta, flavour='vanilla'):
      pass

    class WatchedObject(Watcher, BaseObject, flavour='vanilla'):
      pass

    class WatchedDeep(Middle, metaclass=BaseMeta, flavour='vanilla'):
      pass

    self.assertEqual(Watched.__received__, {'flavour': 'vanilla'})
    self.assertEqual(WatchedObject.__received__, {'flavour': 'vanilla'})
    self.assertEqual(WatchedDeep.__received__, {'flavour': 'vanilla'})

  def test_object_takes_keywords(self) -> None:
    """
    Testing that a class based on 'Object' and built by 'MetaType' takes
    a class keyword, since none of its bases has an '__init_subclass__' to
    hand it to 'object'; see 'MetaType.takesKeywords'.
    """

    class Desc(Object, flavour='vanilla'):
      pass

    self.assertEqual(Desc.__name__, 'Desc')
