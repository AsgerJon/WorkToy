"""
PromiseAttriBox promises 'AttriBox' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import threading
from unittest import TestCase

from worktoy.core.sentinels import THIS, OWNER
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, MissingVariable


class PromiseAttriBox(TestCase):
  """
  'x = AttriBox[float](0.0)' in a class body declares a typed attribute
  with a default. The default is built at the first read, for each
  instance apart, by calling the field type with the arguments in the
  parentheses, and kept for later reads; among the arguments, 'THIS'
  becomes the instance and 'OWNER' its class. A lone argument already of
  the field type is deep-copied for each instance instead, and one that
  cannot be copied, as a lock, raises 'TypeError' at the first read,
  while empty parentheses build a new object for each instance. The
  default is built by the constructor of the field type, so
  'AttriBox[int]('3')' holds 3, while an assignment converts only as
  'typeCast' does. A box works in a plain class too.
  'AttriBox[THIS]' types the attribute with the class declaring it. An
  assigned value of the field type is kept as it is, a 'bool' in an
  'AttriBox[int]' staying a 'bool'; any other converts as 'typeCast'
  converts it, or raises 'TypeException' naming the field. After a
  deletion, a read raises 'MissingVariable' until a value is assigned
  again. 'fieldType' gives the field type. A copy of an instance copies
  its values, and a copy of a box is the box itself. Source: the
  'AttriBox' docstring and its example.
  """

  def test_default_built_lazily_per_instance(self) -> None:
    built = []

    class Gear(BaseObject):
      def __init__(self, teeth: int) -> None:
        built.append(teeth)
        self.teeth = teeth

    class Machine(BaseObject):
      gear = AttriBox[Gear](12)

    machine = Machine()
    self.assertEqual(built, [])
    self.assertEqual(machine.gear.teeth, 12)
    self.assertIs(machine.gear, machine.gear)
    self.assertIsNot(Machine().gear, machine.gear)
    self.assertEqual(built, [12, 12])

  def test_placeholders(self) -> None:
    class Part(BaseObject):
      def __init__(self, holder: object, holderClass: type) -> None:
        self.holder, self.holderClass = holder, holderClass

    class Machine(BaseObject):
      part = AttriBox[Part](THIS, OWNER)

    machine = Machine()
    self.assertIs(machine.part.holder, machine)
    self.assertIs(machine.part.holderClass, Machine)

  def test_lone_default_copied(self) -> None:
    class Basket(BaseObject):
      items = AttriBox[list](['apple'])
      nested = AttriBox[list]([['apple']])

    first, second = Basket(), Basket()
    first.items.append('pear')
    first.nested[0].append('pear')
    self.assertEqual(second.items, ['apple'])
    self.assertEqual(second.nested, [['apple']])

  def test_default_built_by_the_constructor(self) -> None:
    class Settings(BaseObject):
      retries = AttriBox[int]('3')

    settings = Settings()
    self.assertEqual(settings.retries, 3)
    with self.assertRaises(TypeException):
      settings.retries = '4'

  def test_new_object_per_instance(self) -> None:
    class Worker(BaseObject):
      done = AttriBox[threading.Event]()

    first, second = Worker(), Worker()
    self.assertIsNot(first.done, second.done)
    first.done.set()
    self.assertFalse(second.done.is_set())

  def test_plain_class(self) -> None:
    class Plain:
      count = AttriBox[int](3)

    plain = Plain()
    plain.count = 4.0
    self.assertEqual(plain.count, 4)
    self.assertIs(type(plain.count), int)

  def test_uncopyable_default(self) -> None:
    lockType = type(threading.Lock())

    class Guarded(BaseObject):
      lock = AttriBox[lockType](threading.Lock())

    with self.assertRaises(TypeError):
      _ = Guarded().lock

  def test_this_type(self) -> None:
    class Node(BaseObject):
      parent = AttriBox[THIS]()

    child, root = Node(), Node()
    child.parent = root
    self.assertIs(child.parent, root)
    with self.assertRaises(TypeException):
      child.parent = 'root'

  def test_assignment(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    class Counter(BaseObject):
      n = AttriBox[int](0)

    point, counter = Point(), Counter()
    point.x = 3
    self.assertEqual(point.x, 3.0)
    self.assertIs(type(point.x), float)
    counter.n = True
    self.assertIs(counter.n, True)
    with self.assertRaises(TypeException) as context:
      point.x = 'three'
    e = context.exception
    self.assertEqual(e.varName, 'x')
    self.assertEqual(e.actualObject, 'three')
    self.assertIs(e.actualType, str)
    self.assertEqual(e.expectedTypes, (float,))

  def test_delete(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    point = Point()
    del point.x
    self.assertFalse(hasattr(point, 'x'))
    with self.assertRaises(MissingVariable):
      _ = point.x
    point.x = 1.5
    self.assertEqual(point.x, 1.5)

  def test_field_type(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    self.assertIs(vars(Point)['x'].fieldType, float)

  def test_copies(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    point = Point()
    point.x = 2.0
    twin = copy.deepcopy(point)
    self.assertIsNot(twin, point)
    self.assertEqual(twin.x, 2.0)
    box = vars(Point)['x']
    self.assertIs(copy.copy(box), box)
    self.assertIs(copy.deepcopy(box), box)
