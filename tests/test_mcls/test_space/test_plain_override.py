"""
TestPlainOverride pins the behaviour of a subclass that reimplements an
overloaded method as a plain (non-'overload') function. The plain
definition must win: the inherited overloads are dropped rather than
rebuilt into a 'Dispatcher' that would silently shadow the override.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject
from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class Base(BaseObject):
  """Base exposes an overloaded constructor."""

  bar = AttriBox[int](69)

  @overload(int)
  def __init__(self, value: int) -> None:
    self.bar = value

  @overload(str)
  def __init__(self, value: str) -> None:
    try:
      intValue = int(value)
    except (TypeError, ValueError):
      pass
    else:
      self.__init__(intValue)

  @overload()
  def __init__(self) -> None:
    pass


class _Stop(Exception):
  """Marker raised by the plain override to prove it ran."""


class Plain(Base):
  """Plain reimplements '__init__' as an ordinary function."""

  def __init__(self, *args, **kwargs) -> None:
    raise _Stop


class Grand(Plain):
  """Grand adds nothing, inheriting the plain override of 'Plain'."""


class SuperCaller(Base):
  """SuperCaller reimplements '__init__' as a plain function that
  delegates to the overloaded base through 'super'."""

  tag = AttriBox[str]('')

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.tag = 'super'


class TestPlainOverride(MCLSTest):
  """
  TestPlainOverride pins that a plain reimplementation of an overloaded
  method replaces the overloads rather than being silently discarded.
  """

  def test_base_init_is_dispatcher(self) -> None:
    """The overloaded base keeps a 'Dispatcher' for its method."""
    self.assertIsInstance(Base.__dict__['__init__'], Dispatcher)

  def test_override_is_plain_function(self) -> None:
    """The plain override is stored as the function itself, not rebuilt
    into a 'Dispatcher' from the inherited overloads."""
    self.assertIsInstance(Plain.__dict__['__init__'], FunctionType)

  def test_base_overloads_still_work(self) -> None:
    """Overriding in a subclass leaves the base dispatch intact."""
    self.assertEqual(Base().bar, 69)
    self.assertEqual(Base(420).bar, 420)
    self.assertEqual(Base('1337').bar, 1337)
    #  A non-numeric string falls through the base str overload and
    #  leaves the default in place.
    self.assertEqual(Base('not a number').bar, 69)

  def test_override_runs_for_every_call_shape(self) -> None:
    """Every call shape reaches the plain override, regardless of the
    argument types the inherited overloads would have matched."""
    for args in [(), (420,), ('1337',)]:
      with self.assertRaises(_Stop):
        Plain(*args)

  def test_grandchild_inherits_override(self) -> None:
    """A subclass of the override does not resurrect the inherited
    overloads: it inherits the plain function through the MRO."""
    self.assertNotIn('__init__', Grand.__dict__)
    for args in [(), (420,), ('1337',)]:
      with self.assertRaises(_Stop):
        Grand(*args)

  def test_super_dispatch_from_plain_override(self) -> None:
    """A plain override may delegate to the overloaded base through
    'super', and the base dispatch still resolves the arguments."""
    obj = SuperCaller('1337')
    self.assertEqual(obj.bar, 1337)
    self.assertEqual(obj.tag, 'super')
