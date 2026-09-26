"""
TestFlexCallKeywords subclasses 'DispatcherTest' from the
'tests.test_dispatch' package and pins how a 'flexCall' wrapper treats
keyword arguments. The wrapper drops positional arguments beyond those
the wrapped function declares, and refuses a call that leaves a required
positional parameter without a value. A parameter supplied by keyword has
a value, so it does not count as missing, while a positional-only
parameter still takes its value by position alone, as the wrapped
function itself insists. The wrapper also carries the attributes set on
the wrapped function.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from unittest import skipIf

from worktoy.dispatch import flexCall, isFlex

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable

#  The positional-only marker of Python 3.8 cannot appear directly in a
#  file that must still parse on Python 3.7.
_POSITIONAL_ONLY = """
def positionalOnly(a, /, b):
  return a, b
"""


def _binary(a: Any, b: Any) -> tuple:
  """The '_binary' function takes two required parameters."""
  return a, b


def _ternary(a: Any, b: Any, c: Any = 10) -> tuple:
  """The '_ternary' function takes two required parameters and one with a
  default."""
  return a, b, c


def _positionalOnly() -> Callable:
  """The '_positionalOnly' function compiles a function whose first
  parameter is positional-only and returns it."""
  namespace = dict()
  exec(_POSITIONAL_ONLY, namespace)
  return namespace['positionalOnly']


class TestFlexCallKeywords(DispatcherTest):
  """
  TestFlexCallKeywords provides tests for keyword arguments and function
  attributes on 'flexCall' wrappers.
  """

  def test_every_parameter_by_keyword(self) -> None:
    """Both required parameters receive their values by keyword."""
    self.assertEqual(flexCall(_binary)(a=1, b=2), (1, 2))

  def test_last_parameter_by_keyword(self) -> None:
    """The first parameter receives its value by position and the second
    by keyword."""
    self.assertEqual(flexCall(_binary)(1, b=2), (1, 2))

  def test_keywords_with_default(self) -> None:
    """Keywords supply the required parameters of a function with a
    defaulted one, which keeps its default unless named too."""
    wrapped = flexCall(_ternary)
    self.assertEqual(wrapped(1, b=2), (1, 2, 10))
    self.assertEqual(wrapped(a=1, b=2, c=3), (1, 2, 3))

  def test_missing_lists_only_absent_parameters(self) -> None:
    """The error for a missing parameter names that parameter alone, not
    the ones supplied by keyword."""
    with self.assertRaises(TypeError) as context:
      flexCall(_binary)(b=2)
    message = str(context.exception)
    self.assertIn('(a)', message)
    self.assertNotIn('a and b', message)

  def test_missing_despite_unknown_keyword(self) -> None:
    """A keyword naming no parameter does not stand in for a missing
    one, and the error names the missing parameter."""
    with self.assertRaises(TypeError) as context:
      flexCall(_binary)(1, c=3)
    self.assertIn('(b)', str(context.exception))

  @skipIf(sys.version_info < (3, 8), 'positional-only needs Python 3.8')
  def test_positional_only_by_position(self) -> None:
    """A positional-only parameter receives its value by position while
    the next one receives its value by keyword."""
    wrapped = flexCall(_positionalOnly())
    self.assertEqual(wrapped(1, b=2), (1, 2))

  @skipIf(sys.version_info < (3, 8), 'positional-only needs Python 3.8')
  def test_positional_only_by_keyword_raises(self) -> None:
    """A keyword naming a positional-only parameter does not supply it,
    so the call raises 'TypeError', which the wrapped function raises
    itself."""
    wrapped = flexCall(_positionalOnly())
    with self.assertRaises(TypeError):
      wrapped(a=1, b=2)

  def test_function_attribute_carried(self) -> None:
    """An attribute set on the wrapped function is readable on the
    wrapper."""

    def tagged(a: Any) -> Any:
      return a

    tagged.tag = 'kept'
    wrapped = flexCall(tagged)
    self.assertEqual(wrapped.tag, 'kept')
    self.assertEqual(wrapped(69, 420), 69)

  def test_wrapper_attributes_win(self) -> None:
    """Where the attributes of the wrapped function share a name with
    those the wrapper sets itself, the wrapper keeps its own. A function
    already wrapped by another decorator carries '__wrapped__', which
    must still lead back to the function 'flexCall' received."""

    def inner(a: Any) -> Any:
      return a

    def outer(a: Any) -> Any:
      return inner(a)

    outer.__wrapped__ = inner
    wrapped = flexCall(outer)
    self.assertIs(wrapped.__wrapped__, outer)
    self.assertTrue(isFlex(wrapped))
    self.assertEqual(wrapped(69, 420), 69)
