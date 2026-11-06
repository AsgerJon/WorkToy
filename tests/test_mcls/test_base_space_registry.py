"""
TestBaseSpaceRegistry tests the records a 'BaseSpace' from 'worktoy.mcls'
keeps of the declarations of one class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseMeta, BaseSpace
from worktoy.waitaminute.dispatch import DuplicateSignature
from worktoy.waitaminute.meta import MixedMethodKind
from . import MclsTest


def _first(self, n: int) -> None:
  """The first function registered at a name."""


def _second(self, n: int) -> None:
  """The second function registered at a name."""


class TestBaseSpaceRegistry(MclsTest):
  """
  'BaseSpace' records the concrete, flexible and variadic signatures,
  the fallback, the finalizer, the kind of method and the plain names
  of one body, and refuses a second declaration that would leave
  dispatch undecided. The tests drive a namespace by hand through every
  setter and getter, including the refusals.
  """

  def setUp(self) -> None:
    MclsTest.setUp(self)
    self.space = BaseSpace(BaseMeta, 'Hand', ())

  def test_empty(self) -> None:
    self.assertEqual(self.space.getOverloads(), {})
    self.assertEqual(self.space.getVariadics(), {})
    self.assertEqual(self.space.getFlexes(), {})
    self.assertEqual(self.space.getFallbacks(), {})
    self.assertEqual(self.space.getFinalizers(), {})
    self.assertEqual(self.space.getMethodKinds(), {})
    self.assertEqual(self.space.getPlainNames(), ())
    self.assertIsNone(self.space.getClaimedName(overload(int)(_first)))
    self.assertFalse(self.space.hasOverloads('f'))
    self.assertEqual(self.space._getDeclaredKind('f'), ())
    self.assertEqual(self.space.getOverloadNames(), [])

  def test_overloads(self) -> None:
    self.space.addOverload('f', TypeSig(int), _first)
    self.space.addOverload('f', TypeSig(int), _first)
    self.space.addOverload('f', TypeSig(str), _second)
    recorded = self.space.getOverloads()['f']
    self.assertEqual(recorded,
                     [(TypeSig(int), _first), (TypeSig(str), _second)])
    self.assertTrue(self.space.hasOverloads('f'))
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addOverload('f', TypeSig(int), _second)
    self.assertEqual(context.exception.sig, TypeSig(int))
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('<TypeSig: [int]>', str(context.exception))
    self.assertIn('_first', str(context.exception))
    self.assertEqual(len(self.space.getOverloads()['f']), 2)

  def test_flexes(self) -> None:
    sig = TypeSig(int, str, float, list)
    self.space.addFlex('g', sig, _first)
    self.space.addFlex('g', TypeSig(str, int, list, float), _first)
    self.assertEqual(self.space.getFlexes()['g'], [(sig, _first)])
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addFlex('g', TypeSig(list, float, str, int), _second)
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertEqual(context.exception.sig, TypeSig(list, float, str, int))
    self.assertIn('[list, float, str, int]', str(context.exception))
    self.space.addFlex('g', TypeSig(int, int, str, float), _second)
    self.assertEqual(len(self.space.getFlexes()['g']), 2)
    self.space.addFlex('g', TypeSig(int, str, float, list, dict), _second)
    self.assertEqual(len(self.space.getFlexes()['g']), 3)
    self.space.addFlex('m', TypeSig(int, str, float, list, dict), _first)
    self.space.addFlex('m', TypeSig(list, float, str, int), _second)
    self.assertEqual(len(self.space.getFlexes()['m']), 2)
    self.assertTrue(self.space.hasOverloads('g'))

  def test_flex_and_overload_of_one_bag(self) -> None:
    self.space.addFlex('g', TypeSig(int, str, float, list), _first)
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addOverload('g', TypeSig(str, int, float, list), _second)
    self.assertEqual(context.exception.sig, TypeSig(str, int, float, list))
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('[str, int, float, list]', str(context.exception))
    self.space.addOverload('g', TypeSig(str, int, float, list), _first)
    self.space.addOverload('g', TypeSig(int), _second)
    self.space.addOverload('g', TypeSig(int, str, float, list, dict),
                           _second)
    self.assertEqual(len(self.space.getOverloads()['g']), 3)
    self.space.addOverload('h', TypeSig(int, str, float, list), _first)
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addFlex('h', TypeSig(list, float, str, int), _second)
    self.assertEqual(context.exception.sig, TypeSig(list, float, str, int))
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('_second', str(context.exception))
    self.space.addFlex('h', TypeSig(list, float, str, int), _first)
    self.assertEqual(len(self.space.getFlexes()['h']), 1)
    self.space.addOverload('k', TypeSig(int, str, float, list, dict),
                           _first)
    self.space.addFlex('k', TypeSig(list, float, str, int), _second)
    self.assertEqual(len(self.space.getFlexes()['k']), 1)

  def test_variadics(self) -> None:
    sig = TypeSig(ARGS[int])
    self.space.addVariadic('v', sig, _first)
    self.space.addVariadic('v', TypeSig(ARGS[int]), _first)
    self.space.addVariadic('v', TypeSig(str, ARGS[int]), _second)
    self.assertEqual(len(self.space.getVariadics()['v']), 2)
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addVariadic('v', TypeSig(ARGS[int]), _second)
    self.assertEqual(context.exception.sig, sig)
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('ARGS[int]', str(context.exception))
    self.assertTrue(self.space.hasOverloads('v'))

  def test_fallback_and_finalizer(self) -> None:
    self.space.addFallback('f', _first)
    self.space.addFallback('f', _first)
    self.assertEqual(self.space.getFallbacks(), {'f': _first})
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addFallback('f', _second)
    self.assertEqual(context.exception.sig, 'fallback')
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('fallback function', str(context.exception))
    self.space.addFinalizer('g', _first)
    self.space.addFinalizer('g', _first)
    self.assertEqual(self.space.getFinalizers(), {'g': _first})
    with self.assertRaises(DuplicateSignature) as context:
      self.space.addFinalizer('g', _second)
    self.assertEqual(context.exception.sig, 'finalizer')
    self.assertIs(context.exception.existing, _first)
    self.assertIs(context.exception.duplicate, _second)
    self.assertIn('finalizer function', str(context.exception))
    self.assertTrue(self.space.hasOverloads('f'))
    self.assertTrue(self.space.hasOverloads('g'))
    self.assertEqual(self.space.getOverloadNames(), ['f', 'g'])

  def test_method_kinds(self) -> None:
    self.space.addMethodKind('f', None)
    self.space.addMethodKind('f', None)
    self.space.addMethodKind('g', classmethod)
    self.assertEqual(self.space.getMethodKinds(),
                     {'f': None, 'g': classmethod})
    self.assertEqual(self.space._getDeclaredKind('f'), (None,))
    self.assertEqual(self.space._getDeclaredKind('g'), (classmethod,))
    with self.assertRaises(MixedMethodKind) as context:
      self.space.addMethodKind('f', staticmethod)
    exception = context.exception
    self.assertEqual(exception.className, 'Hand')
    self.assertEqual(exception.overloadName, 'f')
    self.assertEqual(exception.kinds, (None, staticmethod))
    self.assertIn('instance method', str(exception))

  def test_plain_names(self) -> None:
    self.space.addPlainName('p')
    self.space.addPlainName('p')
    self.space.addPlainName('q')
    self.space.addPlainName('plain')
    self.assertEqual(self.space.getPlainNames(), ('p', 'q', 'plain'))
    self.space.removePlainName('q')
    self.assertEqual(self.space.getPlainNames(), ('p', 'plain'))
    self.space.removePlainName(str.join('', ['pl', 'ain']))
    self.assertEqual(self.space.getPlainNames(), ('p',))
    self.space.removePlainName('absent')
    self.assertEqual(self.space.getPlainNames(), ('p',))

  def test_claimed_names(self) -> None:
    first = overload(int)(_first)
    second = overload(int)(_second)
    self.space.addClaimedName(first, 'f')
    self.assertEqual(self.space.getClaimedName(first), 'f')
    self.assertIsNone(self.space.getClaimedName(second))
    self.space.addClaimedName(second, 'g')
    self.assertEqual(self.space.getClaimedName(second), 'g')

  def test_random_names(self) -> None:
    self.randomWord.size = 6
    words = self.randomWord.row
    for word in words:
      self.space.addOverload(word, TypeSig(int), _first)
    self.assertEqual(self.space.getOverloadNames(), [*dict.fromkeys(words)])
    for word in words:
      with self.subTest(word=word):
        self.assertTrue(self.space.hasOverloads(word))
        self.assertIsNone(self.space.collectFallback(word))
