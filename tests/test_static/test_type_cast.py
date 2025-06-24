"""
TestTypeCast tests the 'typeCast' function from the 'worktoy.static' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject
from worktoy.static import typeCast, overload
from worktoy.static.zeroton import THIS
from worktoy.waitaminute import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestTypeCast(TestCase):
  """
  TestTypeCast tests the 'typeCast' function from the 'worktoy.static'
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_exact(self) -> None:
    """
    Test that 'typeCast(target, arg)' returns 'arg' when 'arg' is an
    instance of 'target'.
    """
    self.assertEqual(typeCast(int, 42), 42)
    self.assertEqual(typeCast(str, 'hello'), 'hello')
    self.assertEqual(typeCast(float, 3.14), 3.14)
    self.assertEqual(typeCast(list, [1, 2, 3]), [1, 2, 3])

  def test_good_to_str(self) -> None:
    """
    Test that 'typeCast(str, arg)' converts 'arg' to a string, but only
    when arg is an instance of 'bytes'.
    """
    self.assertEqual(typeCast(str, b'hello'), 'hello')

  def test_bad_to_str(self) -> None:
    """
    Test that 'typeCast(str, arg)' raises TypeError when 'arg' is not an
    instance of 'bytes'.
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(str, 42)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, str)
    self.assertEqual(e.arg, 42)

  def test_bad_to_dispatcher(self) -> None:
    """
    Test that 'typeCast' raises TypeError when 'arg' is not an instance of
    'target'.
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
        pass

      @overload(str)
      def __init__(self, *args) -> None:
        """
        Initialize Foo no args
        """
        pass

    with self.assertRaises(TypeCastException) as context:
      typeCast(Foo, 42)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, Foo)
    self.assertEqual(e.arg, 42)

  def test_good_to_int(self) -> None:
    """
    Test that 'typeCast(int, arg)' converts 'arg' to an integer, but only
    when 'arg' is an instance of 'float'.
    """
    self.assertEqual(typeCast(int, 3.0), 3)
    self.assertEqual(typeCast(int, '42'), 42)
    self.assertEqual(typeCast(int, 69 + 0j), 69)
    self.assertTrue(typeCast(int, True))
    self.assertFalse(typeCast(int, False))

  def test_bad_value_to_int(self) -> None:
    """
    Test that 'typeCast(int, arg)' raises TypeError when 'arg' is not an
    instance of 'float' or 'str'.
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
    Test that 'typeCast(int, arg)' raises TypeError when 'arg' is not an
    instance of 'float' or 'str'.
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(int, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, int)

  def test_good_to_float(self) -> None:
    """
    Test that 'typeCast(float, arg)' converts 'arg' to a float, but only
    when 'arg' is an instance of 'int'.
    """
    self.assertEqual(typeCast(float, 3), 3.0)
    self.assertEqual(typeCast(float, '3.14'), 3.14)
    self.assertEqual(typeCast(float, 69 + 0j), 69.0)

  def test_bad_value_to_float(self) -> None:
    """
    Test that 'typeCast(float, arg)' raises TypeError when 'arg' is not an
    instance of 'int' or 'str'.
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
    Test that 'typeCast(float, arg)' raises TypeError when 'arg' is not an
    instance of 'int' or 'str'.
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(float, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, float)

  def test_good_to_complex(self) -> None:
    """
    Test that 'typeCast(complex, arg)' converts 'arg' to a complex number,
    but only when 'arg' is an instance of 'int' or 'float'.
    """
    self.assertEqual(typeCast(complex, 3), 3 + 0j)
    self.assertEqual(typeCast(complex, 3.14), 3.14 + 0j)
    self.assertEqual(typeCast(complex, '3.14'), 3.14 + 0j)
    self.assertEqual(typeCast(complex, '3+4j'), 3 + 4j)

  def test_bad_value_to_complex(self) -> None:
    """
    Test that 'typeCast(complex, arg)' raises TypeError when 'arg' is not an
    instance of 'int', 'float', or 'str'.
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
    Test that 'typeCast(complex, arg)' raises TypeError when 'arg' is not an
    instance of 'int', 'float', or 'str'.
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(complex, lambda: None)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, complex)

  def test_any_to_bool(self) -> None:
    """
    Test that 'typeCast(bool, arg)' converts 'arg' to a boolean.
    """
    self.assertTrue(typeCast(bool, 1))
    self.assertFalse(typeCast(bool, 0))
    self.assertTrue(typeCast(bool, 'True'))
    self.assertTrue(typeCast(bool, 'False'))
    self.assertTrue(typeCast(bool, [1, 2, 3]))
    self.assertFalse(typeCast(bool, []))

  def test_bad_targets(self, ) -> None:
    """
    Test that 'typeCast' raises TypeError when 'target' is not a supported
    type. Except are only exact matches where the argument given is an
    instance of the otherwise unsupported type.
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

  def test_good_unpacked_to_target(self) -> None:
    """
    Test that 'typeCast(target, arg)' can unpack 'arg' to match 'target'.
    """
    self.assertEqual(typeCast(int, (42,)), 42)
    self.assertEqual(typeCast(str, ['hello']), 'hello')
    self.assertEqual(typeCast(float, [3.14]), 3.14)

  def test_bad_unpacked_to_target(self) -> None:
    """
    Test that 'typeCast(target, arg)' raises TypeError when 'arg' cannot be
    unpacked to match 'target'.
    """
    with self.assertRaises(TypeCastException) as context:
      typeCast(int, ['breh', ])
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.type_, int)
    self.assertEqual(e.arg, 'breh', )
