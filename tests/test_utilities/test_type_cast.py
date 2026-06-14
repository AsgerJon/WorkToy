"""
TestTypeCast tests the 'typeCast' function from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from . import UtilitiesTest
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.core.sentinels import THIS
from worktoy.waitaminute.dispatch import TypeCastException


class TestTypeCast(UtilitiesTest):
  """
  TestTypeCast tests the 'typeCast' function from 'worktoy.utilities'.
  """

  def test_exact(self) -> None:
    """
    Testing that 'typeCast(target, arg)' returns 'arg' when 'arg' is an
    instance of 'target'.
    """
    self.assertEqual(typeCast(int, 42), 42)
    self.assertEqual(typeCast(str, 'hello'), 'hello')
    self.assertEqual(typeCast(float, 3.14), 3.14)
    self.assertEqual(typeCast(list, [1, 2, 3]), [1, 2, 3])

  def test_good_to_str(self) -> None:
    """
    Testing that 'typeCast(str, arg)' converts 'arg' to a string, but only
    when arg is an instance of 'bytes'.
    """
    self.assertEqual(typeCast(str, b'hello'), 'hello')

  def test_bad_to_str(self) -> None:
    """
    Testing that 'typeCast(str, arg)' raises 'TypeCastException' for a
    value that is neither a 'str' nor decodable 'bytes' (here an int).
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(str, 42)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, str)
    self.assertEqual(e.arg, 42)

  def test_bad_to_dispatcher(self) -> None:
    """
    Testing that 'typeCast' raises 'TypeCastException' when 'arg' cannot be
    cast to 'target' (here a 'BaseObject' subclass).
    """

    class Foo(BaseObject):
      """
      Overloaded class for testing type casting.
      """

      @overload(THIS)
      def __init__(self, *args) -> None:
        """
        Initialize Foo with an integer.
        """

      @overload(str)
      def __init__(self, *args) -> None:
        """
        Initialize Foo no args
        """

    with self.assertRaises(TypeCastException) as context:
      typeCast(Foo, 42)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, Foo)
    self.assertEqual(e.arg, 42)

  def test_good_to_int(self) -> None:
    """
    Testing that 'typeCast(int, arg)' returns an int for a whole-number
    float, an integer-valued real complex, a parseable str, and bool.
    """
    self.assertEqual(typeCast(int, 3.0), 3)
    self.assertEqual(typeCast(int, '42'), 42)
    self.assertEqual(typeCast(int, 69 + 0j), 69)
    self.assertTrue(typeCast(int, True))
    self.assertFalse(typeCast(int, False))

  def test_bad_value_to_int(self) -> None:
    """
    Testing that 'typeCast(int, arg)' raises 'TypeCastException' for values
    that cannot be converted without loss: a non-integer float, a
    non-parseable str, and a complex with a nonzero imaginary part.
    """
    for bad in [0.80085, 'breh', 69 + 420j, ]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(int, bad)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, int)
      self.assertEqual(e.arg, bad)

  def test_bad_type_to_int(self) -> None:
    """
    Testing that 'typeCast(int, arg)' raises 'TypeCastException' for a value
    whose type has no conversion rule (a lambda).
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(int, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, int)

  def test_good_to_float(self) -> None:
    """
    Testing that 'typeCast(float, arg)' returns a float for an int, a
    parseable str, and a real-valued complex.
    """
    self.assertEqual(typeCast(float, 3), 3.0)
    self.assertEqual(typeCast(float, '3.14'), 3.14)
    self.assertEqual(typeCast(float, 69 + 0j), 69.0)

  def test_bad_value_to_float(self) -> None:
    """
    Testing that 'typeCast(float, arg)' raises 'TypeCastException' for a
    non-parseable str and a complex with a nonzero imaginary part.
    """
    for bad in ['breh', 69 + 420j, ]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(float, bad)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, float)
      self.assertEqual(e.arg, bad)

  def test_bad_type_to_float(self) -> None:
    """
    Testing that 'typeCast(float, arg)' raises 'TypeCastException' for a
    value whose type has no conversion rule (a lambda).
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(float, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, float)

  def test_good_to_complex(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' returns a complex for an int, a
    float, and a parseable str (including '3+4j').
    """
    self.assertEqual(typeCast(complex, 3), 3 + 0j)
    self.assertEqual(typeCast(complex, 3.14), 3.14 + 0j)
    self.assertEqual(typeCast(complex, '3.14'), 3.14 + 0j)
    self.assertEqual(typeCast(complex, '3+4j'), 3 + 4j)

  def test_bad_value_to_complex(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' raises 'TypeCastException' for a
    non-parseable str.
    """
    for bad in ['breh', ]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(complex, bad)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, complex)
      self.assertEqual(e.arg, bad)

  def test_bad_type_to_complex(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' raises 'TypeCastException' for a
    value whose type has no conversion rule (a lambda).
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(complex, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, complex)

  def test_any_to_bool(self) -> None:
    """
    Testing that 'typeCast(bool, arg)' converts 'arg' to a boolean.
    """
    self.assertTrue(typeCast(bool, 1))
    self.assertFalse(typeCast(bool, 0))
    self.assertTrue(typeCast(bool, True))
    self.assertFalse(typeCast(bool, False))

  def test_bad_targets(self, ) -> None:
    """
    Testing that 'typeCast' raises 'TypeCastException' when 'target' is an
    unsupported type (list, tuple, set, frozenset, dict), except for an
    exact match where 'arg' is already an instance of that type.
    """
    for target in [list, tuple, set, frozenset, dict]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(target, 42)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, target)
      self.assertEqual(e.arg, 42)

    # Exact match should not raise an exception
    self.assertEqual(typeCast(list, []), [])
    self.assertEqual(typeCast(tuple, ()), ())
    self.assertEqual(typeCast(set, set()), set())
    self.assertEqual(typeCast(frozenset, frozenset()), frozenset())
    self.assertEqual(typeCast(dict, {}), {})

  def test_str_to_str(self) -> None:
    """
    Testing that 'typeCast(str, arg)' returns 'arg' when 'arg' is an
    instance of 'str'.
    """
    self.assertEqual(typeCast(str, 'hello'), 'hello')

  def test_bad_bytes_to_str(self) -> None:
    """
    Creates a bad bytes object that causes an exception when any attempt
    is made to decode it under 'utf-8' encoding.
    """
    bad_bytes = bytes([0x80, 0xFF])  # Invalid UTF-8 byte sequence
    with self.assertRaises(TypeCastException) as context:
      typeCast(str, bad_bytes)
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def test_int_to_float(self) -> None:
    """
    Testing that 'typeCast(float, arg)' returns 'arg' when 'arg' is an
    instance of
    'int'.
    """
    for value in [69, 420, 1337, 80085, 8008135]:
      self.assertAlmostEqual(typeCast(float, value), float(value))

  def test_int_to_float_overflow(self) -> None:
    """
    Testing that 'typeCast(float, arg)' raises 'TypeCastException' (chained
    from 'OverflowError') for an int too large for a float, instead of
    letting the 'OverflowError' escape.
    """
    for big in [2 ** 2000, 10 ** 400, -(2 ** 2000)]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(float, big)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, float)
      self.assertEqual(e.arg, big)
      self.assertIsInstance(e.__cause__, OverflowError)

  def test_int_to_float_precision_loss(self) -> None:
    """
    Testing that 'typeCast(float, arg)' raises 'TypeCastException' for an
    int a float cannot hold exactly, honoring the lossless contract in
    the int-to-float direction.
    """
    for lossy in [2 ** 53 + 1, 2 ** 60 + 1, -(2 ** 64 + 1)]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(float, lossy)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, float)
      self.assertEqual(e.arg, lossy)

  def test_int_to_float_exact_large(self) -> None:
    """
    Testing that 'typeCast(float, arg)' still succeeds for large ints a
    float represents exactly, including powers of two at and beyond the
    53-bit mantissa boundary.
    """
    for exact in [2 ** 53, 2 ** 100, -(2 ** 90), 2 ** 53 - 1]:
      out = typeCast(float, exact)
      self.assertIsInstance(out, float)
      self.assertEqual(int(out), exact)

  def test_int_to_complex_overflow(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' raises 'TypeCastException'
    (chained from 'OverflowError') for an int too large for the float
    real part, instead of leaking the 'OverflowError'.
    """
    for big in [2 ** 2000, 10 ** 400, -(2 ** 2000)]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(complex, big)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, complex)
      self.assertEqual(e.arg, big)
      self.assertIsInstance(e.__cause__, OverflowError)

  def test_int_to_complex_precision_loss(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' raises 'TypeCastException' for an
    int whose value a float real part cannot hold exactly.
    """
    for lossy in [2 ** 53 + 1, 2 ** 60 + 1, -(2 ** 64 + 1)]:
      with self.assertRaises(TypeCastException) as context:
        typeCast(complex, lossy)
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertIs(e.type_, complex)
      self.assertEqual(e.arg, lossy)

  def test_int_to_complex_exact_large(self) -> None:
    """
    Testing that 'typeCast(complex, arg)' still succeeds for large ints a
    float represents exactly, returning a complex with zero imaginary
    part.
    """
    for exact in [2 ** 53, 2 ** 100, -(2 ** 90)]:
      out = typeCast(complex, exact)
      self.assertIsInstance(out, complex)
      self.assertEqual(out.imag, 0.0)
      self.assertEqual(int(out.real), exact)

  def test_slice_from_valid_list(self) -> None:
    """
    Testing that 'typeCast(slice, arg)' builds the matching slice from a
    list of up to three int or None components.
    """
    self.assertEqual(typeCast(slice, [1, 10, 2]), slice(1, 10, 2))

  def test_slice_from_invalid_list(self) -> None:
    """
    Testing that 'typeCast(slice, arg)' raises 'TypeCastException' for a
    list whose components do not form a valid slice.
    """
    with self.assertRaises(TypeCastException):
      typeCast(slice, ['x', 'y'])
