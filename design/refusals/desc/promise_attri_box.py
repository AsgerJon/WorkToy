"""
RefusedAttriBox holds the refusals that belong with
'design.promises.desc.promise_attri_box'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from unittest import TestCase

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, MissingVariable


class RefusedAttriBox(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A lone argument of the field type that cannot be copied, as a
  lock, raises 'TypeError' at the first read. An assigned value 'typeCast'
  does not convert to the field type raises 'TypeException' naming the field.
  After a deletion, a read raises 'MissingVariable'. Source: the 'AttriBox'
  docstring and its example.
  """

  def test_default_built_by_the_constructor(self) -> None:
    class Settings(BaseObject):
      retries = AttriBox[int]('3')

    settings = Settings()
    with self.assertRaises(Exception) as refused:
      settings.retries = '4'
    self.assertIsInstance(refused.exception, TypeException)

  def test_uncopyable_default(self) -> None:
    lockType = type(threading.Lock())

    class Guarded(BaseObject):
      lock = AttriBox[lockType](threading.Lock())

    with self.assertRaises(Exception) as refused:
      _ = Guarded().lock
    self.assertIsInstance(refused.exception, TypeError)

  def test_this_type(self) -> None:
    class Node(BaseObject):
      parent = AttriBox[THIS]()

    child, root = Node(), Node()
    child.parent = root
    with self.assertRaises(Exception) as refused:
      child.parent = 'root'
    self.assertIsInstance(refused.exception, TypeException)

  def test_assignment(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    class Counter(BaseObject):
      n = AttriBox[int](0)

    point, counter = Point(), Counter()
    point.x = 3
    counter.n = True
    with self.assertRaises(Exception) as refused:
      point.x = 'three'
    self.assertIsInstance(refused.exception, TypeException)

  def test_delete(self) -> None:
    class Point(BaseObject):
      x = AttriBox[float](0.0)

    point = Point()
    del point.x
    with self.assertRaises(Exception) as refused:
      _ = point.x
    self.assertIsInstance(refused.exception, MissingVariable)
