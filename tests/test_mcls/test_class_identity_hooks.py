"""
TestClassIdentityHooks tests the class hooks of 'AbstractMetaclass' from
'worktoy.mcls' that decide how a class is called, recognizes instances
and subclasses, writes itself and hashes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core._meta_type import _Chill
from worktoy.mcls import AbstractMetaclass, BaseMeta, BaseObject
from . import MclsTest, Factory, Branded


class TestClassIdentityHooks(MclsTest):
  """
  '__class_call__', '__class_instancecheck__', '__class_subclasscheck__',
  '__class_str__', '__class_repr__' and '__class_hash__' take the
  operation over when defined, and the defaults hand over to the next
  metaclass. Without '__class_hash__' a class hashes from its name, its
  declared bases and its metaclass, once, and keeps the value. The tests
  pin each hook on 'Factory' and 'Branded', the defaults on plain
  classes, and the computed hash.
  """

  def test_call(self) -> None:
    self.assertEqual(Factory(1, k=2), ('made', (1,), {'k': 2}))
    self.assertEqual(Factory(), ('made', (), {}))

    class Plain(BaseObject):
      pass

    self.assertIsInstance(Plain(), Plain)

  def test_instance_check(self) -> None:
    self.assertIsInstance(3, Factory)
    self.assertNotIsInstance('3', Factory)
    self.assertTrue(isinstance(True, Factory))

    class Plain(BaseObject):
      pass

    self.assertIsInstance(Plain(), Plain)
    self.assertNotIsInstance(3, Plain)

  def test_subclass_check(self) -> None:
    self.assertIsSubclass(bool, Factory)
    self.assertNotIsSubclass(str, Factory)
    self.assertNotIsSubclass(Factory, Factory)

    class Plain(BaseObject):
      pass

    class Sub(Plain):
      pass

    self.assertIsSubclass(Sub, Plain)
    self.assertNotIsSubclass(Plain, Sub)

  def test_str_and_repr(self) -> None:
    self.assertEqual(str(Branded), 'branded:Branded')
    self.assertEqual(repr(Branded), 'Branded()')
    self.assertEqual('%s' % Branded, 'branded:Branded')

    class Plain(BaseObject):
      pass

    self.assertEqual(str(Plain), 'Plain[metaclass=BaseMeta]')
    self.assertEqual(repr(Plain), 'Plain[metaclass=BaseMeta]')

  def test_hash_hook(self) -> None:
    self.assertEqual(hash(Branded), 42)
    self.assertNotIn('__class_hash_value__', Branded.__dict__)
    self.assertEqual({Branded: 'b'}[Branded], 'b')

  def test_hash_computed_once(self) -> None:
    class Plain(BaseObject):
      pass

    expected = hash(('Plain', 'BaseObject', 'BaseMeta'))
    self.assertNotIn('__class_hash_value__', Plain.__dict__)
    self.assertEqual(hash(Plain), expected)
    self.assertEqual(Plain.__dict__['__class_hash_value__'], expected)
    Plain.__name__ = 'Renamed'
    self.assertEqual(hash(Plain), expected)
    self.assertEqual({Plain: 1}[Plain], 1)

  def test_hash_of_subclass_is_its_own(self) -> None:
    class Plain(BaseObject):
      pass

    class Sub(Plain):
      pass

    self.assertEqual(hash(Sub), hash(('Sub', 'Plain', 'BaseMeta')))
    self.assertNotIn('__class_hash_value__', Plain.__dict__)
    self.assertNotEqual(hash(Sub), hash(Plain))

  def test_hash_leaves_out_chill_and_keeps_plain_bases(self) -> None:
    class Top(metaclass=BaseMeta):
      pass

    class Mixin:
      pass

    class Mixed(Mixin, BaseObject):
      pass

    self.assertEqual(Top.__bases__, (_Chill,))
    self.assertEqual(hash(Top), hash(('Top', 'BaseMeta')))
    self.assertEqual(hash(Mixed), hash(('Mixed', 'Mixin', 'BaseObject',
                                        'BaseMeta')))
    self.assertTrue(AbstractMetaclass._skipHash(_Chill))
    self.assertFalse(AbstractMetaclass._skipHash(Mixin))
    self.assertFalse(AbstractMetaclass._skipHash(BaseObject))
    self.assertTrue(BaseObject._skipHash(_Chill))
    self.assertFalse(Mixed._skipHash(Mixin))

  def test_hash_names_the_metaclass(self) -> None:
    class Meta(BaseMeta):
      pass

    class Plain(BaseObject, metaclass=Meta):
      pass

    self.assertEqual(hash(Plain), hash(('Plain', 'BaseObject', 'Meta')))

  def test_random_names(self) -> None:
    self.randomWord.size = 6
    for word in self.randomWord.row:
      cls = BaseMeta(word, (), {})
      with self.subTest(word=word):
        self.assertEqual(hash(cls), hash((word, 'BaseMeta')))
        self.assertEqual(str(cls), '%s[metaclass=BaseMeta]' % word)
