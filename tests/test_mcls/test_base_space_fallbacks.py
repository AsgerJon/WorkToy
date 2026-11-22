"""
TestBaseSpaceFallbacks tests the fallbacks a 'BaseSpace' from
'worktoy.mcls' gathers for a name holding several kinds of method.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseMeta, BaseObject, BaseSpace
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.dispatch import DuplicateSignature
from . import MclsTest

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Optional, Type


def _spareBound(self, *args) -> tuple:
  """A fallback a namespace hands out, taking the instance."""
  return 'spare-bound', self, args


def _spareStatic(*args) -> tuple:
  """A fallback a namespace hands out, taking no receiver."""
  return 'spare-static', args


def _spareOther(self, *args) -> None:
  """A second fallback taking the instance, which nothing calls."""


class TestBaseSpaceFallbacks(MclsTest):
  """
  A name holding bound methods beside staticmethods is reached two ways,
  and its fallbacks are two, apart: the instance bound fallback, declared
  as a bound method, for the calls through an instance, and the class
  bound fallback, declared as a staticmethod, for the calls through the
  class. One declared as a classmethod is both. A subclass adds the one
  its base lacks, and a nearer fallback replaces an inherited one that
  the same call could reach. The tests pin what the namespace gathers
  and what each way of calling reaches, for fallbacks a body declares
  and for fallbacks a namespace class hands out.
  """

  @staticmethod
  def _metaOf(spaceClass: Type[BaseSpace]) -> Type[BaseMeta]:
    """Returns a metaclass whose classes are built in a namespace of
    'spaceClass'."""

    class SpareMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> Any:
        return spaceClass(mcls, name, bases, **kwargs)

    return SpareMeta

  def _assertRefused(self, dispatcher: Any, call: Callable) -> None:
    """Asserts that 'call', passing 'None' alone, is refused by
    'dispatcher'."""
    with self.assertRaises(DispatchException) as context:
      call()
    exception = context.exception
    self.assertIs(exception.dispatch, dispatcher)
    self.assertEqual(exception.posArgs, (None,))
    self.assertEqual(exception.keyArgs, {})
    owner = dispatcher.getFieldOwner().__name__
    name = "'%s.%s'" % (owner, dispatcher.getFieldName())
    self.assertIn(name, str(exception))

  def test_subclass_adding_the_other_fallback(self) -> None:
    class Base(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @overload.fallback
      def run(self, *args) -> tuple:
        return 'base-bound', self, args

    class Sub(Base):
      @staticmethod
      @overload.fallback
      def run(*args) -> tuple:
        return 'sub-static', args

    base, sub = Base(), Sub()
    baseBound = Base.__namespace__.getFallbacks()['run'][0]
    subStatic = Sub.__namespace__.getFallbacks()['run'][0]
    self.assertEqual(Base.__namespace__.collectFallbacks('run'), [baseBound])
    self.assertIs(Sub.__namespace__.collectFallback('run'), subStatic)
    self.assertEqual(
        Sub.__namespace__.collectFallbacks('run'), [subStatic, baseBound],
    )
    self.assertEqual(sub.run(1), ('bound', 1))
    self.assertEqual(Sub.run('s'), ('static', 's'))
    self.assertEqual(sub.run(None), ('base-bound', sub, (None,)))
    self.assertEqual(Sub.run(None), ('sub-static', (None,)))
    self.assertEqual(base.run(None), ('base-bound', base, (None,)))
    onClass = Base.__dict__['run'].getClassDispatcher()
    self._assertRefused(onClass, lambda: Base.run(None))

  def test_nearer_fallback_replaces_the_one_it_meets(self) -> None:
    class Base(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @classmethod
      @overload(bytes)
      def run(cls, b: bytes) -> tuple:
        return 'class', cls, b

      @overload.fallback
      def run(self, *args) -> tuple:
        return 'base-bound', self, args

      @staticmethod
      @overload.fallback
      def run(*args) -> tuple:
        return 'base-static', args

    class Bound(Base):
      @overload.fallback
      def run(self, *args) -> tuple:
        return 'sub-bound', self, args

    class Classed(Base):
      @classmethod
      @overload.fallback
      def run(cls, *args) -> tuple:
        return 'sub-class', cls, args

    baseBound, baseStatic = Base.__namespace__.getFallbacks()['run']
    subBound = Bound.__namespace__.getFallbacks()['run'][0]
    subClass = Classed.__namespace__.getFallbacks()['run'][0]
    self.assertEqual(
        Base.__namespace__.collectFallbacks('run'), [baseBound, baseStatic],
    )
    self.assertEqual(
        Bound.__namespace__.collectFallbacks('run'), [subBound, baseStatic],
    )
    self.assertEqual(
        Classed.__namespace__.collectFallbacks('run'), [subClass],
    )
    base, bound, classed = Base(), Bound(), Classed()
    self.assertEqual(base.run(None), ('base-bound', base, (None,)))
    self.assertEqual(Base.run(None), ('base-static', (None,)))
    self.assertEqual(bound.run(None), ('sub-bound', bound, (None,)))
    self.assertEqual(Bound.run(None), ('base-static', (None,)))
    self.assertEqual(bound.run(1), ('bound', 1))
    self.assertEqual(Bound.run(b'b'), ('class', Bound, b'b'))
    self.assertEqual(classed.run(None), ('sub-class', Classed, (None,)))
    self.assertEqual(Classed.run(None), ('sub-class', Classed, (None,)))
    self.assertEqual(classed.run(1), ('bound', 1))
    self.assertEqual(Classed.run('s'), ('static', 's'))

  def test_static_fallback_replaces_inherited_classmethod_one(self) -> None:
    class Base(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @classmethod
      @overload.fallback
      def run(cls, *args) -> tuple:
        return 'base-class', cls, args

    class Sub(Base):
      @staticmethod
      @overload.fallback
      def run(*args) -> tuple:
        return 'sub-static', args

    base, sub = Base(), Sub()
    subStatic = Sub.__namespace__.getFallbacks()['run'][0]
    self.assertEqual(Sub.__namespace__.collectFallbacks('run'), [subStatic])
    self.assertEqual(base.run(None), ('base-class', Base, (None,)))
    self.assertEqual(Base.run(None), ('base-class', Base, (None,)))
    self.assertEqual(Sub.run(None), ('sub-static', (None,)))
    self.assertEqual(Sub.run('s'), ('static', 's'))
    self.assertEqual(sub.run(1), ('bound', 1))
    self._assertRefused(Sub.__dict__['run'], lambda: sub.run(None))

  def test_namespace_handing_out_two_fallbacks(self) -> None:
    class SpareSpace(BaseSpace):
      def collectFallbacks(self, name: str) -> list:
        return [_spareBound, _spareStatic]

      def collectFunctionKinds(self, name: str) -> list:
        kinds = BaseSpace.collectFunctionKinds(self, name)
        return [*kinds, (_spareStatic, staticmethod)]

    class Two(BaseObject, metaclass=self._metaOf(SpareSpace)):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

    two = Two()
    self.assertEqual(two.run(1), ('bound', 1))
    self.assertEqual(Two.run('s'), ('static', 's'))
    self.assertEqual(two.run(None), ('spare-bound', two, (None,)))
    self.assertEqual(Two.run(None), ('spare-static', (None,)))
    onInstance = Two.__dict__['run']
    self.assertIs(onInstance._getFallbackFunction(), _spareBound)
    onClass = onInstance.getClassDispatcher()
    self.assertIs(onClass._getFallbackFunction().__wrapped__, _spareStatic)

  def test_namespace_reimplementing_collect_fallback(self) -> None:
    class BoundSpace(BaseSpace):
      def collectFallback(self, name: str) -> Optional[Callable]:
        return _spareBound

    class StaticSpace(BaseSpace):
      def collectFallback(self, name: str) -> Optional[Callable]:
        return _spareStatic

      def collectFunctionKinds(self, name: str) -> list:
        kinds = BaseSpace.collectFunctionKinds(self, name)
        return [*kinds, (_spareStatic, staticmethod)]

    class OnInstance(BaseObject, metaclass=self._metaOf(BoundSpace)):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload.fallback
      def run(*args) -> tuple:
        return 'own-static', args

    class OnClass(BaseObject, metaclass=self._metaOf(StaticSpace)):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @overload.fallback
      def run(self, *args) -> tuple:
        return 'own-bound', self, args

    class Alone(BaseObject, metaclass=self._metaOf(BoundSpace)):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

    onInstance, onClass, alone = OnInstance(), OnClass(), Alone()
    ownStatic = OnInstance.__namespace__.getFallbacks()['run'][0]
    self.assertEqual(
        OnInstance.__namespace__.collectFallbacks('run'),
        [_spareBound, ownStatic],
    )
    self.assertEqual(
        onInstance.run(None), ('spare-bound', onInstance, (None,)),
    )
    self.assertEqual(OnInstance.run(None), ('own-static', (None,)))
    self.assertEqual(onInstance.run(1), ('bound', 1))
    ownBound = OnClass.__namespace__.getFallbacks()['run'][0]
    self.assertEqual(
        OnClass.__namespace__.collectFallbacks('run'),
        [_spareStatic, ownBound],
    )
    self.assertEqual(onClass.run(None), ('own-bound', onClass, (None,)))
    self.assertEqual(OnClass.run(None), ('spare-static', (None,)))
    self.assertEqual(onClass.run(1), ('bound', 1))
    self.assertEqual(
        Alone.__namespace__.collectFallbacks('run'), [_spareBound],
    )
    self.assertEqual(alone.run(None), ('spare-bound', alone, (None,)))
    self.assertEqual(alone.run(1), ('bound', 1))
    self.assertEqual(Alone.run('s'), ('static', 's'))
    side = Alone.__dict__['run'].getClassDispatcher()
    self._assertRefused(side, lambda: Alone.run(None))

  def test_namespace_handing_out_two_that_meet(self) -> None:
    class CrowdedSpace(BaseSpace):
      def collectFallbacks(self, name: str) -> list:
        return [_spareBound, _spareOther]

    meta = self._metaOf(CrowdedSpace)
    with self.assertRaises(DuplicateSignature) as context:
      class Crowded(BaseObject, metaclass=meta):
        @overload(int)
        def run(self, n: int) -> tuple:
          """Never built: the class statement is refused."""
    self.assertEqual(context.exception.sig, 'fallback')
    self.assertIs(context.exception.existing, _spareBound)
    self.assertIs(context.exception.duplicate, _spareOther)
    self.assertIn('fallback function', str(context.exception))
