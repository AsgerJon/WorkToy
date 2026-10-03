"""
TestVariadicExactPass subclasses 'OverloadTest' and pins that a variadic
declaration is one registration, matched by exact type at any length. A
declaration such as '@overload(int, ARGS[str])' used to be stored as the
concrete signatures of every length up to five beside the variadic one, so
a call one argument past that limit left the exact-type lookup: with
'@overload(ARGS[object])' declared before '@overload(ARGS[int])', a call
of three integers reached the 'int' function by exact type while a call
of seven reached the 'object' function by 'isinstance'. The dispatcher now
finds the variadic signature accepting a call by exact type by hash, the
prefix and the trailing type as the key, so the same function receives
both calls, and the expansions, their collision rules, the ambiguity
record and the limit are gone.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import VariadicOverlap

from . import OverloadTest


class Bag(BaseObject):
  """Bag takes any objects, or integers alone, the empty call settled."""

  @overload(ARGS[object])
  def put(self, *items: object) -> str:
    return 'objects'

  @overload(ARGS[int])
  def put(self, *items: int) -> str:
    return 'ints'

  @overload()
  def put(self) -> str:
    return 'empty'


class Parent(BaseObject):
  """Parent declares one integer explicitly, and an integer with a
  string."""

  @overload(int)
  def f(self, n: int) -> str:
    return 'parent explicit'

  @overload(int, str)
  def f(self, n: int, s: str) -> str:
    return 'parent labelled'


class Child(Parent):
  """Child declares any number of integers, which covers the one."""

  @overload(ARGS[int])
  def f(self, *ns: int) -> str:
    return 'child variadic'


class Sibling(Parent):
  """Sibling declares two integers followed by any number of integers,
  which does not cover the one alone."""

  @overload(int, int, ARGS[int])
  def f(self, n: int, m: int, *ns: int) -> str:
    return 'sibling variadic'


class Wide(BaseObject):
  """Wide declares any number of integers."""

  @overload(ARGS[int])
  def f(self, *ns: int) -> str:
    return 'wide variadic'


class Narrow(Wide):
  """Narrow declares one integer explicitly, and inherits the rest."""

  @overload(int)
  def f(self, n: int) -> str:
    return 'narrow explicit'


class Nearer(Wide):
  """Nearer declares an integer followed by any number of integers, which
  shares every call of two or more with the inherited declaration."""

  @overload(int, ARGS[int])
  def f(self, n: int, *ns: int) -> str:
    return 'nearer variadic'


class _NoHashMeta(type):
  """_NoHashMeta makes its classes refuse to be hashed."""

  __hash__ = None


class Odd(metaclass=_NoHashMeta):
  """Odd cannot be hashed as a class."""


class Disjoint(BaseObject):
  """Disjoint declares two variadics sharing no call: the prefix of one
  is a string, which the other takes no string for."""

  @overload(ARGS[int])
  def f(self, *ns: int) -> str:
    return 'ints'

  @overload(str, ARGS[int])
  def f(self, label: str, *ns: int) -> str:
    return 'labelled'


class Tagger(BaseObject):
  """Tagger takes any object, or an integer followed by any number of
  strings, the integer alone included."""

  @overload(object)
  def f(self, item: object) -> str:
    return 'object'

  @overload(int, ARGS[str])
  def f(self, n: int, *tags: str) -> str:
    return 'tagged'


class Taker(BaseObject):
  """Taker takes any objects."""

  @overload(ARGS[object])
  def take(self, *items: object) -> int:
    return len(items)


def _first(self, *xs: int) -> str:
  return 'first'  # pragma: no cover


def _second(self, n: int, *xs: int) -> str:
  return 'second'  # pragma: no cover


class TestVariadicExactPass(OverloadTest):
  """
  TestVariadicExactPass provides tests for the exact-type matching of
  variadic declarations.
  """

  def test_exact_match_at_every_length(self) -> None:
    """The variadic declaration matching every argument by exact type
    receives the call at any length, ahead of one declared earlier that
    matches only through 'isinstance'."""
    bag = Bag()
    for n in (1, 3, 5, 6, 7, 20):
      with self.subTest(n=n):
        self.assertEqual(bag.put(*range(n)), 'ints')
    self.assertEqual(bag.put(), 'empty')

  def test_isinstance_match_unchanged(self) -> None:
    """A call matching no declaration by exact type still goes to the
    first declared that matches through 'isinstance', at any length."""
    bag = Bag()
    self.assertEqual(bag.put(True, False), 'objects')
    self.assertEqual(bag.put(*([True] * 7)), 'objects')
    self.assertEqual(bag.put('a', 1), 'objects')
    self.assertEqual(bag.put(1, 'a'), 'objects')
    self.assertEqual(bag.put(1, 2, 3, 4, 5, 6, 'a'), 'objects')

  def test_one_registration_per_declaration(self) -> None:
    """A variadic declaration is held once, as written, with no
    concrete signature beside it, on the overload and on the dispatcher."""
    ov = overload(str, ARGS[int])(_first)
    self.assertEqual([*ov], [])
    self.assertEqual(ov.getVariadics(), [(TypeSig(str, ARGS[int]), _first)])
    dispatcher = Wide.__dict__['f']
    self.assertEqual(dispatcher._getSigFuncList(), [])
    self.assertEqual(len(dispatcher._getVariadicFuncs()), 1)
    self.assertFalse(hasattr(overload, '__variadic_fastpath_limit__'))

  def test_str_lists_declaration(self) -> None:
    """The 'str()' of an overload lists the variadic declaration as
    written."""
    ov = overload(str, ARGS[int])(_first)
    self.assertIn(str(TypeSig(str, ARGS[int])), str(ov))

  def test_subclass_variadic_covers_inherited_explicit(self) -> None:
    """A variadic declaration of a subclass accepting a call by exact type
    beats the explicit declaration of that call inherited from a parent,
    as an override wins every type match it competes in."""
    self.assertEqual(Child().f(5), 'child variadic')
    self.assertEqual(Child().f(*range(7)), 'child variadic')
    self.assertEqual(Parent().f(5), 'parent explicit')

  def test_inherited_explicit_outside_variadic(self) -> None:
    """The inherited explicit declarations keep the calls a subclass
    variadic does not accept by exact type: one too short for its
    prefix, and one whose trailing argument is not of its inner type."""
    self.assertEqual(Sibling().f(5), 'parent explicit')
    self.assertEqual(Sibling().f(5, 6), 'sibling variadic')
    self.assertEqual(Sibling().f(5, 6, 7), 'sibling variadic')
    self.assertEqual(Child().f(5, 'a'), 'parent labelled')

  def test_prefix_alone_exact(self) -> None:
    """A call of the prefix alone matches the variadic declaration by
    exact type, ahead of a concrete declaration matching it through
    'isinstance' only."""
    self.assertEqual(Tagger().f(5), 'tagged')
    self.assertEqual(Tagger().f(5, 'a', 'b'), 'tagged')
    self.assertEqual(Tagger().f('x'), 'object')
    self.assertEqual(Tagger().f(True), 'object')

  def test_disjoint_variadics_accepted(self) -> None:
    """Two variadic declarations sharing no call build without complaint
    and each receives its own calls."""
    self.assertEqual(Disjoint().f(1, 2), 'ints')
    self.assertEqual(Disjoint().f(), 'ints')
    self.assertEqual(Disjoint().f('a', 1), 'labelled')
    self.assertEqual(Disjoint().f('a'), 'labelled')

  def test_subclass_explicit_beats_inherited_variadic(self) -> None:
    """An explicit declaration of a subclass beats an inherited variadic
    declaration accepting the same call, and the variadic keeps the
    rest."""
    self.assertEqual(Narrow().f(5), 'narrow explicit')
    self.assertEqual(Narrow().f(5, 6), 'wide variadic')
    self.assertEqual(Narrow().f(), 'wide variadic')

  def test_nearest_variadic_wins(self) -> None:
    """Of two variadic declarations accepting a call by exact type, the
    nearest to the class wins, and the inherited one keeps the calls the
    nearer does not accept."""
    self.assertEqual(Nearer().f(1, 2), 'nearer variadic')
    self.assertEqual(Nearer().f(*range(9)), 'nearer variadic')
    self.assertEqual(Nearer().f(), 'wide variadic')

  def test_same_inner_overlap_unsettleable(self) -> None:
    """Two variadic declarations of one inner type whose prefixes share a
    call share every longer call too, so an explicit declaration of the
    shared call settles nothing, and the class body is refused."""
    with self.assertRaises(VariadicOverlap) as context:
      class Totals(BaseObject):
        add = overload(ARGS[int])(_first)
        add = overload(int, ARGS[int])(_second)  # noqa: F811
        add = overload(int)(_second)  # noqa: F811
    self.assertEqual(context.exception.sig, TypeSig(int))

  def test_unhashable_class_in_call(self) -> None:
    """An argument whose class cannot be hashed misses the exact passes
    and is matched through 'isinstance', at any length."""
    taker = Taker()
    self.assertEqual(taker.take(Odd(), Odd()), 2)
    self.assertEqual(taker.take(*[Odd() for _ in range(8)]), 8)
    self.assertEqual(taker.take(1, Odd()), 2)
