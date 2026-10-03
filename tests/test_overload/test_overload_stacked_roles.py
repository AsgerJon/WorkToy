"""
TestOverloadStackedRoles subclasses 'OverloadTest' and pins that
'@overload' stacks with '@overload.flex', '@overload.fallback' and
'@overload.finalize', in either order. A stack decorates one function, and
each decorator in it adds one role for that function. Every such stack
failed: an '@overload' on a fallback or a finalizer raised a bare
'RuntimeError', one on a 'flex' registered the wrapper of the other
arity, so the shorter call failed when made, and a role decorator on an
'@overload' took the 'overload' object for the function.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


class Money(BaseObject):
  """Money reads text and anything else through one function."""

  cents = AttriBox[int](0)

  @overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @overload(str)
  @overload.fallback
  def __init__(self, value: object) -> None:
    self.cents = round(float(str(value)) * 100)


class FlippedMoney(BaseObject):
  """FlippedMoney stacks the same two decorators the other way around."""

  cents = AttriBox[int](0)

  @overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @overload.fallback
  @overload(str)
  def __init__(self, value: object) -> None:
    self.cents = round(float(str(value)) * 100)


class Label(BaseObject):
  """Label takes a lone text, or a text and a size in either order."""

  text = AttriBox[str]('')
  size = AttriBox[int](12)

  @overload(str)
  @overload.flex(str, int)
  def __init__(self, text: str, size: int = 12) -> None:
    self.text = text
    self.size = size


class FlippedLabel(BaseObject):
  """FlippedLabel stacks the same two decorators the other way around."""

  text = AttriBox[str]('')
  size = AttriBox[int](12)

  @overload.flex(str, int)
  @overload(str)
  def __init__(self, text: str, size: int = 12) -> None:
    self.text = text
    self.size = size


class Ticker(BaseObject):
  """Ticker records each call, as the method and as its finalizer."""

  calls = AttriBox[list]()

  @overload(int)
  @overload.finalize
  def tick(self, *args) -> None:
    self.calls.append(args)


class FlippedTicker(BaseObject):
  """FlippedTicker stacks the same two decorators the other way around."""

  calls = AttriBox[list]()

  @overload.finalize
  @overload(int)
  def tick(self, *args) -> None:
    self.calls.append(args)


class TestOverloadStackedRoles(OverloadTest):
  """
  TestOverloadStackedRoles provides tests for '@overload' stacked with
  the role decorators.
  """

  def test_fallback_stack(self) -> None:
    """One function is the 'str' overload and the fallback."""
    for cls in (Money, FlippedMoney):
      with self.subTest(cls=cls.__name__):
        self.assertEqual(cls(5).cents, 5)
        self.assertEqual(cls('12.50').cents, 1250)
        self.assertEqual(cls(1.5).cents, 150)
        #  Text the 'int' overload could cast reaches the 'str' overload.
        self.assertEqual(cls('12').cents, 1200)

  def test_flex_stack(self) -> None:
    """One function takes a lone text, and a text and a size."""
    for cls in (Label, FlippedLabel):
      with self.subTest(cls=cls.__name__):
        lone = cls('Hello')
        self.assertEqual((lone.text, lone.size), ('Hello', 12))
        pair = cls('Hello', 14)
        self.assertEqual((pair.text, pair.size), ('Hello', 14))
        flipped = cls(14, 'Hello')
        self.assertEqual((flipped.text, flipped.size), ('Hello', 14))

  def test_finalize_stack(self) -> None:
    """One function is the 'int' overload and the finalizer."""
    for cls in (Ticker, FlippedTicker):
      with self.subTest(cls=cls.__name__):
        ticker = cls()
        ticker.tick(1)
        self.assertEqual(ticker.calls, [(1,), (1,)])
        with self.assertRaises(DispatchException):
          ticker.tick('x')
        self.assertEqual(ticker.calls, [(1,), (1,), ('x',)])

  def test_str_names_roles(self) -> None:
    """The 'str()' of a stacked overload lists every role."""

    def parse(self, value: object) -> object:
      """A function stacked as the 'str' overload and the fallback."""
      return value

    self.assertIsNone(parse(None, None))
    stacked = overload(str)(overload.fallback(parse))
    info = str(stacked)
    self.assertIn('parse', info)
    self.assertIn('<TypeSig: [str]>', info)
    self.assertIn('fallback', info)
