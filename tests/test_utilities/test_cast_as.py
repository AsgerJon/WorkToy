"""
TestCastAs subclasses 'UtilitiesTest' and pins the '__cast_as__' protocol
of 'typeCast'. Outside the two builtin families nothing converts unless
the target class declares a classmethod '__cast_as__(cls, value)', which
returns an instance of the class or 'NotImplemented' to refuse. A
subclass of a builtin, an 'IntEnum' and any other class are refused until
they declare it, no constructor is ever called on the value, and a hook
that is not a classmethod is refused with 'UnboundCastHook' rather than
run with the value bound as 'self'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from worktoy.utilities import typeCast, hasCastRule
from worktoy.waitaminute.dispatch import TypeCastException, UnboundCastHook

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Count(int):
  """Count leans on the number family and builds itself from the
  result."""

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    return cls(typeCast(int, value))


class Tally(Count):
  """Tally inherits the hook of 'Count' and gets instances of itself."""


class Picky:
  """Picky takes upper-case text and refuses everything else."""

  def __init__(self, text: str) -> None:
    self.text = text

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    if isinstance(value, str) and value.isupper():
      return cls(value)
    return NotImplemented


class Shifty:
  """Shifty answers with something that is no 'Shifty'."""

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    return 42


class Plain:
  """Plain declares no hook, and its constructor must never be asked."""

  def __init__(self, value: Any) -> None:
    raise AssertionError('constructor called')  # pragma: no cover


class Unbound:
  """Unbound defines the hook as a plain function."""

  def __cast_as__(self, value: Any) -> Any:
    return self  # pragma: no cover


class Static:
  """Static defines the hook as a staticmethod."""

  @staticmethod
  def __cast_as__(value: Any) -> Any:
    return Static()  # pragma: no cover


class Level(IntEnum):
  """Level is a subclass of 'int' without a hook."""

  LOW = 1
  HIGH = 2


class TestCastAs(UtilitiesTest):
  """
  TestCastAs provides tests for the '__cast_as__' protocol of 'typeCast'.
  """

  def test_hook_casts(self) -> None:
    """The hook turns a foreign value into an instance of the class."""
    cast = typeCast(Count, 2.0)
    self.assertIs(type(cast), Count)
    self.assertEqual(cast, 2)
    cast = typeCast(Count, True)
    self.assertIs(type(cast), Count)
    self.assertEqual(cast, 1)

  def test_hook_refuses_through_the_family(self) -> None:
    """A value the family rule the hook leans on refuses is refused."""
    for value in (2.5, '2', None):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeCastException):
          typeCast(Count, value)

  def test_not_implemented_refuses(self) -> None:
    """'NotImplemented' from the hook is a refusal, naming the target and
    the value."""
    self.assertEqual(typeCast(Picky, 'UPPER').text, 'UPPER')
    for value in ('lower', 5, None):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeCastException) as context:
          typeCast(Picky, value)
        self.assertIs(context.exception.type_, Picky)
        self.assertEqual(context.exception.arg, value)

  def test_result_must_be_an_instance(self) -> None:
    """A hook answering with something other than an instance of the
    class is refused."""
    with self.assertRaises(TypeCastException):
      typeCast(Shifty, 'x')

  def test_instance_skips_the_hook(self) -> None:
    """A value already an instance is returned as it is, whatever the
    hook would say about it."""
    picky = Picky('lower')
    self.assertIs(typeCast(Picky, picky), picky)

  def test_hook_inherited_builds_the_subclass(self) -> None:
    """Bound to 'cls', an inherited hook builds the subclass it is looked
    up on."""
    cast = typeCast(Tally, 3.0)
    self.assertIs(type(cast), Tally)
    self.assertEqual(cast, 3)

  def test_no_hook_refused(self) -> None:
    """Without a hook a class, a subclass of a builtin and an 'IntEnum'
    accept their own instances and nothing else; no constructor runs."""
    with self.assertRaises(TypeCastException):
      typeCast(Plain, 5)
    for value in (1, 1.0, True):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeCastException):
          typeCast(Level, value)
    self.assertIs(typeCast(Level, Level.LOW), Level.LOW)

  def test_unbound_hook_refused(self) -> None:
    """A hook that is not a classmethod raises 'UnboundCastHook', which
    is no 'TypeError', so the cast passes of an overloaded method cannot
    mistake it for a signature that merely failed to match."""
    for target in (Unbound, Static):
      with self.subTest(target=target.__name__):
        with self.assertRaises(UnboundCastHook) as context:
          typeCast(target, 'x')
        e = context.exception
        self.assertNotIsInstance(e, TypeError)
        self.assertEqual(e.className, target.__name__)
        self.assertIn('@classmethod', str(e))
        self.assertEqual(str(e), e.msg)

  def test_unbound_hook_inherited_names_both(self) -> None:
    """An unbound hook found on a base names the base and the class
    being cast to."""

    class Heir(Unbound):
      pass

    with self.assertRaises(UnboundCastHook) as context:
      typeCast(Heir, 'x')
    self.assertEqual(context.exception.className, 'Unbound')
    self.assertEqual(context.exception.targetName, 'Heir')
    self.assertIn('Heir', str(context.exception))

  def test_has_cast_rule(self) -> None:
    """'hasCastRule' answers 'True' for the family builtins, their
    subclasses and classes declaring the hook, and 'False' otherwise."""
    for target in (bool, int, float, complex, str, bytes, bytearray,
                   Count, Level, Picky):
      with self.subTest(target=target.__name__):
        self.assertTrue(hasCastRule(target))
    for target in (Plain, slice, list, dict, object, type):
      with self.subTest(target=target.__name__):
        self.assertFalse(hasCastRule(target))
    with self.assertRaises(UnboundCastHook):
      hasCastRule(Unbound)
