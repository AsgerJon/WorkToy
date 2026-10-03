"""
TestDispatcherStackedDecorators subclasses 'DispatcherTest' and pins that
the decorators of a 'Dispatcher' wired by hand stack, as the 'overload'
decorators of a 'BaseObject' do. Each of 'overload', 'flex', 'fallback'
and 'finalize' returns the dispatcher, so a decorator stacked above
another received the dispatcher itself and registered it as the body of
its signature, or as the fallback or the finalizer. A call reaching it
raised "'Dispatcher' object is not callable", and a fallback or a
finalizer on top raised as the class was created.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.dispatch import DispatchException

from . import DispatcherTest


class Temperature:
  """Temperature in degrees Celsius, from a number or from a label."""

  __init__ = Dispatcher()

  @__init__.overload(float)
  @__init__.overload(int)
  def __init__(self, degrees: float) -> None:
    self.degrees = float(degrees)
    self.label = '%.1f C' % self.degrees

  @__init__.overload(str)
  def __init__(self, label: str) -> None:
    self.label = label
    self.degrees = 0.0


class Money:
  """Money reads text and anything else through one function."""

  __init__ = Dispatcher()

  @__init__.overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @__init__.overload(str)
  @__init__.fallback
  def __init__(self, value: object) -> None:
    self.cents = round(float(str(value)) * 100)


class FlippedMoney:
  """FlippedMoney stacks the same two decorators the other way around."""

  __init__ = Dispatcher()

  @__init__.overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @__init__.fallback
  @__init__.overload(str)
  def __init__(self, value: object) -> None:
    self.cents = round(float(str(value)) * 100)


class Label:
  """Label takes a lone text, or a text and a size in either order."""

  __init__ = Dispatcher()

  @__init__.overload(str)
  @__init__.flex(str, int)
  def __init__(self, text: str, size: int = 12) -> None:
    self.text = text
    self.size = size


class FlippedLabel:
  """FlippedLabel stacks the same two decorators the other way around."""

  __init__ = Dispatcher()

  @__init__.flex(str, int)
  @__init__.overload(str)
  def __init__(self, text: str, size: int = 12) -> None:
    self.text = text
    self.size = size


class Ticker:
  """Ticker records each call, as the method and as its finalizer."""

  tick = Dispatcher()

  @tick.overload(int)
  @tick.finalize
  def tick(self, *args) -> None:
    self.calls.append(args)

  def __init__(self, ) -> None:
    self.calls = []


class FlippedTicker:
  """FlippedTicker stacks the same two decorators the other way around."""

  tick = Dispatcher()

  @tick.finalize
  @tick.overload(int)
  def tick(self, *args) -> None:
    self.calls.append(args)

  def __init__(self, ) -> None:
    self.calls = []


class TestDispatcherStackedDecorators(DispatcherTest):
  """
  TestDispatcherStackedDecorators provides tests for stacking the
  decorators of a 'Dispatcher'.
  """

  def test_overload_stack(self) -> None:
    """Stacked signatures share one body, beside a later stack."""
    self.assertEqual(Temperature(20).degrees, 20.0)
    self.assertEqual(Temperature(20.5).degrees, 20.5)
    self.assertEqual(Temperature(20.5).label, '20.5 C')
    self.assertEqual(Temperature('warm').label, 'warm')

  def test_fallback_stack(self) -> None:
    """One function is the 'str' overload and the fallback."""
    for cls in (Money, FlippedMoney):
      with self.subTest(cls=cls.__name__):
        self.assertEqual(cls(5).cents, 5)
        self.assertEqual(cls('12').cents, 1200)
        self.assertEqual(cls(1.5).cents, 150)

  def test_flex_stack(self) -> None:
    """One function takes a lone text, and a text and a size."""
    for cls in (Label, FlippedLabel):
      with self.subTest(cls=cls.__name__):
        lone = cls('Hello')
        self.assertEqual((lone.text, lone.size), ('Hello', 12))
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

  def test_itself_before_any_function(self) -> None:
    """Given itself before any function, a decorator has none to use."""
    dispatcher = Dispatcher()
    with self.assertRaises(MissingVariable):
      dispatcher.fallback(dispatcher)
