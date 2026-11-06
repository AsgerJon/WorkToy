"""
TestClassAttributeHooks tests the class hooks of 'AbstractMetaclass' from
'worktoy.mcls' that take over the attributes and the items of a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable
from . import MclsTest, Ledger, Guarded


class TestClassAttributeHooks(MclsTest):
  """
  '__class_setitem__' and '__class_delitem__' subscript a class,
  '__class_getattr__' answers for a missing attribute, and
  '__class_setattr__' and '__class_delattr__' watch the attributes of
  the class. Without them a subscript fails as for a plain class, a
  missing attribute raises 'MissingVariable', and attributes are set
  and deleted as on any class. The tests pin each route.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    Ledger.entries.clear()
    Guarded.writes.clear()
    Guarded.deletes.clear()

  def test_items(self) -> None:
    Ledger['k'] = 1
    self.assertEqual(Ledger.entries, {'k': 1})
    self.assertEqual(Ledger.k, 1)
    del Ledger['k']
    self.assertEqual(Ledger.entries, {})
    with self.assertRaises(KeyError) as context:
      del Ledger['k']
    self.assertEqual(context.exception.args, ('k',))

  def test_items_refused_without_hooks(self) -> None:
    class Plain(BaseObject):
      pass

    with self.assertRaises(TypeError) as context:
      Plain['k'] = 1
    self.assertEqual(str(context.exception),
                     "type object 'Plain' is not subscriptable")
    with self.assertRaises(TypeError) as context:
      del Plain['k']
    self.assertEqual(str(context.exception),
                     "type object 'Plain' does not support item deletion")

  def test_missing_attribute_answered(self) -> None:
    self.assertEqual(Ledger.anything, ('ledger', 'anything'))
    Ledger.entries['named'] = 'entry'
    self.assertEqual(Ledger.named, 'entry')
    self.assertIs(Ledger.entries, Ledger.__dict__['entries'])
    self.assertFalse(hasattr(Ledger, '_private'))
    self.assertTrue(hasattr(Ledger, 'anything'))

  def test_missing_attribute_refused_without_hook(self) -> None:
    class Plain(BaseObject):
      pass

    with self.assertRaises(MissingVariable) as context:
      _ = Plain.missing
    self.assertIs(context.exception.instance, Plain)
    self.assertEqual(context.exception.varName, 'missing')
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'Plain.missing'!")
    self.assertFalse(hasattr(Plain, 'missing'))

  def test_attributes_watched(self) -> None:
    Guarded.x = 1
    self.assertEqual(Guarded.writes, [('x', 1)])
    self.assertEqual(Guarded.__dict__['x'], 1)
    del Guarded.x
    self.assertEqual(Guarded.deletes, ['x'])
    self.assertNotIn('x', Guarded.__dict__)
    hash(Guarded)
    self.assertIn('__class_hash_value__', Guarded.__dict__)
    self.assertEqual(Guarded.writes, [('x', 1)])

  def test_attributes_plain_without_hooks(self) -> None:
    class Plain(BaseObject):
      pass

    Plain.y = 2
    self.assertEqual(Plain.__dict__['y'], 2)
    del Plain.y
    self.assertNotIn('y', Plain.__dict__)
    with self.assertRaises(AttributeError):
      del Plain.y

  def test_random_entries(self) -> None:
    self.randomWord.size = 6
    self.randomInteger.size = 6
    words = self.randomWord.row
    numbers = self.randomInteger.row
    for word, number in zip(words, numbers):
      Ledger[word] = number
    for word, number in zip(words, numbers):
      with self.subTest(word=word):
        self.assertEqual(getattr(Ledger, word), number)
        self.assertIn(word, Ledger)
        del Ledger[word]
        self.assertEqual(getattr(Ledger, word), ('ledger', word))
