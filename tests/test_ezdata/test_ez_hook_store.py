"""
TestEZHookStore tests how 'EZHook' from 'worktoy.ezdata' decides which
fields need an 'EZStore'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.ezdata import EZData, EZHook, EZStore
from worktoy.mcls import BaseMeta
from . import EzdataTest, Point2D, Labelled, Reporter


class TestEZHookStore(EzdataTest):
  """
  A field whose name a data descriptor further along the resolution
  order would take over receives an 'EZStore'; any other field gets no
  class attribute at all. The tests pin the data-descriptor test, the
  lookup for the first class holding the name, the factory, and the
  two descriptors that clash in practice: a property on a mixin and
  'Object.directory'.
  """

  def test_is_data_descriptor(self) -> None:
    class SetOnly:
      def __set__(self, instance: object, value: object) -> None:
        """Takes writes."""

    class DelOnly:
      def __delete__(self, instance: object) -> None:
        """Takes deletions."""

    class GetOnly:
      def __get__(self, instance: object, owner: type) -> int:
        return 1

    self.assertTrue(EZHook._isDataDescriptor(property()))
    self.assertTrue(EZHook._isDataDescriptor(SetOnly()))
    self.assertTrue(EZHook._isDataDescriptor(DelOnly()))
    self.assertFalse(EZHook._isDataDescriptor(GetOnly()))
    self.assertFalse(EZHook._isDataDescriptor(EZStore('x')))
    self.assertFalse(EZHook._isDataDescriptor(5))

    class Loose(metaclass=BaseMeta):
      @classmethod
      def __class_getattr__(cls, name: str) -> str:
        return 'made up'

    #  A class hook answers 'hasattr' for any name; the decision looks
    #  past it, at what the class defines.
    self.assertTrue(hasattr(Loose, '__set__'))
    self.assertFalse(EZHook._isDataDescriptor(Loose()))
    SetOnly().__set__(None, 1)
    DelOnly().__delete__(None)
    self.assertEqual(GetOnly().__get__(None, GetOnly), 1)

  def test_needs_store(self) -> None:
    order = [Reporter, EZData, Object, object]
    self.assertTrue(EZHook._needsStore('label', order))
    self.assertFalse(EZHook._needsStore('count', order))
    self.assertFalse(EZHook._needsStore('nothing', order))
    self.assertTrue(EZHook._needsStore('directory', [EZData, Object]))
    self.assertFalse(EZHook._needsStore('label', [Labelled, Reporter]))

  def test_store_factory(self) -> None:
    order = [Reporter, EZData, Object, object]
    stores = EZHook.storeFactory(Labelled.__ez_fields__, order)
    self.assertEqual([*stores], ['label'])
    self.assertEqual(Reporter.__dict__['label'].fget(Labelled('t')),
                     'property')
    self.assertIsInstance(stores['label'], EZStore)
    self.assertEqual(EZHook.storeFactory(Point2D.__ez_fields__, [EZData]),
                     {})

  def test_directory_clashes(self) -> None:
    class A(EZData):
      directory = 'here'
      x = 1

    self.assertIsInstance(A.__dict__['directory'], EZStore)
    self.assertNotIn('x', A.__dict__)
    self.assertEqual(A().directory, 'here')
    self.assertEqual(A('there').directory, 'there')
    a = A()
    a.directory = 'moved'
    self.assertEqual(a.__dict__['directory'], 'moved')
    self.assertIsInstance(Point2D().directory, str)

  def test_random_names_need_no_store(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertFalse(EZHook._needsStore(word, [EZData, Object]))
