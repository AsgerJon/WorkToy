"""
TestDispatcherCalls tests the compiled dispatch function of 'Dispatcher'
from 'worktoy.dispatch' on dispatchers fed by hand.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import MethodType

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import Dispatcher, TypeSig
from worktoy.waitaminute.dispatch import DispatchException
from . import DispatchTest, UnhashableMeta


def _tag(name: str):
  """A function reporting its name, the receiver and its arguments."""
  def func(receiver: object, *args, **kwargs) -> tuple:
    return name, args, kwargs
  func.__name__ = name
  func.__doc__ = 'Docstring of %s.' % name
  return func


class TestDispatcherCalls(DispatchTest):
  """
  A call reaches the declaration matching its positional arguments
  through five passes: exact classes, 'isinstance' nearest class first,
  casts that widen numbers only, every cast, then the fallback or
  'DispatchException'. The tests pin each pass and the order between
  them, the nearer class winning an exact hit of a farther one, the
  flexible and variadic routes of each pass, the finalizer with and
  without an exception, the reads through class and instance for each
  method kind, and the call with no arguments at all.
  """

  @staticmethod
  def _placed() -> tuple:
    """A plain class holding a fresh dispatcher at 'd', and that
    dispatcher, which a read of 'Owner.d' would compile into a function."""
    class Owner:
      d = Dispatcher()
    return Owner, Owner.__dict__['d']

  def test_no_arguments_at_all(self) -> None:
    Owner, d = self._placed()
    with self.assertRaises(TypeError) as context:
      Owner.d()
    message = "Owner.d() missing 1 required positional argument: 'self'"
    self.assertEqual(str(context.exception), message)

  def test_exact_hit(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    d.addSigFunc(TypeSig(str, int), _tag('str-int'))
    owner = Owner()
    self.assertEqual(owner.d(1, k=2), ('int', (1,), {'k': 2}))
    self.assertEqual(owner.d('a', 1), ('str-int', ('a', 1), {}))
    self.assertEqual(Owner.d(owner, 1), ('int', (1,), {}))

  def test_nearer_class_overrides_exact_hit_of_farther(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('far'), 1)
    d.addSigFunc(TypeSig(object), _tag('near'), 0)
    self.assertEqual(Owner().d(1)[0], 'near')
    Other, od = self._placed()
    od.addSigFunc(TypeSig(int), _tag('far'), 1)
    od.addSigFunc(TypeSig(str), _tag('near'), 0)
    self.assertEqual(Other().d(1)[0], 'far')

  def test_isinstance_pass(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    d.addSigFunc(TypeSig(int, int), _tag('int-int'))
    self.assertEqual(Owner().d(True)[0], 'int')
    self.assertEqual(Owner().d(True, 1)[0], 'int-int')
    with self.assertRaises(DispatchException) as context:
      Owner().d(True, 'x')
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, (True, 'x'))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'Owner.d'", str(context.exception))

  def test_widening_before_narrowing(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(float), _tag('float'))
    d.addSigFunc(TypeSig(int), _tag('int'))
    self.assertEqual(Owner().d(2), ('int', (2,), {}))
    Other, od = self._placed()
    od.addSigFunc(TypeSig(int), _tag('int'))
    od.addSigFunc(TypeSig(float), _tag('float'))
    self.assertEqual(Other().d(2.0), ('float', (2.0,), {}))
    Third, td = self._placed()
    td.addSigFunc(TypeSig(float), _tag('float'))
    self.assertEqual(Third().d(2), ('float', (2.0,), {}))
    Fourth, fd = self._placed()
    fd.addSigFunc(TypeSig(int), _tag('int'))
    self.assertEqual(Fourth().d(2.0), ('int', (2,), {}))
    with self.assertRaises(DispatchException) as context:
      Fourth().d(2.5)
    self.assertIs(context.exception.dispatch, fd)
    self.assertEqual(context.exception.posArgs, (2.5,))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'Owner.d'", str(context.exception))

  def test_cast_pass_keeps_instances_and_moves_on(self) -> None:
    #  Text casts freely in the widening pass; only numbers are held to
    #  widening there, so a failed number cast moves on to the next
    #  signature and the narrowing pass takes what is left.
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int, str), _tag('int-str'))
    d.addSigFunc(TypeSig(float, int), _tag('float-int'))
    self.assertEqual(Owner().d(1, b'x'), ('int-str', (1, 'x'), {}))
    self.assertEqual(Owner().d(1, 2), ('float-int', (1.0, 2), {}))
    self.assertEqual(Owner().d(2.0, b'x'), ('int-str', (2, 'x'), {}))
    with self.assertRaises(DispatchException) as context:
      Owner().d(2.5, 2.5)
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, (2.5, 2.5))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn('<float 2.5>', str(context.exception))

  def test_fallback_and_refusal(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    owner = Owner()
    with self.assertRaises(DispatchException) as context:
      owner.d('x', k=1)
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, ('x',))
    self.assertEqual(context.exception.keyArgs, {'k': 1})
    self.assertIn('received keywords: k', str(context.exception))
    d.setFallbackFunction(_tag('fallback'))
    self.assertEqual(owner.d('x', k=1), ('fallback', ('x',), {'k': 1}))
    self.assertEqual(owner.d(1), ('int', (1,), {}))

  def test_finalizer(self) -> None:
    log = []

    def final(receiver: object, *args, **kwargs) -> None:
      log.append(args)

    def loud(receiver: object, *args, **kwargs) -> None:
      raise ValueError('final')

    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    d.setFinalizerFunction(final)
    owner = Owner()
    self.assertEqual(owner.d(1)[0], 'int')
    with self.assertRaises(DispatchException) as context:
      owner.d('x')
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, ('x',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("<str 'x'>", str(context.exception))
    self.assertEqual(log, [(1,), ('x',)])
    Other, od = self._placed()
    od.addSigFunc(TypeSig(int), _tag('int'))
    od.setFinalizerFunction(loud)
    with self.assertRaises(ValueError) as context:
      Other().d(1)
    self.assertIsNone(context.exception.__cause__)
    self.assertEqual(str(context.exception), 'final')
    with self.assertRaises(ValueError) as context:
      Other().d('x')
    self.assertIsInstance(context.exception.__cause__, DispatchException)
    self.assertEqual(str(context.exception), 'final')
    self.assertEqual(context.exception.__cause__.posArgs, ('x',))

  def test_unhashable_class_goes_to_isinstance_pass(self) -> None:
    class Odd(metaclass=UnhashableMeta):
      pass

    with self.assertRaises(TypeError):
      hash(Odd)
    self.assertTrue(Odd == Odd)
    self.assertFalse(Odd == int)
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(object), _tag('any'))
    odd = Odd()
    self.assertEqual(Owner().d(odd), ('any', (odd,), {}))

  def test_flexible_declaration_routes(self) -> None:
    #  Four classes none of which casts into another, so every call has
    #  one assignment: by exact class, by 'isinstance', by widening.
    class Items(list):
      pass

    Owner, d = self._placed()
    d.addFlexSigFunc(TypeSig(str, float, list, dict), _tag('wide'))
    owner = Owner()
    items = Items()
    self.assertEqual(owner.d({}, [], 2.0, 's')[1], ('s', 2.0, [], {}))
    self.assertEqual(owner.d({}, items, 2.0, 's')[1], ('s', 2.0, items, {}))
    self.assertEqual(owner.d({}, [], 2, 's')[1], ('s', 2.0, [], {}))
    with self.assertRaises(DispatchException) as context:
      owner.d({}, [], 'x', 's')
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, ({}, [], 'x', 's'))
    self.assertIn("'Owner.d'", str(context.exception))
    with self.assertRaises(DispatchException) as context:
      owner.d({}, [])
    self.assertEqual(context.exception.posArgs, ({}, []))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn('argument signature: <TypeSig: [dict, list]>',
                  str(context.exception))
    Narrow, nd = self._placed()
    nd.addFlexSigFunc(TypeSig(str, int, list, dict), _tag('narrow'))
    self.assertEqual(Narrow().d({}, [], 2.0, 's')[1], ('s', 2, [], {}))

  def test_variadic_routes(self) -> None:
    Owner, d = self._placed()
    d.addVariadicSigFunc(TypeSig(int, ARGS[str]), _tag('int-strs'))
    owner = Owner()
    self.assertEqual(owner.d(1, 'a', 'b')[1], (1, 'a', 'b'))
    self.assertEqual(owner.d(1)[1], (1,))
    self.assertEqual(owner.d(True, 'a')[1], (True, 'a'))
    self.assertEqual(owner.d(1, 'a', b'b')[1], (1, 'a', 'b'))
    self.assertEqual(owner.d(2.0, 'a')[1], (2, 'a'))
    for args in ((), ('x',), ('x', 'a'), (1, 'a', 2), (1, 2.5)):
      with self.subTest(args=args):
        with self.assertRaises(DispatchException) as context:
          owner.d(*args)
        self.assertIs(context.exception.dispatch, d)
        self.assertEqual(context.exception.posArgs, args)
        self.assertIn("'Owner.d'", str(context.exception))

  def test_variadic_against_flexible_by_distance(self) -> None:
    Owner, d = self._placed()
    d.addFlexSigFunc(TypeSig(int, str, str, str), _tag('flex'), 1)
    d.addVariadicSigFunc(TypeSig(int, ARGS[str]), _tag('variadic'), 0)
    self.assertEqual(Owner().d(1, 'a', 'b', 'c')[0], 'variadic')
    Other, od = self._placed()
    od.addFlexSigFunc(TypeSig(int, str, str, str), _tag('flex'), 0)
    od.addVariadicSigFunc(TypeSig(int, ARGS[str]), _tag('variadic'), 1)
    flexed = ('flex', (1, 'a', 'b', 'c'), {})
    self.assertEqual(Other().d('a', 1, 'b', 'c'), flexed)
    self.assertEqual(Other().d(1, 'a', 'b', 'c'), flexed)
    self.assertEqual(Other().d(1, 'a')[0], 'variadic')

  def test_reads_by_method_kind(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    self.assertEqual(Owner.d.__name__, 'd')
    self.assertEqual(Owner.d.__qualname__, 'Owner.d')
    self.assertEqual(Owner.d.__doc__, 'Docstring of int.')
    self.assertEqual(Owner.d.__module__, __name__)
    bound = Owner().d
    self.assertIsInstance(bound, MethodType)
    self.assertIs(bound.__func__, Owner.d)
    owner = Owner()
    self.assertIs(d.__get__(owner, None).__self__, owner)
    Classy, cd = self._placed()
    cd.setMethodKind(classmethod)
    cd.addSigFunc(TypeSig(int), _tag('int'))
    self.assertEqual(Classy.d(1), ('int', (1,), {}))
    self.assertIs(Classy.d.__self__, Classy)
    self.assertIs(Classy().d.__self__, Classy)
    def alone(*args, **kwargs) -> tuple:
      return 'alone', args, kwargs

    def spare(*args, **kwargs) -> tuple:
      return 'spare', args, kwargs

    Static, sd = self._placed()
    sd.setMethodKind(staticmethod)
    sd.addSigFunc(TypeSig(int), alone)
    sd.setFallbackFunction(spare)
    self.assertEqual(Static.d(1), ('alone', (1,), {}))
    self.assertEqual(Static().d('x', k=2), ('spare', ('x',), {'k': 2}))
    self.assertIs(Static.d.__self__, Static)

  def test_empty_dispatcher(self) -> None:
    Owner, d = self._placed()
    self.assertIsNone(Owner.d.__doc__)
    with self.assertRaises(DispatchException) as context:
      Owner().d()
    self.assertIs(context.exception.dispatch, d)
    self.assertEqual(context.exception.posArgs, ())
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn('received:', str(context.exception))

  def test_random_calls(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int), _tag('int'))
    d.addSigFunc(TypeSig(str), _tag('str'))
    owner = Owner()
    for number, word in zip(self.randomInteger.row, self.randomWord.row):
      with self.subTest(number=number, word=word):
        self.assertEqual(owner.d(number), ('int', (number,), {}))
        self.assertEqual(owner.d(word), ('str', (word,), {}))

  def test_most_recent_variadic_wins_exact_lookup(self) -> None:
    Owner, d = self._placed()
    d.addVariadicSigFunc(TypeSig(ARGS[int]), _tag('older'))
    d.addVariadicSigFunc(TypeSig(int, ARGS[int]), _tag('newer'))
    self.assertEqual(Owner().d(1, 2)[0], 'newer')
    Other, od = self._placed()
    od.addVariadicSigFunc(TypeSig(int, ARGS[int]), _tag('older'))
    od.addVariadicSigFunc(TypeSig(ARGS[int]), _tag('newer'))
    self.assertEqual(Other().d(1, 2)[0], 'newer')

  def test_flexible_preferred_over_variadic_at_one_distance(self) -> None:
    Owner, d = self._placed()
    d.addVariadicSigFunc(TypeSig(int, ARGS[str]), _tag('variadic'))
    d.addFlexSigFunc(TypeSig(int, str, str, str), _tag('flex'))
    self.assertEqual(Owner().d(1, 'a', 'b', 'c')[0], 'flex')

  def test_cast_pass_tries_variadics_farthest_first(self) -> None:
    Owner, d = self._placed()
    d.addVariadicSigFunc(TypeSig(ARGS[float]), _tag('near'), 0)
    d.addVariadicSigFunc(TypeSig(ARGS[complex]), _tag('far'), 1)
    self.assertEqual(Owner().d(1), ('far', (1 + 0j,), {}))

  def test_fewer_arguments_than_declared(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int, int), _tag('int-int'))
    for args in ((True,), (1.0,), ()):
      with self.subTest(args=args):
        with self.assertRaises(DispatchException) as context:
          Owner().d(*args)
        self.assertIs(context.exception.dispatch, d)
        self.assertEqual(context.exception.posArgs, args)
        self.assertIn("'Owner.d'", str(context.exception))

  def test_length_mismatch_moves_to_next_concrete(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(int, int), _tag('int-int'), 0)
    d.addSigFunc(TypeSig(int), _tag('int'), 0)
    d.addSigFunc(TypeSig(float), _tag('float'), 1)
    self.assertEqual(Owner().d(True)[0], 'int')
    Other, od = self._placed()
    od.addSigFunc(TypeSig(int, int), _tag('int-int'))
    od.addSigFunc(TypeSig(float), _tag('float'))
    self.assertEqual(Other().d(1), ('float', (1.0,), {}))

  def test_isinstance_pass_beats_a_farther_cast(self) -> None:
    #  A farther concrete signature that the cast pass would take shows
    #  that the flexible and variadic registrations of the nearer class
    #  are matched in the 'isinstance' pass, whatever their shape.
    class Items(list):
      pass

    Flex, fd = self._placed()
    fd.addFlexSigFunc(TypeSig(str, float, list, dict), _tag('flex'), 0)
    fd.addSigFunc(TypeSig(dict, list, float, str), _tag('far'), 1)
    self.assertEqual(Flex().d({}, Items(), 2.0, 's')[0], 'flex')
    self.assertEqual(Flex().d({}, Items(), 2, 's')[0], 'far')
    Vari, vd = self._placed()
    vd.addVariadicSigFunc(TypeSig(int, ARGS[str]), _tag('tail'), 0)
    vd.addVariadicSigFunc(TypeSig(int, int, int, ARGS[str]), _tag('long'), 0)
    vd.addVariadicSigFunc(TypeSig(str, ARGS[str]), _tag('text'), 0)
    vd.addSigFunc(TypeSig(int), _tag('far-one'), 1)
    vd.addSigFunc(TypeSig(int, str), _tag('far-two'), 1)
    self.assertEqual(Vari().d(True)[0], 'tail')
    self.assertEqual(Vari().d(True, 'a')[0], 'tail')
    self.assertEqual(Vari().d(1, 'a'), ('tail', (1, 'a'), {}))

  def test_cast_pass_variadic_routes(self) -> None:
    Owner, d = self._placed()
    d.addVariadicSigFunc(TypeSig(float, ARGS[str]), _tag('float-strs'))
    d.addVariadicSigFunc(TypeSig(float, float, ARGS[str]),
                         _tag('two-floats'))
    self.assertEqual(Owner().d(1), ('float-strs', (1.0,), {}))
    self.assertEqual(Owner().d(1, 2), ('two-floats', (1.0, 2.0), {}))
    Kept, kd = self._placed()
    kd.addVariadicSigFunc(TypeSig(int, float, ARGS[str]), _tag('int-float'))
    self.assertEqual(Kept().d(1, 2), ('int-float', (1, 2.0), {}))
    self.assertEqual(Kept().d(1, 2, 'a'), ('int-float', (1, 2.0, 'a'), {}))
    Text, td = self._placed()
    td.addVariadicSigFunc(TypeSig(bytes, ARGS[str]), _tag('bytes'))
    td.addVariadicSigFunc(TypeSig(float, ARGS[str]), _tag('float'))
    self.assertEqual(Text().d('a'), ('bytes', (b'a',), {}))

  def test_override_searches_strictly_nearer_tiers(self) -> None:
    Owner, d = self._placed()
    d.addSigFunc(TypeSig(str), _tag('near'), 0)
    d.addSigFunc(TypeSig(object), _tag('far-any'), 1)
    d.addSigFunc(TypeSig(int), _tag('far-int'), 1)
    self.assertEqual(Owner().d(1)[0], 'far-int')
