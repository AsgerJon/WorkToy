"""
TestOverloadMixedKinds tests one overloaded name declared as several
kinds of method: bound methods, classmethods and staticmethods.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import MethodType, FunctionType

from worktoy.core.sentinels import THIS, ARGS
from worktoy.dispatch import overload, Dispatcher, TypeSig, PermuterMethod
from worktoy.mcls import BaseObject
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.desc import WriteOnceError
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.dispatch import DuplicateSignature
from worktoy.waitaminute.meta import MixedMethodKind
from . import DispatchTest


def _static(n: int) -> tuple:
  """A function taking no receiver, as a staticmethod does."""
  return 'static', n


def _class(cls: type, n: int) -> tuple:
  """A function taking the class, as a classmethod does."""
  return 'class', cls, n


def _bound(self, n: int) -> tuple:
  """A function taking the instance, as a bound method does."""
  return 'bound', self, n


class TestOverloadMixedKinds(DispatchTest):
  """
  One overloaded name may hold bound methods, classmethods and
  staticmethods together. Through the class the classmethods and the
  staticmethods are tried and the bound methods are not considered.
  Through an instance the bound methods and the classmethods are tried,
  and the staticmethods are not considered when the name has a bound
  method. The overload that matches receives the instance if it is
  bound, the class if it is a classmethod, and nothing ahead of the
  arguments if it is static. A name with bound methods and another kind
  holds two dispatchers, one for each way of reaching it. The tests pin
  each mix, the same signature on both sides, variadic and flexible
  declarations, the fallback and the finalizer, what a subclass keeps
  and hides, and the two dispatchers by hand.
  """

  def _assertRefused(self, dispatcher: Dispatcher, call, *posArgs) -> None:
    """Asserts that 'call' is refused by 'dispatcher', with the positional
    arguments 'posArgs' and no keyword."""
    with self.assertRaises(DispatchException) as context:
      call()
    exception = context.exception
    self.assertIs(exception.dispatch, dispatcher)
    self.assertEqual(exception.posArgs, posArgs)
    self.assertEqual(exception.keyArgs, {})
    owner = dispatcher.getFieldOwner().__name__
    name = "'%s.%s'" % (owner, dispatcher.getFieldName())
    self.assertIn(name, str(exception))

  def test_static_and_bound_of_one_signature(self) -> None:
    class Foo(BaseObject):
      @staticmethod
      @overload(int)
      def bar(value: int) -> tuple:
        return 'staticBar', value

      @overload(int)
      def bar(self, value: int) -> tuple:
        return 'boundBar', self, value

    foo = Foo()
    self.assertEqual(Foo.bar(69), ('staticBar', 69))
    self.assertEqual(foo.bar(420), ('boundBar', foo, 420))

  def test_static_and_bound(self) -> None:
    class File(BaseObject):
      def __init__(self, name: str) -> None:
        self.name = name

      @overload()
      def exists(self) -> tuple:
        """Tells of the file of this object."""
        return 'bound', self.name

      @staticmethod
      @overload(str)
      def exists(name: str) -> tuple:
        """Tells of the file by a name."""
        return 'static', name

    file = File('readme')
    onInstance = File.__dict__['exists']
    onClass = onInstance.getClassDispatcher()
    self.assertEqual(file.exists(), ('bound', 'readme'))
    self.assertEqual(File.exists('notes'), ('static', 'notes'))
    self._assertRefused(onInstance, lambda: file.exists('notes'), 'notes')
    self._assertRefused(onClass, lambda: File.exists(file), file)
    self._assertRefused(onClass, lambda: File.exists())

  def test_two_dispatchers(self) -> None:
    class Foo(BaseObject):
      @overload(int)
      def bar(self, value: int) -> None:
        """The bound one."""

      @staticmethod
      @overload(str)
      def bar(value: str) -> None:
        """The static one."""

      @overload(int)
      def plain(self, value: int) -> None:
        """Bound alone."""

    foo = Foo()
    onInstance = Foo.__dict__['bar']
    onClass = onInstance.getClassDispatcher()
    self.assertIsInstance(onInstance, Dispatcher)
    self.assertIsInstance(onClass, Dispatcher)
    self.assertIsNot(onClass, onInstance)
    self.assertIsNone(onInstance.getMethodKind())
    self.assertIs(onClass.getMethodKind(), staticmethod)
    self.assertIsNone(onClass.getClassDispatcher())
    self.assertIs(onClass.getFieldOwner(), Foo)
    self.assertEqual(onClass.getFieldName(), 'bar')
    self.assertEqual(
        [sig for sig, _ in onInstance._getSigFuncList()], [TypeSig(int)],
    )
    self.assertEqual(
        [sig for sig, _ in onClass._getSigFuncList()], [TypeSig(str)],
    )
    self.assertIsInstance(foo.bar, MethodType)
    self.assertIs(foo.bar.__self__, foo)
    self.assertEqual(foo.bar.__doc__, 'The bound one.')
    self.assertIsInstance(Foo.bar, MethodType)
    self.assertIs(Foo.bar.__self__, Foo)
    self.assertEqual(Foo.bar.__doc__, 'The static one.')
    for method in (foo.bar, Foo.bar):
      self.assertEqual(method.__name__, 'bar')
      self.assertEqual(method.__qualname__, 'Foo.bar')
    self.assertIsNone(Foo.__dict__['plain'].getClassDispatcher())
    self.assertIsInstance(Foo.plain, FunctionType)

  def test_static_and_classmethod(self) -> None:
    class Maker(BaseObject):
      @staticmethod
      @overload(int)
      def make(n: int) -> tuple:
        return 'static', n

      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

    maker = Maker()
    dispatcher = Maker.__dict__['make']
    self.assertIs(dispatcher.getMethodKind(), classmethod)
    self.assertIsNone(dispatcher.getClassDispatcher())
    self.assertEqual(Maker.make(1), ('static', 1))
    self.assertEqual(Maker.make('a'), ('class', Maker, 'a'))
    self.assertEqual(maker.make(1), ('static', 1))
    self.assertEqual(maker.make('a'), ('class', Maker, 'a'))
    self._assertRefused(dispatcher, lambda: Maker.make(None), None)
    self._assertRefused(dispatcher, lambda: maker.make(None), None)

  def test_classmethod_then_static(self) -> None:
    class Maker(BaseObject):
      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

      @staticmethod
      @overload(int)
      def make(n: int) -> tuple:
        return 'static', n

    self.assertIs(Maker.__dict__['make'].getMethodKind(), classmethod)
    self.assertEqual(Maker.make(1), ('static', 1))
    self.assertEqual(Maker().make('a'), ('class', Maker, 'a'))

  def test_classmethod_and_bound(self) -> None:
    class Color(BaseObject):
      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

      @overload(int)
      def make(self, shade: int) -> tuple:
        return 'bound', self, shade

    red = Color()
    onInstance = Color.__dict__['make']
    onClass = onInstance.getClassDispatcher()
    self.assertIsNone(onInstance.getMethodKind())
    self.assertIs(onClass.getMethodKind(), classmethod)
    self.assertEqual(Color.make('red'), ('class', Color, 'red'))
    self.assertEqual(red.make(3), ('bound', red, 3))
    self.assertEqual(red.make('blue'), ('class', Color, 'blue'))
    self._assertRefused(onClass, lambda: Color.make(3), 3)
    self._assertRefused(onInstance, lambda: red.make(None), None)

  def test_all_three(self) -> None:
    class All(BaseObject):
      @overload(int)
      def f(self, n: int) -> tuple:
        return 'bound', self, n

      @classmethod
      @overload(str)
      def f(cls, s: str) -> tuple:
        return 'class', cls, s

      @staticmethod
      @overload(int)
      def f(n: int) -> tuple:
        return 'static', n

      @staticmethod
      @overload(float)
      def f(x: float) -> tuple:
        return 'static', x

    one = All()
    onInstance = All.__dict__['f']
    onClass = onInstance.getClassDispatcher()
    self.assertIsNone(onInstance.getMethodKind())
    self.assertIs(onClass.getMethodKind(), classmethod)
    self.assertEqual(one.f(1), ('bound', one, 1))
    self.assertEqual(All.f(1), ('static', 1))
    self.assertEqual(one.f('s'), ('class', All, 's'))
    self.assertEqual(All.f('s'), ('class', All, 's'))
    self.assertEqual(All.f(1.5), ('static', 1.5))
    self._assertRefused(onInstance, lambda: one.f(1.5), 1.5)

  def test_same_signature_where_two_kinds_meet(self) -> None:
    with self.assertRaises(DuplicateSignature) as context:
      class Meets(BaseObject):
        @staticmethod
        @overload(int)
        def f(n: int) -> None:
          """The static one."""

        @classmethod
        @overload(int)
        def f(cls, n: int) -> None:
          """The classmethod."""

    exception = context.exception
    self.assertEqual(exception.sig, TypeSig(int))
    self.assertEqual(exception.existing.__doc__, 'The static one.')
    self.assertEqual(exception.duplicate.__doc__, 'The classmethod.')
    self.assertIn('already has a function registered', str(exception))
    with self.assertRaises(DuplicateSignature) as context:
      class Meets(BaseObject):
        @overload(int)
        def f(self, n: int) -> None:
          """The bound one."""

        @classmethod
        @overload(int)
        def f(cls, n: int) -> None:
          """The classmethod."""

    exception = context.exception
    self.assertEqual(exception.sig, TypeSig(int))
    self.assertEqual(exception.existing.__doc__, 'The bound one.')
    self.assertEqual(exception.duplicate.__doc__, 'The classmethod.')
    self.assertIn('already has a function registered', str(exception))

  def test_variadic(self) -> None:
    class Sum(BaseObject):
      @overload(ARGS[int])
      def total(self, *numbers) -> tuple:
        return 'bound', self, numbers

      @staticmethod
      @overload(ARGS[int])
      def total(*numbers) -> tuple:
        return 'static', numbers

      @classmethod
      @overload(str, ARGS[str])
      def total(cls, first: str, *rest) -> tuple:
        return 'class', cls, first, rest

    one = Sum()
    self.assertEqual(one.total(1, 2), ('bound', one, (1, 2)))
    self.assertEqual(Sum.total(1, 2), ('static', (1, 2)))
    self.assertEqual(one.total(), ('bound', one, ()))
    self.assertEqual(Sum.total(), ('static', ()))
    self.assertEqual(one.total('a', 'b'), ('class', Sum, 'a', ('b',)))
    self.assertEqual(Sum.total('a'), ('class', Sum, 'a', ()))

  def test_flexible_of_two(self) -> None:
    class Tag(BaseObject):
      @classmethod
      @overload.flex(int, str)
      def mark(cls, n: int, s: str) -> tuple:
        return 'class', cls, n, s

      @staticmethod
      @overload.flex(float, bytes)
      def mark(x: float, b: bytes) -> tuple:
        return 'static', x, b

      @overload.flex(int, float)
      def mark(self, n: int, x: float) -> tuple:
        return 'bound', self, n, x

    tag = Tag()
    onInstance = Tag.__dict__['mark']
    self.assertEqual(tag.mark('a', 1), ('class', Tag, 1, 'a'))
    self.assertEqual(Tag.mark(1, 'a'), ('class', Tag, 1, 'a'))
    self.assertEqual(Tag.mark(b'b', 1.5), ('static', 1.5, b'b'))
    self.assertEqual(tag.mark(1.5, 2), ('bound', tag, 2, 1.5))
    refused = lambda: tag.mark(None, b'b')
    self._assertRefused(onInstance, refused, None, b'b')

  def test_flexible_of_four(self) -> None:
    class Crate(BaseObject):
      @staticmethod
      @overload.flex(int, str, float, bytes)
      def pack(n: int, s: str, x: float, b: bytes) -> tuple:
        return 'static', n, s, x, b

      @classmethod
      @overload.flex(int, str, float, bool)
      def pack(cls, n: int, s: str, x: float, flag: bool) -> tuple:
        return 'class', cls, n, s, x, flag

      @overload()
      def pack(self) -> tuple:
        return 'bound', self

    crate = Crate()
    onInstance = Crate.__dict__['pack']
    packed = ('static', 1, 's', 1.5, b'b')
    flagged = ('class', Crate, 1, 's', 1.5, True)
    self.assertEqual(Crate.pack(b'b', 1.5, 's', 1), packed)
    self.assertEqual(Crate.pack(True, 1.5, 's', 1), flagged)
    self.assertEqual(crate.pack(1.5, True, 1, 's'), flagged)
    self.assertEqual(crate.pack(), ('bound', crate))
    refused = lambda: crate.pack(b'b', 1.5, 's', None)
    self._assertRefused(onInstance, refused, b'b', 1.5, 's', None)

  def test_flexible_of_four_of_the_same_classes(self) -> None:
    class Crate(BaseObject):
      @overload.flex(int, str, float, bytes)
      def pack(self, n: int, s: str, x: float, b: bytes) -> tuple:
        return 'bound', self, n, s, x, b

      @staticmethod
      @overload.flex(bytes, float, str, int)
      def pack(b: bytes, x: float, s: str, n: int) -> tuple:
        return 'static', b, x, s, n

    class Sub(Crate):
      """Declares nothing at the name."""

    for cls in (Crate, Sub):
      crate = cls()
      bound = ('bound', crate, 1, 's', 1.5, b'b')
      self.assertEqual(crate.pack(1.5, b'b', 1, 's'), bound)
      static = ('static', b'b', 1.5, 's', 1)
      self.assertEqual(cls.pack(1, 's', 1.5, b'b'), static)

  def test_mixed_method_kind_by_hand(self) -> None:
    with self.assertRaises(MixedMethodKind) as context:
      raise MixedMethodKind('Owner', 'f', (None, classmethod))
    exception = context.exception
    self.assertEqual(exception.className, 'Owner')
    self.assertEqual(exception.overloadName, 'f')
    self.assertEqual(exception.kinds, (None, classmethod))
    text = "'Owner.f' is declared as an instance method and as a"
    self.assertIn(text, str(exception))
    self.assertIn('Functions of different kinds may share', str(exception))

  def test_fallback_and_finalizer_bound(self) -> None:
    calls = []

    class Loud(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @overload.fallback
      def run(self, *args) -> tuple:
        return 'fallback', self, args

      @overload.finalize
      def run(self, *args) -> None:
        calls.append((self, args))

    loud = Loud()
    onClass = Loud.__dict__['run'].getClassDispatcher()
    self.assertEqual(loud.run(1), ('bound', 1))
    self.assertEqual(calls, [(loud, (1,))])
    self.assertEqual(loud.run('s'), ('fallback', loud, ('s',)))
    self.assertEqual(calls[-1], (loud, ('s',)))
    self.assertEqual(Loud.run('s'), ('static', 's'))
    self._assertRefused(onClass, lambda: Loud.run(None), None)
    self.assertEqual(len(calls), 2)

  def test_fallback_and_finalizer_static(self) -> None:
    calls = []

    class Quiet(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @staticmethod
      @overload.fallback
      def run(*args) -> tuple:
        return 'fallback', args

      @staticmethod
      @overload.finalize
      def run(*args) -> None:
        calls.append(args)

    quiet = Quiet()
    onInstance = Quiet.__dict__['run']
    self.assertEqual(Quiet.run('s'), ('static', 's'))
    self.assertEqual(calls, [('s',)])
    self.assertEqual(Quiet.run(None), ('fallback', (None,)))
    self.assertEqual(calls[-1], (None,))
    self.assertEqual(quiet.run(1), ('bound', 1))
    self._assertRefused(onInstance, lambda: quiet.run('s'), 's')
    self.assertEqual(len(calls), 2)

  def test_fallback_and_finalizer_classmethod(self) -> None:
    calls = []

    class Both(BaseObject):
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
        return 'fallback', cls, args

      @classmethod
      @overload.finalize
      def run(cls, *args) -> None:
        calls.append((cls, args))

    both = Both()
    self.assertEqual(both.run(1), ('bound', 1))
    self.assertEqual(calls, [(Both, (1,))])
    self.assertEqual(both.run('s'), ('fallback', Both, ('s',)))
    self.assertEqual(calls[-1], (Both, ('s',)))
    self.assertEqual(Both.run('s'), ('static', 's'))
    self.assertEqual(calls[-1], (Both, ('s',)))
    self.assertEqual(Both.run(1), ('fallback', Both, (1,)))
    self.assertEqual(calls[-1], (Both, (1,)))
    self.assertEqual(len(calls), 4)

  def test_fallback_and_finalizer_of_different_kinds(self) -> None:
    calls = []

    class Split(BaseObject):
      @overload(int)
      def run(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(str)
      def run(s: str) -> tuple:
        return 'static', s

      @overload.fallback
      def run(self, *args) -> tuple:
        return 'fallback', self, args

      @staticmethod
      @overload.finalize
      def run(*args) -> None:
        calls.append(args)

    split = Split()
    onClass = Split.__dict__['run'].getClassDispatcher()
    self.assertEqual(split.run(1), ('bound', 1))
    self.assertEqual(split.run(None), ('fallback', split, (None,)))
    self.assertEqual(calls, [])
    self.assertEqual(Split.run('s'), ('static', 's'))
    self.assertEqual(calls, [('s',)])
    self._assertRefused(onClass, lambda: Split.run(None), None)
    self.assertEqual(calls, [('s',), (None,)])

  def test_this_on_both_sides(self) -> None:
    class Node(BaseObject):
      @overload(THIS)
      def link(self, other: Node) -> tuple:
        return 'bound', self, other

      @staticmethod
      @overload(THIS, THIS)
      def link(first: Node, second: Node) -> tuple:
        return 'static', first, second

    a, b = Node(), Node()
    onInstance = Node.__dict__['link']
    onClass = onInstance.getClassDispatcher()
    self.assertEqual(a.link(b), ('bound', a, b))
    self.assertEqual(Node.link(a, b), ('static', a, b))
    self._assertRefused(onInstance, lambda: a.link(a, b), a, b)
    self._assertRefused(onClass, lambda: Node.link(a), a)

  def test_subclass_declaring_nothing(self) -> None:
    class Foo(BaseObject):
      @overload(int)
      def bar(self, n: int) -> tuple:
        return 'bound', self, n

      @staticmethod
      @overload(int)
      def bar(n: int) -> tuple:
        return 'static', n

    class Sub(Foo):
      """Declares nothing at the name."""

    sub = Sub()
    onInstance = Sub.__dict__['bar']
    onClass = onInstance.getClassDispatcher()
    self.assertIsNot(onInstance, Foo.__dict__['bar'])
    self.assertIs(onClass.getFieldOwner(), Sub)
    self.assertEqual(sub.bar(1), ('bound', sub, 1))
    self.assertEqual(Sub.bar(1), ('static', 1))
    self._assertRefused(onInstance, lambda: sub.bar('s'), 's')
    self._assertRefused(onClass, lambda: Sub.bar('s'), 's')

  def test_subclass_adding_to_each_side(self) -> None:
    class Foo(BaseObject):
      @overload(int)
      def bar(self, n: int) -> tuple:
        return 'bound', self, n

      @staticmethod
      @overload(int)
      def bar(n: int) -> tuple:
        return 'static', n

    class Bound(Foo):
      @overload(str)
      def bar(self, s: str) -> tuple:
        return 'bound in Bound', self, s

    class Static(Foo):
      @staticmethod
      @overload(str)
      def bar(s: str) -> tuple:
        return 'static in Static', s

    bound, static = Bound(), Static()
    self.assertEqual(bound.bar('s'), ('bound in Bound', bound, 's'))
    self.assertEqual(bound.bar(1), ('bound', bound, 1))
    self.assertEqual(Bound.bar(1), ('static', 1))
    onClass = Bound.__dict__['bar'].getClassDispatcher()
    self._assertRefused(onClass, lambda: Bound.bar(None), None)
    self.assertEqual(Static.bar('s'), ('static in Static', 's'))
    self.assertEqual(Static.bar(1), ('static', 1))
    self.assertEqual(static.bar(1), ('bound', static, 1))
    onInstance = Static.__dict__['bar']
    self._assertRefused(onInstance, lambda: static.bar(None), None)

  def test_nearer_class_keeps_a_signature_on_its_own_side(self) -> None:
    class Foo(BaseObject):
      @overload(int)
      def bar(self, n: int) -> tuple:
        return 'bound', n

      @staticmethod
      @overload(int)
      def bar(n: int) -> tuple:
        return 'static', n

    class Sub(Foo):
      @overload(int)
      def bar(self, n: int) -> tuple:
        return 'bound in Sub', n

    self.assertEqual(Sub().bar(1), ('bound in Sub', 1))
    self.assertEqual(Sub.bar(1), ('static', 1))
    self.assertEqual(Foo().bar(1), ('bound', 1))
    self.assertEqual(Foo.bar(1), ('static', 1))

  def test_another_kind_alone_still_hides(self) -> None:
    class Base(BaseObject):
      @overload(int)
      def f(self, n: int) -> tuple:
        return 'bound', n

    class Static(Base):
      @staticmethod
      @overload(str)
      def f(s: str) -> tuple:
        return 'static', s

    class Both(Base):
      @overload(str)
      def f(self, s: str) -> tuple:
        return 'bound in Both', s

      @staticmethod
      @overload(str)
      def f(s: str) -> tuple:
        return 'static', s

    hidden = Static.__dict__['f']
    self.assertIs(hidden.getMethodKind(), staticmethod)
    self.assertIsNone(hidden.getClassDispatcher())
    self.assertEqual(Static.f('s'), ('static', 's'))
    self.assertEqual(Static().f('s'), ('static', 's'))
    self._assertRefused(hidden, lambda: Static().f(None), None)
    self.assertEqual(Both().f(1), ('bound', 1))
    self.assertEqual(Both().f('s'), ('bound in Both', 's'))
    self.assertEqual(Both.f('s'), ('static', 's'))

  def test_function_kind_by_hand(self) -> None:
    dispatcher = Dispatcher()
    self.assertIsNone(dispatcher._getFunctionKind(_bound))
    with self.assertRaises(TypeError) as context:
      dispatcher.setFunctionKind(None, _bound)
    self.assertIn("'classmethod' or 'staticmethod'", str(context.exception))
    dispatcher.setFunctionKind(classmethod, _class)
    dispatcher.setFunctionKind(staticmethod, _static)
    self.assertIs(dispatcher._getFunctionKind(_class), classmethod)
    self.assertIs(dispatcher._getFunctionKind(_static), staticmethod)
    self.assertIsNone(dispatcher._getFunctionKind(_bound))
    self.assertIs(dispatcher._adaptToKind(_bound), _bound)
    classed = dispatcher._adaptToKind(_class)
    self.assertIsNot(classed, _class)
    self.assertIs(dispatcher._adaptToKind(_class), classed)
    self.assertEqual(classed.__name__, '_class')
    self.assertEqual(classed('receiver', 3), ('class', str, 3))
    dropped = dispatcher._adaptToKind(_static)
    self.assertIsNot(dropped, _static)
    self.assertEqual(dropped('receiver', 3), ('static', 3))
    arrangement = Arrangement(('n',), (0,))
    permuter = PermuterMethod(_class, arrangement)
    dispatcher.setFunctionKind(classmethod, permuter)
    rebuilt = dispatcher._adaptToKind(permuter)
    self.assertIsInstance(rebuilt, PermuterMethod)
    self.assertIs(rebuilt.__wrapped__, classed)
    self.assertEqual(rebuilt.arrangement, arrangement)
    self.assertEqual(rebuilt('receiver', 3), ('class', str, 3))
    onClass = Dispatcher()
    onClass.setMethodKind(classmethod)
    onClass.setFunctionKind(staticmethod, _static)
    self.assertIs(onClass._getFunctionKind(_class), classmethod)
    self.assertIs(onClass._adaptToKind(_class), _class)
    self.assertEqual(onClass._adaptToKind(_static)('receiver', 3),
                     ('static', 3))
    copied = dispatcher.clone()
    self.assertIs(copied._getFunctionKind(_class), classmethod)
    self.assertIs(copied._getFunctionKind(_static), staticmethod)
    self.assertIs(copied._adaptToKind(_class), classed)
    dispatcher.addSigFunc(TypeSig(int), _bound)
    with self.assertRaises(WriteOnceError) as context:
      dispatcher.setFunctionKind(staticmethod, _bound)
    self.assertIs(context.exception.desc, dispatcher)
    self.assertEqual(len(context.exception.oldValue), 3)
    self.assertEqual(context.exception.newValue, (staticmethod, _bound))
    self.assertIn('write-once', str(context.exception))
    self.assertIsNone(dispatcher._getFunctionKind(_bound))

  def test_class_dispatcher_by_hand(self) -> None:
    onInstance, onClass = Dispatcher(), Dispatcher()
    self.assertIsNone(onInstance.getClassDispatcher())
    with self.assertRaises(TypeException) as context:
      onInstance.setClassDispatcher('dispatcher')
    exception = context.exception
    self.assertEqual(exception.varName, 'dispatcher')
    self.assertEqual(exception.actualObject, 'dispatcher')
    self.assertIs(exception.actualType, str)
    self.assertEqual(exception.expectedTypes, (Dispatcher,))
    self.assertIn("'dispatcher'", str(exception))
    onClass.setMethodKind(staticmethod)
    onClass.addSigFunc(TypeSig(THIS), _static)
    onInstance.addSigFunc(TypeSig(int), _bound)
    onInstance.setClassDispatcher(onClass)
    self.assertIs(onInstance.getClassDispatcher(), onClass)
    copied = onInstance.clone()
    self.assertIsNot(copied.getClassDispatcher(), onClass)
    self.assertIsInstance(copied.getClassDispatcher(), Dispatcher)
    copied.restoreTHIS()

    class First:
      """The class the two dispatchers are placed on."""

    class Second:
      """The class the clone is placed on."""

    onInstance.__set_name__(First, 'd')
    self.assertIs(onClass.getFieldOwner(), First)
    self.assertEqual(onClass.getFieldName(), 'd')
    first = First()
    throughInstance = onInstance.__get__(first, First)
    throughClass = onInstance.__get__(None, First)
    self.assertEqual(throughInstance(3), ('bound', first, 3))
    self.assertEqual(throughClass(first), ('static', first))
    copied.restoreTHIS()
    copied.__set_name__(Second, 'd')
    second = Second()
    side = copied.getClassDispatcher()
    self.assertIs(side.getFieldOwner(), Second)
    throughClass = copied.__get__(None, Second)
    self.assertEqual(throughClass(second), ('static', second))
    self._assertRefused(side, lambda: throughClass(first), first)
