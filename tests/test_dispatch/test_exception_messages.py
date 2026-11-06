"""
TestExceptionMessages renders the messages of the exceptions
'worktoy.dispatch' raises and pins their slots.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher, TypeSig
from worktoy.waitaminute import UncheckableType
from worktoy.waitaminute.dispatch import BareOverload, DispatchException
from worktoy.waitaminute.dispatch import DuplicateSignature
from worktoy.waitaminute.dispatch import TypeCastException
from . import DispatchTest, Label, Uncheckable


def _first(self, n: int) -> None:
  """The first function registered at a signature."""


def _second(self, n: int) -> None:
  """The second function registered at a signature."""


class TestExceptionMessages(DispatchTest):
  """
  An exception the package raises carries a message naming what went
  wrong, and slots holding what it was given, and both are what a
  reader looks for. 'waitaminute' has no tests of its own: each raising
  package renders the messages of the exceptions it raises. The tests
  pin the names each message carries, the branches the rendering
  takes, and every slot of each exception.
  """

  def test_bare_overload(self) -> None:
    named = BareOverload('overload', _first)
    self.assertEqual(named.decorator, 'overload')
    self.assertIs(named.func, _first)
    self.assertIn("'@overload'", str(named))
    self.assertIn("over '_first'", str(named))
    nameless = BareOverload('overload.flex', 5)
    self.assertEqual(nameless.decorator, 'overload.flex')
    self.assertEqual(nameless.func, 5)
    self.assertIn("'@overload.flex'", str(nameless))
    self.assertIn("over '5'", str(nameless))
    self.assertEqual(repr(nameless), str(nameless))

  def test_dispatch_exception(self) -> None:
    with self.assertRaises(DispatchException) as context:
      Label(1.5)
    exception = context.exception
    self.assertIs(exception.dispatch, Label.__dict__['__init__'])
    self.assertEqual(exception.posArgs, (1.5,))
    self.assertEqual(exception.keyArgs, {})
    text = str(exception)
    self.assertIn("'Label.__init__'", text)
    self.assertIn('<float 1.5>', text)
    self.assertIn('argument signature: <TypeSig: [float]>', text)
    self.assertIn('available signatures:', text)
    self.assertIn('<TypeSig: [str, int]>', text)
    self.assertNotIn('received keywords', text)
    with self.assertRaises(DispatchException) as context:
      Label(1.5, k=2)
    self.assertIn('received keywords: k', str(context.exception))
    self.assertEqual(context.exception.posArgs, (1.5,))
    self.assertEqual(context.exception.keyArgs, {'k': 2})

  def test_dispatch_exception_without_registrations(self) -> None:
    class Owner:
      d = Dispatcher()

    exception = DispatchException(Owner.__dict__['d'], ())
    self.assertIs(exception.dispatch, Owner.__dict__['d'])
    self.assertEqual(exception.posArgs, ())
    self.assertEqual(exception.keyArgs, {})
    text = str(exception)
    self.assertIn("'Owner.d'", text)
    self.assertEqual(text.count('(none)'), 2)
    self.assertEqual(repr(exception), text)

  def test_duplicate_signature(self) -> None:
    bySig = DuplicateSignature(TypeSig(int), _first, _second)
    self.assertEqual(bySig.sig, TypeSig(int))
    self.assertIs(bySig.existing, _first)
    self.assertIs(bySig.duplicate, _second)
    text = str(bySig)
    self.assertIn('<TypeSig: [int]>', text)
    self.assertIn('_first', text)
    self.assertIn('_second', text)
    self.assertIn('type signature', text)
    byRole = DuplicateSignature('fallback', _first, _second)
    self.assertEqual(byRole.sig, 'fallback')
    self.assertIn('fallback function', str(byRole))
    self.assertNotIn('type signature', str(byRole))
    self.assertEqual(repr(byRole), str(byRole))

  def test_type_cast_exception(self) -> None:
    exception = TypeCastException(int, 'seven')
    self.assertIs(exception.type_, int)
    self.assertEqual(exception.arg, 'seven')
    self.assertIn('seven', str(exception))
    self.assertIn("'int'", str(exception))
    self.assertEqual(repr(exception), str(exception))

  def test_uncheckable_type(self) -> None:
    with self.assertRaises(UncheckableType) as context:
      TypeSig.validateTypes(int, Uncheckable)
    signed = context.exception
    self.assertIs(signed.entry, Uncheckable)
    self.assertIn('Uncheckable', signed.declaration)
    self.assertEqual(signed.position, 1)
    self.assertIsInstance(signed.refusal, TypeError)
    text = str(signed)
    self.assertIn("'Uncheckable' at position 1", text)
    self.assertIn("'isinstance' refuses", text)
    self.assertIn('runtime_checkable', text)
    with self.assertRaises(UncheckableType) as context:
      TypeSig.validateTypes(Uncheckable, declaration='Box[Uncheckable]')
    boxed = context.exception
    self.assertIs(boxed.entry, Uncheckable)
    self.assertEqual(boxed.declaration, 'Box[Uncheckable]')
    self.assertIsNone(boxed.position)
    self.assertIsInstance(boxed.refusal, TypeError)
    self.assertIn("box 'Box[Uncheckable]'", str(boxed))
    self.assertIn("'Uncheckable' as its field type", str(boxed))
    self.assertEqual(repr(boxed), str(boxed))

  def test_random_casts(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      exception = TypeCastException(float, word)
      with self.subTest(word=word):
        self.assertIs(exception.type_, float)
        self.assertEqual(exception.arg, word)
        self.assertIn(word, str(exception))
        self.assertIn("'float'", str(exception))
