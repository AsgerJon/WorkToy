"""
TestAbstractNamespaceCompile tests the compilation of 'AbstractNamespace'
from 'worktoy.mcls' and the reading of compiled namespaces.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.mcls import AbstractNamespace, BaseMeta, BaseSpace, BaseObject
from worktoy.waitaminute import TypeException
from . import MclsTest, LoggingHook, LoggedSpace, LoggedMeta


class TestAbstractNamespaceCompile(MclsTest):
  """
  'compile' assembles the dictionary the class is created from: the
  defaults of the hooks, the names of the body over them, the
  transformations of the hooks, and the three entries naming the
  metaclass, the namespace and the keywords. The compiled dictionary is
  kept, so a subclass reads what its bases declared through
  'getMROSpace'. The tests pin each step, the refusals, and the merged
  reading.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    LoggingHook.log.clear()

  def test_pre_compile(self) -> None:
    space = LoggedSpace(LoggedMeta, 'A', ())
    fresh = space.preCompile()
    self.assertEqual(fresh['hookDefault'], 'pre')
    self.assertIn('__class_len__', fresh)
    given = {'x': 1}
    self.assertIs(space.preCompile(given), given)
    self.assertEqual(given['x'], 1)
    self.assertEqual(given['hookDefault'], 'pre')
    with self.assertRaises(TypeException) as context:
      space.preCompile(5)
    self.assertEqual(context.exception.varName, 'namespace')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (dict,))
    self.assertIn("'namespace'", str(context.exception))
    self.assertIn("'dict'", str(context.exception))

  def test_post_compile(self) -> None:
    space = LoggedSpace(LoggedMeta, 'A', ())
    given = {'hookFinal': 'body'}
    self.assertIs(space.postCompile(given), given)
    self.assertEqual(given['hookFinal'], 'post')
    self.assertEqual(LoggingHook.log[-1], ('post', 'A'))

  def test_compile(self) -> None:
    space = LoggedSpace(LoggedMeta, 'A', (), tag=1)
    space['x'] = 1
    space['hookDefault'] = 'body'
    space['hookFinal'] = 'body'
    compiled = space.compile()
    self.assertEqual(compiled['x'], 1)
    self.assertEqual(compiled['hookDefault'], 'body')
    self.assertEqual(compiled['hookFinal'], 'post')
    self.assertIs(compiled['__metaclass__'], LoggedMeta)
    self.assertIs(compiled['__namespace__'], space)
    self.assertEqual(compiled['__keyword_arguments__'], {'tag': 1})
    self.assertIs(object.__getattribute__(space, '__compiled_space__'),
                  compiled)
    phases = [entry[0] for entry in LoggingHook.log]
    self.assertEqual(phases[-2:], ['pre', 'post'])
    given = {'y': 2}
    self.assertIs(space.compile(given), given)
    self.assertEqual(given['x'], 1)

  def test_compiled_entries_reach_the_class(self) -> None:
    class A(metaclass=LoggedMeta, tag=1):
      hookFinal = 'body'

    self.assertEqual(A.hookDefault, 'pre')
    self.assertEqual(A.hookFinal, 'post')
    self.assertIs(A.__metaclass__, LoggedMeta)
    self.assertIs(A.__dict__['__namespace__'], A.getNamespace())
    self.assertEqual(A.__dict__['__keyword_arguments__'], {'tag': 1})
    self.assertIsInstance(A.__namespace__, LoggedSpace)

  def test_mro_space_nearest_first(self) -> None:
    class Base(BaseObject):
      tag = 'base'
      only = 'base'

    class Sub(Base):
      tag = 'sub'

    class Plain:
      tag = 'plain'

    space = BaseSpace(BaseMeta, 'X', (Plain, Sub))
    merged = space.getMROSpace()
    self.assertEqual(merged['tag'], ['sub', 'base'])
    self.assertEqual(merged['only'], ['base'])
    self.assertEqual(merged['__namespace__'][:2],
                     [Sub.__namespace__, Base.__namespace__])
    self.assertEqual(len(merged['__metaclass__']), 3)
    self.assertNotIn('__skip_hash__', merged)
    self.assertEqual(BaseSpace(BaseMeta, 'X', ()).getMROSpace(), {})

  def test_mro_space_passes_over_plain_namespaces(self) -> None:
    self.assertIsInstance(Object.__dict__['__namespace__'], dict)
    self.assertNotIsInstance(Object.__dict__['__namespace__'],
                             AbstractNamespace)
    space = BaseSpace(BaseMeta, 'X', (Object,))
    self.assertEqual(space.getMROSpace(), {})

  def test_random_bodies(self) -> None:
    self.randomWord.size = 5
    self.randomInteger.size = 5
    words = self.randomWord.row
    numbers = self.randomInteger.row
    space = BaseSpace(BaseMeta, 'X', ())
    for word, number in zip(words, numbers):
      space[word] = number
    compiled = space.compile()
    for word, number in zip(words, numbers):
      with self.subTest(word=word):
        self.assertEqual(compiled[word], number)
