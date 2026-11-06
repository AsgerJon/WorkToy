"""
TestAbstractMetaclassBuild tests how 'AbstractMetaclass' from
'worktoy.mcls' prepares, creates and initializes a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import METACALL
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import AbstractMetaclass, AbstractNamespace
from worktoy.mcls import BaseMeta, BaseSpace, BaseObject
from worktoy.waitaminute.meta import SlotsRefused
from . import MclsTest, LoggingHook, SwappingHook, LoggedSpace, LoggedMeta
from . import ClaimedSpace, ClaimedMeta, Picky, Primed, Roster


class TestAbstractMetaclassBuild(MclsTest):
  """
  '__prepare__' returns the namespace, '__new__' compiles it, creates
  the class and hands it to every hook, and '__init__' calls the class's
  own '__class_init__' and then '__subclasshook__' on each base. A plain
  dictionary given to the metaclass is replayed through a namespace
  first. The tests pin each step on the metaclasses of the folder.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    LoggingHook.log.clear()

  def test_prepare(self) -> None:
    space = AbstractMetaclass.__prepare__('A', (Roster,), tag=1)
    self.assertIs(type(space), AbstractNamespace)
    self.assertIs(space.getMetaclass(), AbstractMetaclass)
    self.assertEqual(space.getClassName(), 'A')
    self.assertEqual(space.getBases(), (Roster,))
    self.assertEqual(space.getKwargs(), {'tag': 1})
    self.assertIsInstance(BaseMeta.__prepare__('A', ()), BaseSpace)
    self.assertIsInstance(LoggedMeta.__prepare__('A', ()), LoggedSpace)

  def test_namespace_class(self) -> None:
    self.assertIs(AbstractMetaclass.getNamespaceClass(), AbstractNamespace)
    self.assertIs(BaseMeta.getNamespaceClass(), BaseSpace)
    self.assertIs(ClaimedMeta.getNamespaceClass(), ClaimedSpace)
    self.assertIs(LoggedMeta.getNamespaceClass(), LoggedSpace)
    self.assertEqual(LoggingHook.log, [('prepare', '_')] * 2)

  def test_namespace_kept(self) -> None:
    class A(metaclass=LoggedMeta):
      pass

    self.assertIs(A.getNamespace(), A.__dict__['__namespace__'])
    self.assertIsInstance(A.getNamespace(), LoggedSpace)
    self.assertEqual(A.getNamespace().getClassName(), 'A')
    self.assertIs(A.__namespace__, A.getNamespace())

  def test_phases_in_order(self) -> None:
    class A(metaclass=LoggedMeta):
      x = 1
      y = x

    phases = [entry[:2] for entry in LoggingHook.log]
    expected = [
      ('prepare', 'A'), ('get', '__name__'), ('set', '__module__'),
      ('set', '__qualname__'),
    ]
    self.assertEqual(phases[:4], expected)
    self.assertIn(('set', 'x'), phases)
    self.assertIn(('get', 'x'), phases)
    self.assertIn(('set', 'y'), phases)
    tail = [('pre', 'A'), ('post', 'A'), ('new', 'A')]
    self.assertEqual(phases[-3:], tail)
    self.assertLess(phases.index(('set', 'y')), phases.index(('pre', 'A')))

  def test_plain_dictionary_replayed(self) -> None:
    def f(self, n: int) -> str:
      return 'int'

    A = BaseMeta('A', (), {'x': 1, 'f': overload(int)(f)})
    self.assertEqual(A.x, 1)
    self.assertIsInstance(A.__namespace__, BaseSpace)
    self.assertIsInstance(A.__dict__['f'], Dispatcher)
    self.assertEqual(A().f(1), 'int')
    self.assertIs(A.__dict__['__class_len__'], METACALL)
    with self.assertRaises(SlotsRefused) as context:
      BaseMeta('B', (), {'__slots__': ()})
    self.assertEqual(context.exception.className, 'B')
    self.assertIn("The class body of 'B' binds '__slots__'",
                  str(context.exception))

  def test_hook_may_replace_the_class(self) -> None:
    class Stub:
      pass

    SwappingHook.replacement = Stub
    try:
      class Decoy(metaclass=ClaimedMeta):
        pass
    finally:
      SwappingHook.replacement = None
    self.assertIs(Decoy, Stub)

    class Decoy(metaclass=ClaimedMeta):
      pass

    self.assertIs(type(Decoy), ClaimedMeta)
    self.assertEqual(Decoy.__name__, 'Decoy')

  def test_class_init_called(self) -> None:
    Primed.inits.clear()

    class A(Primed, tag=1):
      pass

    self.assertEqual(len(Primed.inits), 1)
    cls, name, bases, space, kwargs = Primed.inits[0]
    self.assertIs(cls, A)
    self.assertEqual(name, 'A')
    self.assertEqual(bases, (Primed,))
    self.assertIs(space, A.__namespace__)
    self.assertEqual(kwargs, {'tag': 1})
    self.assertIs(BaseObject.__class_init__, METACALL)

  def test_subclass_hook_sees_every_subclass(self) -> None:
    Picky.seen.clear()

    class Good(Picky):
      pass

    class Pair(Roster, Good):
      pass

    self.assertEqual(Picky.seen, ['Good', 'Pair'])
    with self.assertRaises(TypeError) as context:
      class BadOne(Picky):
        pass

    self.assertEqual(Picky.seen, ['Good', 'Pair', 'BadOne'])
    self.assertEqual(str(context.exception), 'BadOne is refused by Picky')
    self.assertIs(AbstractMetaclass._notifySubclassHook(Good), Good)
    self.assertIs(AbstractMetaclass._notifySubclassHook(Good, Picky), Good)
    self.assertEqual(Picky.seen[-1], 'Good')
    count = len(Picky.seen)
    self.assertIs(Good._notifySubclassHook(Good), Good)
    self.assertEqual(len(Picky.seen), count)

  def test_refused_before_the_body(self) -> None:
    with self.assertRaises(ValueError) as context:
      class Refused(metaclass=ClaimedMeta):
        """Never runs: the namespace refuses the class first."""

    self.assertEqual(str(context.exception), 'refused before the body ran')

    self.assertEqual(LoggingHook.log, [('prepare', 'Refused')])

  def test_random_classes_by_call(self) -> None:
    self.randomWord.size = 5
    self.randomInteger.size = 5
    for word, number in zip(self.randomWord.row, self.randomInteger.row):
      cls = BaseMeta(word, (BaseObject,), {'value': number})
      with self.subTest(word=word):
        self.assertEqual(cls.__name__, word)
        self.assertEqual(cls.value, number)
        self.assertEqual(cls().value, number)
        self.assertEqual(cls.__namespace__.getClassName(), word)
