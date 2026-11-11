"""
PromiseOverloadRoles promises the stacked, flexible, fallback and
finalizer declarations of '@overload', from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import THIS, ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class PromiseOverloadRoles(TestCase):
  """
  Decorators stack, so one function may serve several signatures.
  'overload.flex(...)' accepts its classes in any order, the function
  receiving them in the declared order, for any number of classes.
  'THIS' in a signature stands for the class being declared.
  'ARGS[int]' last in a signature takes any number of further
  integers, none included, converting as a single entry does, and a
  bare 'ARGS', or '*ARGS', any number of anything; a concrete signature
  matching exactly wins over a variadic one. '@overload.fallback' takes
  every call nothing else accepts, and '@overload.finalize' runs after
  every call, whichever declaration took it and whether or not it
  raised; both receive the positional arguments and the keywords of the
  call, and a subclass inherits both. Source: the docstrings of
  'overload', 'overload.flex', 'overload.fallback', 'overload.finalize',
  'Dispatcher' and 'ARGS', and the 1.1.0 changelog entry "ARGS without a
  type is a tail of any type, with or without the star".
  """

  def test_stacked(self) -> None:
    class Halver(BaseObject):
      @overload(int)
      @overload(float)
      def half(self, value) -> float:
        return value / 2

    self.assertEqual(Halver().half(4), 2.0)
    self.assertEqual(Halver().half(3.0), 1.5)

  def test_flex(self) -> None:
    class Label(BaseObject):
      @overload.flex(str, int)
      def __init__(self, text: str, size: int) -> None:
        self.text, self.size = text, size

    for label in (Label('Title', 12), Label(12, 'Title')):
      with self.subTest():
        self.assertEqual((label.text, label.size), ('Title', 12))

  def test_flex_many(self) -> None:
    class Record(BaseObject):
      @overload.flex(int, str, float, bytes)
      def fields(self, i: int, s: str, x: float, b: bytes) -> tuple:
        return i, s, x, b

    self.assertEqual(Record().fields(b'z', 1.5, 'a', 2), (2, 'a', 1.5, b'z'))

  def test_this(self) -> None:
    class Vector(BaseObject):
      @overload(float, float)
      def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

      @overload(THIS)
      def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    total = Vector(1.0, 2.0) + Vector(3.0, 4.0)
    self.assertEqual((total.x, total.y), (4.0, 6.0))

  def test_args(self) -> None:
    class Summary(BaseObject):
      @overload(str, ARGS[int])
      def total(self, label: str, *numbers: int) -> tuple:
        return label, sum(numbers)

      @overload(ARGS)
      def total(self, *anything) -> int:
        return len(anything)

    self.assertEqual(Summary().total('apples', 1, 2, 3), ('apples', 6))
    self.assertEqual(Summary().total('none'), ('none', 0))
    self.assertEqual(Summary().total(1.5, None), 2)

  def test_concrete_before_tail(self) -> None:
    class Summary(BaseObject):
      @overload(str, ARGS[int])
      def total(self, label: str, *numbers: int) -> str:
        return 'tail'

      @overload(str)
      def total(self, label: str) -> str:
        return 'plain'

    self.assertEqual(Summary().total('none'), 'plain')
    self.assertEqual(Summary().total('some', 1), 'tail')

  def test_tail_converts(self) -> None:
    class Mean(BaseObject):
      @overload(ARGS[float])
      def of(self, *values: float) -> tuple:
        return values

    self.assertEqual(Mean().of(1, 2), (1.0, 2.0))
    self.assertIs(type(Mean().of(1, 2)[0]), float)

  def test_star_args(self) -> None:
    class Anything(BaseObject):
      @overload(int, *ARGS)
      def first(self, head: int, *rest) -> int:
        return head

    self.assertEqual(Anything().first(7, 'a', None), 7)

  def test_fallback_and_finalize(self) -> None:
    log = []

    class Job(BaseObject):
      @overload(int)
      def run(self, n: int) -> int:
        log.append('int')
        if n < 0:
          raise ValueError('negative')
        return n

      @overload.fallback
      def run(self, *args) -> str:
        log.append('fallback')
        return 'fallback'

      @overload.finalize
      def run(self, *args) -> None:
        log.append('finalize')

    job = Job()
    self.assertEqual(job.run(1), 1)
    self.assertEqual(job.run('x'), 'fallback')
    with self.assertRaises(ValueError):
      job.run(-1)
    self.assertEqual(log, ['int', 'finalize', 'fallback', 'finalize',
                           'int', 'finalize'])

  def test_fallback_and_finalize_arguments(self) -> None:
    seen = []

    class Job(BaseObject):
      @overload(int)
      def run(self, n: int, **kwargs) -> int:
        return n

      @overload.fallback
      def run(self, *args, **kwargs) -> str:
        seen.append(('fallback', args, kwargs))
        return 'fallback'

      @overload.finalize
      def run(self, *args, **kwargs) -> None:
        seen.append(('finalize', args, kwargs))

    class NightJob(Job):
      @overload(str)
      def run(self, name: str) -> str:
        return name

    self.assertEqual(NightJob().run(1.5, urgent=True), 'fallback')
    self.assertEqual(seen, [('fallback', (1.5,), {'urgent': True}),
                            ('finalize', (1.5,), {'urgent': True})])
