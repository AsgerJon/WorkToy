"""
TestBaseObject tests 'BaseObject' from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable, Sized

from worktoy.core import Object
from worktoy.dispatch import overload
from worktoy.mcls import BaseMeta, BaseSpace, BaseObject
from . import MclsTest


class TestBaseObject(MclsTest):
  """
  'BaseObject' is an 'Object' built by 'BaseMeta'. Its '__init__'
  refuses arguments as a plain class does when the class defines
  neither '__init__' nor '__new__' of its own, and otherwise keeps them
  for the boxes and initializes the next base without them. The tests
  pin the refusal, the three ways a class takes arguments, the bases
  before and after it, and what the class is.
  """

  def test_arguments_refused_without_initializer(self) -> None:
    class Point(BaseObject):
      pass

    self.assertIsInstance(Point(), Point)
    with self.assertRaises(TypeError) as context:
      Point(1)
    self.assertEqual(str(context.exception), 'Point() takes no arguments')
    with self.assertRaises(TypeError) as context:
      Point(k=1)
    self.assertEqual(str(context.exception), 'Point() takes no arguments')

  def test_own_init_takes_arguments(self) -> None:
    class Point(BaseObject):
      def __init__(self, *args, **kwargs) -> None:
        BaseObject.__init__(self, *args, **kwargs)

    point = Point(1, 2, k=3)
    self.assertEqual(point.getPosArgs(), (1, 2))
    self.assertEqual(point.getKeyArgs(), {'k': 3})

  def test_overloaded_init_takes_arguments(self) -> None:
    class Point(BaseObject):
      @overload(int)
      def __init__(self, n: int) -> None:
        self.n = n

      @overload()
      def __init__(self) -> None:
        self.n = 0

    self.assertEqual(Point(5).n, 5)
    self.assertEqual(Point().n, 0)
    self.assertIsNot(Point.__init__, BaseObject.__init__)

  def test_own_new_takes_arguments(self) -> None:
    class Point(BaseObject):
      def __new__(cls, *args, **kwargs) -> Point:
        return object.__new__(cls)

    point = Point(1, k=2)
    self.assertEqual(point.getPosArgs(), (1,))
    self.assertEqual(point.getKeyArgs(), {'k': 2})

  def test_base_after_is_initialized(self) -> None:
    class Tail:
      def __init__(self) -> None:
        self.tailed = True

    class Point(BaseObject, Tail):
      pass

    self.assertTrue(Point().tailed)
    with self.assertRaises(TypeError) as context:
      Point(1)
    self.assertEqual(str(context.exception), 'Point() takes no arguments')

  def test_base_before_takes_the_arguments(self) -> None:
    class Head:
      def __init__(self, n: int) -> None:
        self.n = n

    class Point(Head, BaseObject):
      pass

    self.assertEqual(Point(3).n, 3)
    with self.assertRaises(TypeError):
      Point()

  def test_what_it_is(self) -> None:
    self.assertIsSubclass(BaseObject, Object)
    self.assertIs(type(BaseObject), BaseMeta)
    self.assertIsInstance(BaseObject.__namespace__, BaseSpace)
    self.assertIs(BaseObject.__metaclass__, BaseMeta)
    self.assertEqual(BaseObject.__keyword_arguments__, {})

    class Point(BaseObject):
      pass

    class Holder:
      p = Point()

    self.assertEqual(Holder.__dict__['p'].getFieldName(), 'p')
    self.assertIs(Holder.__dict__['p'].getFieldOwner(), Holder)

  def test_abc_report(self) -> None:
    class Point(BaseObject):
      pass

    self.assertIsInstance(Point, Iterable)
    self.assertIsInstance(Point, Sized)
    with self.assertRaises(TypeError) as context:
      iter(Point)
    self.assertEqual(str(context.exception),
                     "type object 'Point' is not iterable")
    with self.assertRaises(TypeError) as context:
      len(Point)
    self.assertEqual(str(context.exception),
                     "type object 'Point' has no len()")

  def test_random_names(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      cls = BaseMeta(word, (BaseObject,), {})
      with self.subTest(word=word):
        with self.assertRaises(TypeError) as context:
          cls(1)
        self.assertEqual(str(context.exception),
                         '%s() takes no arguments' % word)
