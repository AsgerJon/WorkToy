"""
TestEZOrder tests ordering of EZData classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests import WYD
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ez import UnorderedEZException, EZDeleteException
from . import EZTest
from worktoy.ezdata import EZData, EZDesc

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class OrderFull(EZData, frozen=True, order=True):
  """
  OrderFull is an EZData class that is fully ordered.
  It is used to test the ordering functionality of EZData classes.
  """

  a = 0
  b = 0
  c = 0


class OrderLess(EZData, frozen=True, order=False):
  """
  OrderLess is an EZData class that is not ordered.
  It is used to test the non-ordering functionality of EZData classes.
  """

  a = 0
  b = 0
  c = 0


class LongOrder(EZData, frozen=True, order=True):
  """
  LongOrder is an EZData class that is fully ordered and has a long
  number of fields.
  """
  a = 0
  b = 1
  c = 2
  d = 3
  e = 4
  f = 5
  g = 6
  h = 7
  i = 8
  j = 9


class MutableLong(EZData, frozen=False, ):
  """
  MutableLong is an EZData class that is mutable and has a long
  number of fields.
  """
  a = 0
  b = 1
  c = 2
  d = 3
  e = 4
  f = 5
  g = 6
  h = 7
  i = 8
  j = 9


class TestEZOrder(EZTest):
  """Tests ordering of EZData classes."""

  def test_good_ordering(self) -> None:
    """Test that EZData classes with order=True are ordered correctly."""
    a = OrderFull(1, 2, 3)
    b = OrderFull(4, 5, 6)
    c = OrderFull(7, 8, 9)

    self.assertLess(a, b)
    self.assertTrue(a <= b)
    self.assertTrue(b >= a)
    self.assertLess(b, c)
    self.assertTrue(b <= c)
    self.assertTrue(c >= b)
    self.assertLess(a, c)
    self.assertTrue(a <= c)
    self.assertTrue(c >= a)

    self.assertGreater(b, a, )
    self.assertGreater(c, b, )
    self.assertGreater(c, a, )

    self.assertFalse(a < a)
    self.assertFalse(a > a)
    self.assertFalse(b < a)
    self.assertFalse(a > b)

    for i in 'abc':
      self.assertEqual(i, i)
      self.assertLessEqual(i, i)
      self.assertGreaterEqual(i, i)

  def test_bad_ordering(self) -> None:
    """Apply inequality operators between EZData and other types."""

    with self.assertRaises(UnorderedEZException) as context:
      OrderLess(1, 2, 3) < OrderLess(1, 2, 3)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderLess')

    with self.assertRaises(UnorderedEZException) as context:
      OrderLess(1, 2, 3) <= OrderLess(1, 2, 3)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderLess')

    with self.assertRaises(UnorderedEZException) as context:
      OrderLess(1, 2, 3) >= OrderLess(1, 2, 3)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderLess')

    with self.assertRaises(UnorderedEZException) as context:
      OrderLess(1, 2, 3) > OrderLess(1, 2, 3)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderLess')

  def test_order_other_type(self) -> None:
    """Test that EZData classes with order=False raise an error when
    compared."""

    class Loser:
      def __lt__(self, *_) -> bool:
        return True

    class NeverWin:
      def __le__(self, *_) -> bool:
        return True

    class NeverLose:
      def __ge__(self, *_) -> bool:
        return True

    class Asger:
      def __gt__(self, *_) -> bool:
        return True

    classes = [Loser, NeverWin, NeverLose, Asger]
    for cls in classes:
      with self.assertRaises(UnorderedEZException) as context:
        OrderLess(1, 2, 3) < cls()
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertEqual(e.className, 'OrderLess')
      with self.assertRaises(UnorderedEZException) as context:
        OrderLess(1, 2, 3) <= cls()
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertEqual(e.className, 'OrderLess')
      with self.assertRaises(UnorderedEZException) as context:
        OrderLess(1, 2, 3) >= cls()
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertEqual(e.className, 'OrderLess')
      with self.assertRaises(UnorderedEZException) as context:
        OrderLess(1, 2, 3) > cls()
      e = context.exception
      self.assertEqual(str(e), repr(e))
      self.assertEqual(e.className, 'OrderLess')

    self.assertLess(Loser(), OrderFull(1, 2, 3))
    self.assertLessEqual(NeverWin(), OrderFull(1, 2, 3))
    self.assertGreaterEqual(NeverLose(), OrderFull(1, 2, 3))
    self.assertGreater(Asger(), OrderFull(1, 2, 3))

    self.assertGreater(OrderFull(1, 2, 3), Loser(), )
    self.assertGreaterEqual(OrderFull(1, 2, 3), NeverWin(), )
    self.assertLessEqual(OrderFull(1, 2, 3), NeverLose(), )
    self.assertLess(OrderFull(1, 2, 3), Asger(), )

  def test_eq_self_type(self) -> None:
    """Test that EZData classes with order=True are equal."""
    a = OrderFull(1, 2, 3)
    b = OrderFull(1, 2, 3)
    c = OrderFull(4, 5, 6)

    self.assertEqual(a, b)
    self.assertNotEqual(a, c)
    self.assertNotEqual(b, c)

  def test_eq_other_type(self) -> None:
    """Test that EZData classes with order=False are not equal to other
    types."""
    a = OrderLess(1, 2, 3)
    b = OrderLess(1, 2, 3)
    c = OrderLess(4, 5, 6)

    self.assertEqual(a, b)
    self.assertNotEqual(a, c)
    self.assertNotEqual(b, c)

    self.assertNotEqual(a, 'string')
    self.assertNotEqual(b, 123)
    self.assertNotEqual(c, [1, 2, 3])

  def test_str_repr(self) -> None:
    """Test the string representation of EZData classes."""
    a = OrderFull(1, 2, 3)

    self.assertIn('=', str(a))
    self.assertIn('OrderFull', str(a))
    self.assertNotIn('=', repr(a))

  def test_iter(self) -> None:
    """Test that EZData classes with order=True can be iterated."""
    A = OrderFull(0, 1, 2, )
    for i, c in enumerate(A):
      self.assertEqual(i, c)
    self.assertEqual(len(A), 3)
    self.assertEqual(len(A), len(OrderFull))

  def test_good_index_get_item(self) -> None:
    """Test that EZData classes with order=True can be indexed."""
    a = OrderFull(0, 1, 2, )
    self.assertEqual(a[0], 0)
    self.assertEqual(a[1], 1)
    self.assertEqual(a[2], 2)
    self.assertEqual(a[0 - 69], 0)
    self.assertEqual(a[1 - 69], 1)
    self.assertEqual(a[2 - 69], 2)

  def test_bad_index_get_item(self) -> None:
    """Test that EZData classes with order=True raise an error when
    indexed out of range."""
    a = OrderFull(0, 1, 2, )
    with self.assertRaises(IndexError):
      _ = a[3]

    with self.assertRaises(IndexError):
      _ = a[4]

  def test_good_str_get_item(self) -> None:
    """Test that EZData classes with order=True raise an error when
    indexed out of range."""
    A = OrderFull(0, 1, 2, )
    self.assertEqual(A['a'], 0)
    self.assertEqual(A['b'], 1)
    self.assertEqual(A['c'], 2)

  def test_bad_str_get_item(self) -> None:
    """Test that EZData classes with order=True raise an error when
    indexed out of range."""
    a = OrderFull(0, 1, 2, )
    with self.assertRaises(KeyError):
      _ = a['never']

    with self.assertRaises(KeyError):
      _ = a['gonna']

    with self.assertRaises(KeyError):
      _ = a['give']

    with self.assertRaises(KeyError):
      _ = a['you']

    with self.assertRaises(KeyError):
      _ = a['up']

  def test_good_slice_get_item(self) -> None:
    """Test that EZData classes with order=True can be sliced."""

    args = (69, 420, 1337, 80085, 8008135, 69, 420, 1337, 80085, 8008135,)
    A = LongOrder(*args)
    self.assertEqual(A[0:3], args[0:3])
    self.assertEqual(A[1:4], args[1:4])
    self.assertEqual(A[2:5], args[2:5])
    self.assertEqual(A[3:6], args[3:6])
    self.assertEqual(A[4:7], args[4:7])
    self.assertEqual(A[5:8], args[5:8])
    self.assertEqual(A[::], args[::])

  def test_bad_slice_get_item(self) -> None:
    """Test that EZData classes with order=True raise an error when
    sliced out of range. It does not. Because slicing is forgiving,
    so instead of IndexError, an empty tuple returns."""
    args = (69, 420, 1337, 80085, 8008135, 69, 420, 1337, 80085, 8008135,)
    A = LongOrder(*args)
    self.assertFalse(A[69:420])

  def test_bad_type_get_item(self) -> None:
    """Test that EZData classes with order=True raise an error when
    indexed with an unsupported identifier type"""
    a = OrderFull(0, 1, 2, )
    with self.assertRaises(TypeException) as context:
      _ = a[object]
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, object)
    self.assertEqual(e.actualType, type(object))
    self.assertEqual(set(e.expectedTypes), {int, str, slice})

    with self.assertRaises(TypeException) as context:
      _ = a[None]
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, None)
    self.assertEqual(e.actualType, type(None))
    self.assertEqual(set(e.expectedTypes), {int, str, slice})

    with self.assertRaises(TypeException) as context:
      _ = a[3.14]
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, 3.14)
    self.assertEqual(e.actualType, type(3.14))
    self.assertEqual(set(e.expectedTypes), {int, str, slice})

    trololo = Exception()
    with self.assertRaises(TypeException) as context:
      _ = a[trololo]
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, trololo)
    self.assertEqual(e.actualType, type(trololo))
    self.assertEqual(set(e.expectedTypes), {int, str, slice})

  def test_bad_type_set_item(self) -> None:
    """Tests that EZData classes raises TypeException when using
    identifiers of unsupported types on __setitem__."""
    A = OrderFull(0, 1, 2, )

    with self.assertRaises(TypeException):
      A[object] = 69

    with self.assertRaises(TypeException):
      A[None] = 420

    with self.assertRaises(TypeException):
      A[3.14] = 1337

    with self.assertRaises(TypeException):
      A[Exception()] = 80085

  def test_good_set_item(self) -> None:
    """Test that EZData classes with order=True can be set."""

    args = (69, 420, 1337, 80085, 8008135, 69, 420, 1337, 80085, 8008135,)
    keys = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    A = MutableLong()
    for i, slot in enumerate(A):
      self.assertEqual(slot, i)
    for i, arg in enumerate(args):
      A[i] = arg
    B = MutableLong()
    for i, slot in enumerate(B):
      self.assertEqual(slot, i)
    for key, arg in zip(keys, args):
      B[key] = arg
    for slot, arg in zip(B, args):
      self.assertEqual(slot, arg)
    C = MutableLong()

    class Knife:
      def __getitem__(self, s: slice) -> slice:
        return s

    cut = Knife()[1:3]
    C[cut] = args[cut]
    cutIndices = [i for i, _ in enumerate(C)][cut]
    for i, slot in enumerate(C):
      if i in cutIndices:
        self.assertEqual(slot, args[i])
      else:
        self.assertEqual(slot, i)

  def test_bad_set_item(self) -> None:
    """Testing __setitem__ on indices not in range."""
    A = OrderFull(0, 1, 2, )

    with self.assertRaises(IndexError):
      A[69] = 420

  def test_bad_str_set_item(self) -> None:
    """Testing __setitem__ on keys not in slots"""
    A = OrderFull(0, 1, 2, )

    with self.assertRaises(KeyError):
      A['never'] = 420

    with self.assertRaises(KeyError):
      A['gonna'] = 80085

    with self.assertRaises(KeyError):
      A['give'] = 8008135

    with self.assertRaises(KeyError):
      A['you'] = 69

    with self.assertRaises(KeyError):
      A['up'] = 1337

  def test_good_slice_set_item(self) -> None:
    """Test that EZData classes with order=True can be sliced."""
    args = (69, 420, 1337, 80085, 8008135, 69, 420, 1337, 80085, 8008135,)
    keys = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    A = MutableLong()
    B = MutableLong()
    C = MutableLong()
    A[::-1] = (*reversed(args),)
    B[::] = args
    C[::2] = args[::2]
    for a, b in zip(A, B):
      self.assertEqual(a, b)
    for i, slot in enumerate(C):
      if i % 2:
        continue
      self.assertEqual(slot, args[i])

  def test_set_item_slice_str(self) -> None:
    """Tests the special case of setting a slice with a string."""
    A = MutableLong()
    with self.assertRaises(TypeError) as context:
      A[69:420] = 'lol'
    e = context.exception
    self.assertIn("""only to 'str' not to 'bytes' or 'bytearray'""", str(e))

  def test_set_item_slice_len_mismatch(self) -> None:
    """Tests that IndexError raises when setting a slice to an array of
    incompatible length."""
    A = MutableLong()
    with self.assertRaises(IndexError) as context:
      A[0:3] = (69, 420, 1337, 80085)
    e = context.exception
    self.assertIn("""slots cannot be set to""", str(e))

  def test_get_attr_fallback(self) -> None:
    """Test that EZData classes with order=True can use __getattr__."""
    a = OrderFull(1, 2, 3)
    self.assertEqual(a.a, 1)
    self.assertEqual(a.b, 2)
    self.assertEqual(a.c, 3)

    with self.assertRaises(AttributeError):
      _ = a.d

    with self.assertRaises(KeyError):
      _ = a['d']

  def test_set_attr_bad_key(self) -> None:
    """Test that EZData classes correctly raise AttributeError when
    setting an attribute to a key not in the slots."""
    a = OrderFull(1, 2, 3)
    with self.assertRaises(AttributeError):
      a.d = 4

    with self.assertRaises(KeyError):
      a['d'] = 4

  def test_bad_del_item(self) -> None:
    """Test that EZData classes correctly raise TypeError on any deletion
    attempt. """
    A = MutableLong()
    with self.assertRaises(TypeError):
      del A[69]

  def test_as_tuple(self) -> None:
    """Test that EZData classes with order=True can be converted to a
    tuple."""
    A = OrderFull(1, 2, 3)
    self.assertEqual(A.asTuple(), (1, 2, 3))

    B = LongOrder(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    self.assertEqual(B.asTuple(), tuple(range(10)))

    C = MutableLong(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    self.assertEqual(C.asTuple(), tuple(range(10)))

  def test_as_dict(self) -> None:
    """Test that EZData classes with order=True can be converted to a
    dict."""
    A = OrderFull(1, 2, 3)
    self.assertEqual(A.asDict(), {'a': 1, 'b': 2, 'c': 3})

  def test_orderable_mismatch(self) -> None:
    """Test that EZData classes created with keyword argument order=True,
    but also with any slot types that are not orderable, such as
    'complex', raises UnorderedEZException before class creation
    completes. """

    with self.assertRaises(UnorderedEZException) as context:
      class OrderableMismatch(EZData, order=True):
        a: complex = 1 + 2j
        b: int = 2
        c: str = 'three'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderableMismatch')
    self.assertEqual(e.fieldName, 'a')
    self.assertEqual(e.fieldType, complex)

    with self.assertRaises(UnorderedEZException) as context:
      class OrderableMismatch(EZData, order=True):
        b: int = 2
        c: str = 'three'
        a: complex = 1 + 2j  # coverage gymnastics
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'OrderableMismatch')
    self.assertEqual(e.fieldName, 'a')
    self.assertEqual(e.fieldType, complex)

  def test_coverage_gymnastics(self) -> None:
    """Really gotta reach for this one!"""

    class Trololo:
      def __lt__(self, other: Any) -> bool:
        raise WYD

    with self.assertRaises(WYD):
      class Derp(EZData, order=True):
        trololo = Trololo()

  def test_ez_desc(self) -> None:
    """Testing non-bool EZDesc descriptor"""

    class Space:
      __key_args__ = dict()

    class Foo:
      bar = EZDesc('keys, scumbag!', int, 69)
      baz = EZDesc("""it's the universal symbol for keys!""", int, 420)
      bad = EZDesc('wut u doin bro?', int, 'im an int, trust!')
      __namespace__ = Space()

    self.assertEqual(Foo.bar._getKwarg(), 'keys, scumbag!')
    expected = """it's the universal symbol for keys!"""
    self.assertEqual(Foo.baz._getKwarg(), expected)
    self.assertEqual(Foo.bar._getValueType(), int)
    self.assertEqual(Foo.baz._getValueType(), int)
    self.assertEqual(Foo.bar.__default_value__, 69)
    self.assertEqual(Foo.baz.__default_value__, 420)

    foo = Foo()
    self.assertEqual(foo.bar, 69)
    self.assertEqual(foo.baz, 420)

    with self.assertRaises(TypeException) as context:
      _ = foo.bad
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'im an int, trust!')
    self.assertEqual(e.actualType, str)
    self.assertEqual(set(e.expectedTypes), {int, })

  def test_delattr(self) -> None:
    """Test that any EZData class reacts to attribute deletion with
    EZDeleteException."""

    class DelAttr(EZData, frozen=True, order=True):
      a = 0
      b = 1
      c = 2

    with self.assertRaises(EZDeleteException) as context:
      del DelAttr().a
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.cls, DelAttr)
    self.assertEqual(e.name, 'a')
