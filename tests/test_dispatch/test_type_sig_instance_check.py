"""
TestTypeSigInstanceCheck subclasses 'DispatcherTest' and pins that
'TypeSig.validateTypes' refuses an entry that 'isinstance' cannot take,
such as 'typing.Any' or a 'Protocol' that is not runtime checkable, with
'TypeError' at the declaration. Such an entry is a class as far as the
class test goes, so it used to be accepted, and the first call raised the
interpreter's own 'TypeError' from inside the dispatch loop.

'typing.Any' is a class from Python 3.11 on; before that it is no class
and the class test refuses it. 'Protocol' exists from Python 3.8 on. The
mechanism itself is pinned with a class of this file whose metaclass
refuses instance checks, on every version.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from abc import ABC
from typing import Any
from unittest import skipIf

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import TypeSig, overload

from . import DispatcherTest


class _RefusingMeta(type):
  """_RefusingMeta refuses instance checks, as 'typing.Any' does."""

  def __instancecheck__(cls, instance: object) -> bool:
    raise TypeError('%s cannot be used with isinstance()' % cls.__name__)


class Refusing(metaclass=_RefusingMeta):
  """Refusing is a class 'isinstance' cannot take."""


class Abstract(ABC):
  """Abstract is an abstract base class."""


class TestTypeSigInstanceCheck(DispatcherTest):
  """
  TestTypeSigInstanceCheck provides tests for entries 'isinstance' refuses.
  """

  def test_refusing_class_refused(self) -> None:
    """A class whose metaclass refuses instance checks is refused, the
    message naming its position and 'isinstance'."""
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(int, Refusing)
    self.assertIn('position 1', str(context.exception))
    self.assertIn('isinstance', str(context.exception))

  def test_inner_type_refused(self) -> None:
    """The inner type of a trailing 'ARGS' is held to the same rule."""
    with self.assertRaises(TypeError):
      TypeSig.validateTypes(ARGS[Refusing])

  def test_overload_refuses(self) -> None:
    """The refusal reaches the decorator."""
    with self.assertRaises(TypeError):
      overload(Refusing)
    with self.assertRaises(TypeError):
      overload.flex(int, Refusing)

  @skipIf(sys.version_info < (3, 11), "'typing.Any' is no class before 3.11")
  def test_any_refused(self) -> None:
    """'typing.Any' is refused by the instance-check rule."""
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(Any)
    self.assertIn('isinstance', str(context.exception))

  @skipIf(sys.version_info < (3, 8), "'Protocol' exists from 3.8 on")
  def test_protocol(self) -> None:
    """A protocol that is not runtime checkable is refused, and one that
    is passes."""
    from typing import Protocol, runtime_checkable

    class Quiet(Protocol):
      def hush(self) -> None: ...

    @runtime_checkable
    class Loud(Protocol):
      def shout(self) -> None: ...

    with self.assertRaises(TypeError):
      TypeSig.validateTypes(Quiet)
    TypeSig.validateTypes(Loud)

  def test_usable_entries_accepted(self) -> None:
    """An abstract base class, a builtin, 'THIS' and 'ARGS[THIS]' pass."""
    TypeSig.validateTypes(Abstract, int, THIS, ARGS[THIS])
