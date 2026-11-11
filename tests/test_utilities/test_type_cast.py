"""
TestTypeCast tests 'typeCast' and 'hasCastRule' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import typeCast, hasCastRule
from worktoy.waitaminute.dispatch import TypeCastException, UnboundCastHook
from . import UtilitiesTest, Count, Inherits, Loose, Static, Refuser
from . import Foreign, Suspicious

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class TestTypeCast(UtilitiesTest):
  """
  'typeCast' is the one authority on conversion in the library: a value
  already of the target type passes, the number builtins and the text
  builtins convert within their family without loss, and any other
  class converts only through a classmethod '__cast_as__' of its own.
  The tests pin every conversion of the two families, every refusal
  with the exception naming the target and the value, the chaining of
  the error Python raised, the hook protocol with its three refusals,
  and 'hasCastRule' for each kind of target.
  """

  def assertRefused(self, target: type, arg: Any) -> TypeCastException:
    """The cast raises 'TypeCastException' naming the target and value."""
    with self.assertRaises(TypeCastException) as context:
      typeCast(target, arg)
    self.assertIs(context.exception.type_, target)
    self.assertIs(context.exception.arg, arg)
    self.assertIn("'%s'" % target.__name__, str(context.exception))
    return context.exception

  def test_docstring_examples(self) -> None:
    self.assertEqual(typeCast(int, 3.0), 3)
    self.assertEqual(typeCast(str, b'hello'), 'hello')
    self.assertIs(typeCast(int, True), True)

  def test_instance_passes_as_itself(self) -> None:
    cases = ((int, 3), (str, 'a'), (list, [1]), (int, True), (float, 1.5),
             (bytes, b'x'), (object, object()), (Count, Count(2)))
    for target, value in cases:
      with self.subTest(target=target.__name__):
        self.assertIs(typeCast(target, value), value)

  def test_str_from_text(self) -> None:
    self.assertEqual(typeCast(str, 'héllo'.encode('utf-8')), 'héllo')
    self.assertEqual(typeCast(str, bytearray(b'abc')), 'abc')
    self.assertIsInstance(typeCast(str, bytearray(b'abc')), str)

  def test_str_refusals(self) -> None:
    exception = self.assertRefused(str, b'\xff')
    self.assertIsInstance(exception.__cause__, UnicodeDecodeError)
    self.assertIsNone(self.assertRefused(str, 5).__cause__)
    self.assertRefused(str, 1.5)
    self.assertRefused(str, None)
    self.assertRefused(str, [b'a'])

  def test_bytes_from_text(self) -> None:
    out = typeCast(bytes, bytearray(b'abc'))
    self.assertEqual(out, b'abc')
    self.assertIs(type(out), bytes)
    self.assertEqual(typeCast(bytes, 'héllo'), 'héllo'.encode('utf-8'))

  def test_bytes_refusals(self) -> None:
    exception = self.assertRefused(bytes, '\ud800')
    self.assertIsInstance(exception.__cause__, UnicodeEncodeError)
    self.assertRefused(bytes, 5)
    self.assertRefused(bytes, [1, 2])

  def test_bytearray_from_text(self) -> None:
    out = typeCast(bytearray, b'abc')
    self.assertEqual(out, bytearray(b'abc'))
    self.assertIs(type(out), bytearray)
    self.assertEqual(typeCast(bytearray, 'hé'),
                     bytearray('hé'.encode('utf-8')))

  def test_bytearray_refusals(self) -> None:
    exception = self.assertRefused(bytearray, '\ud800')
    self.assertIsInstance(exception.__cause__, UnicodeEncodeError)
    self.assertRefused(bytearray, 5)

  def test_bool_from_numbers(self) -> None:
    cases = ((0, False), (1, True), (0.0, False), (1.0, True),
             (0j, False), (1 + 0j, True))
    for value, expected in cases:
      with self.subTest(value=value):
        out = typeCast(bool, value)
        self.assertIs(out, expected)

  def test_bool_refusals(self) -> None:
    for value in (2, -1, 0.5, 1.5, 2j, 'True', '1', None, [1]):
      with self.subTest(value=value):
        self.assertRefused(bool, value)

  def test_bool_never_asks_eq(self) -> None:
    suspicious = Suspicious()
    self.assertTrue(suspicious == 1)
    self.assertEqual(suspicious.asked, 1)
    self.assertRefused(bool, suspicious)
    self.assertEqual(suspicious.asked, 1)

  def test_int_from_numbers(self) -> None:
    cases = ((3.0, 3), (-0.0, 0), (2 + 0j, 2), (-7.0, -7), (1e3, 1000))
    for value, expected in cases:
      with self.subTest(value=value):
        out = typeCast(int, value)
        self.assertEqual(out, expected)
        self.assertIs(type(out), int)

  def test_int_refusals(self) -> None:
    values = (3.5, 2 + 1j, 2 - 1j, 2.5 + 0j, '3', None, float('inf'),
              float('nan'))
    for value in values:
      with self.subTest(value=value):
        self.assertRefused(int, value)

  def test_float_from_numbers(self) -> None:
    cases = ((7, 7.0), (True, 1.0), (2 ** 53, float(2 ** 53)), (3 + 0j, 3.0),
             (-2, -2.0))
    for value, expected in cases:
      with self.subTest(value=value):
        out = typeCast(float, value)
        self.assertEqual(out, expected)
        self.assertIs(type(out), float)

  def test_float_refusals(self) -> None:
    exception = self.assertRefused(float, 10 ** 400)
    self.assertIsInstance(exception.__cause__, OverflowError)
    self.assertIsNone(self.assertRefused(float, 2 ** 53 + 1).__cause__)
    self.assertIsNone(self.assertRefused(float, -(2 ** 53 + 1)).__cause__)
    for value in (3 + 1j, 3 - 1j, '1.5', None, [1.0]):
      with self.subTest(value=value):
        self.assertRefused(float, value)

  def test_complex_from_numbers(self) -> None:
    cases = ((7, 7 + 0j), (True, 1 + 0j), (1.5, 1.5 + 0j), (-2, -2 + 0j))
    for value, expected in cases:
      with self.subTest(value=value):
        out = typeCast(complex, value)
        self.assertEqual(out, expected)
        self.assertIs(type(out), complex)
        self.assertEqual(repr(out), repr(expected))

  def test_complex_refusals(self) -> None:
    exception = self.assertRefused(complex, 10 ** 400)
    self.assertIsInstance(exception.__cause__, OverflowError)
    self.assertIsNone(self.assertRefused(complex, 2 ** 53 + 1).__cause__)
    self.assertIsNone(self.assertRefused(complex, -(2 ** 53 + 1)).__cause__)
    for value in ('1j', None, [1]):
      with self.subTest(value=value):
        self.assertRefused(complex, value)

  def test_no_string_parsed_no_constructor_called(self) -> None:
    #  'int('3')' and 'bytes(5)' would succeed; the cast never calls them.
    self.assertRefused(int, '3')
    self.assertRefused(bytes, 5)
    self.assertRefused(list, (1, 2))
    self.assertRefused(tuple, [1, 2])
    self.assertRefused(slice, 3)
    self.assertRefused(type, 3)

  def test_builtin_subclass_without_hook_refused(self) -> None:
    Plain = type('Plain', (int,), {})
    self.assertRefused(Plain, 3)
    self.assertRefused(Plain, 3.0)
    self.assertTrue(hasCastRule(Plain))

  def test_hook_builds_instance(self) -> None:
    out = typeCast(Count, 3.0)
    self.assertEqual(out, 3)
    self.assertIs(type(out), Count)

  def test_hook_bound_to_subclass(self) -> None:
    out = typeCast(Inherits, 2.0)
    self.assertEqual(out, 2)
    self.assertIs(type(out), Inherits)

  def test_hook_errors_propagate(self) -> None:
    with self.assertRaises(TypeCastException) as context:
      typeCast(Count, 'x')
    self.assertIs(context.exception.type_, int)
    self.assertEqual(context.exception.arg, 'x')
    self.assertIn("'int'", str(context.exception))
    self.assertIn('x', str(context.exception))

  def test_hook_not_implemented_refused(self) -> None:
    self.assertRefused(Refuser, 5)

  def test_hook_foreign_result_refused(self) -> None:
    self.assertRefused(Foreign, 5)

  def test_hook_result_not_asked_for_equality(self) -> None:
    #  The result is compared with 'NotImplemented' by identity, so a
    #  result equal to everything still passes as the instance it is.
    out = typeCast(Suspicious, 5)
    self.assertIsInstance(out, Suspicious)
    self.assertEqual(out.asked, 0)
    self.assertTrue(hasCastRule(Suspicious))

  def test_subclass_instance_offered_to_the_hook(self) -> None:
    class Sub(Suspicious):
      """A strict subclass of a class with a cast hook."""

    class Plain:
      """A class without a cast hook."""

    class PlainSub(Plain):
      """A strict subclass of it."""

    exact = Suspicious()
    sub = Sub()
    self.assertIs(typeCast(Suspicious, exact), exact)
    self.assertIs(typeCast(Sub, sub), sub)
    out = typeCast(Suspicious, sub)
    self.assertIsNot(out, sub)
    self.assertIs(type(out), Suspicious)
    plainSub = PlainSub()
    self.assertIs(typeCast(Plain, plainSub), plainSub)
    self.assertIs(typeCast(int, True), True)

  def test_plain_class_refused(self) -> None:
    Plain = type('Plain', (), {})
    self.assertRefused(Plain, 5)
    self.assertFalse(hasCastRule(Plain))

  def test_unbound_hook_refused(self) -> None:
    for target in (Loose, Static):
      with self.subTest(target=target.__name__):
        with self.assertRaises(UnboundCastHook) as context:
          typeCast(target, 5)
        self.assertEqual(context.exception.className, target.__name__)
        self.assertIsNone(context.exception.targetName)
        self.assertIn("'%s'" % target.__name__, str(context.exception))
        self.assertIn('@classmethod', str(context.exception))
        with self.assertRaises(UnboundCastHook) as context:
          hasCastRule(target)
        self.assertEqual(context.exception.className, target.__name__)
        self.assertIsNone(context.exception.targetName)
        self.assertIn("'%s'" % target.__name__, str(context.exception))

  def test_unbound_hook_would_misbehave(self) -> None:
    #  The premise of the refusal: called on the class, a plain function
    #  takes the value as 'self', and a staticmethod has no class to
    #  build an instance of.
    self.assertEqual(Loose.__cast_as__(5, 6), 6)
    with self.assertRaises(TypeError):
      Loose.__cast_as__(5)
    self.assertEqual(Static.__cast_as__(5), 5)

  def test_unbound_hook_names_inheriting_target(self) -> None:
    LooseChild = type('LooseChild', (Loose,), {})
    with self.assertRaises(UnboundCastHook) as context:
      typeCast(LooseChild, 5)
    self.assertEqual(context.exception.className, 'Loose')
    self.assertEqual(context.exception.targetName, 'LooseChild')
    self.assertIn("'Loose'", str(context.exception))
    self.assertIn("'LooseChild'", str(context.exception))

  def test_has_cast_rule(self) -> None:
    ruled = (bool, int, float, complex, str, bytes, bytearray,
             Count, Inherits, Refuser, Foreign)
    for target in ruled:
      with self.subTest(target=target.__name__):
        self.assertTrue(hasCastRule(target))
    for target in (list, tuple, dict, slice, type, object):
      with self.subTest(target=target.__name__):
        self.assertFalse(hasCastRule(target))
    self.assertFalse(hasCastRule(42))
