"""
TestBasePrecedence subclasses 'OverloadTest' and pins how a class with
several bases combines the overloads it inherits under one name. Distinct
signatures from different bases merge into a single dispatcher, so the
class accepts every call any of its bases accepts. Where two bases
register an equal signature, the base that comes first in the method
resolution order wins, in every dispatch pass alike. A plain method
earlier in the method resolution order shadows overloads that only later
bases contribute, just as it would shadow any other attribute.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject
from . import OverloadTest


class Left(BaseObject):
  """Left registers the overloads that must win every collision, since
  it is the first base of 'Both'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def name(self, n: int) -> str:
    return 'left'

  @overload(int, *ARGS[int])
  def total(self, *values: int) -> str:
    return 'left'

  @overload(int)
  def merge(self, n: int) -> str:
    return 'left'


class Right(BaseObject):
  """Right registers an equal signature for 'name' and 'total', and a
  different signature for 'merge'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def name(self, n: int) -> str:
    return 'right'  # pragma: no cover

  @overload(int, *ARGS[int])
  def total(self, *values: int) -> str:
    return 'right'  # pragma: no cover

  @overload(str)
  def merge(self, s: str) -> str:
    return 'right'


class Both(Left, Right):
  """Both inherits from 'Left' first and 'Right' second, and declares
  nothing of its own."""


class Plain(BaseObject):
  """Plain defines 'name' as a plain method, with no overloads."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def name(self, n: int) -> str:
    return 'plain'


class PlainFirst(Plain, Right):
  """PlainFirst places the plain 'Plain.name' ahead of the overloaded
  'Right.name' in its method resolution order."""


class Loud(Right):
  """Loud overrides the overloaded 'Right.name' with a plain method."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def name(self, n: int) -> str:
    return 'loud'


class LoudRight(Loud, Right):
  """LoudRight lists both 'Loud' and the class it overrides as bases,
  forming a diamond. The method resolution order visits 'Loud' before
  'Right', so the plain override comes first."""


class Manual(BaseObject):
  """Manual defines 'name' through a 'Dispatcher' written in its class
  body rather than through '@overload'. The class body holds the
  'Dispatcher' as it would hold a plain method."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  name = Dispatcher()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.overload(int)
  def name(self, n: int) -> str:
    return 'manual'


class ManualFirst(Manual, Right):
  """ManualFirst places the body-written 'Dispatcher' of 'Manual' ahead
  of the overloaded 'Right.name' in its method resolution order."""


class Foreign:
  """Foreign is an ordinary class, not built by 'BaseMeta', holding a
  'Dispatcher' under 'name'."""

  name = Dispatcher()

  @name.overload(int)
  def name(self, n: int) -> str:
    return 'foreign'


class ForeignFirst(Foreign, Right):
  """ForeignFirst places the 'Dispatcher' of the ordinary class 'Foreign'
  ahead of the overloaded 'Right.name' in its method resolution
  order."""


class TestBasePrecedence(OverloadTest):
  """
  TestBasePrecedence pins merging, first-base precedence on collisions,
  and shadowing by plain methods, for classes with several bases.
  """

  def setUp(self) -> None:
    """
    The long call exceeds the number of variadic lengths the overload
    decorator expands into exact signatures, so it can only be matched
    by walking the variadic signatures.
    """
    super().setUp()
    self.longCall = (*range(overload.__variadic_fastpath_limit__ + 2),)

  def test_distinct_signatures_merge(self) -> None:
    """
    Testing that signatures differing between the bases both remain
    available: an 'int' call reaches 'Left' and a 'str' call reaches
    'Right'.
    """
    self.assertEqual(Both().merge(1), 'left')
    self.assertEqual(Both().merge('one'), 'right')

  def test_first_base_wins_exact_signature(self) -> None:
    """
    Testing that the first base wins an equal signature matched by exact
    lookup, as it would win a plain method of the same name.
    """
    self.assertEqual(Both().name(1), 'left')

  def test_first_base_wins_every_variadic_length(self) -> None:
    """
    Testing that the first base wins an equal variadic signature for
    short calls and for calls too long for the expanded signatures
    alike, so the winner does not change with the length of the call.
    """
    self.assertEqual(Both().total(1, 2), 'left')
    self.assertEqual(Both().total(*self.longCall), 'left')

  def test_plain_method_in_first_base_shadows(self) -> None:
    """
    Testing that a plain method in the first base shadows overloads
    contributed only by a later base.
    """
    self.assertEqual(PlainFirst().name(1), 'plain')

  def test_plain_override_in_diamond_shadows(self) -> None:
    """
    Testing that a plain override keeps shadowing the overloads it
    overrides when a subclass also lists the overridden class as a
    base.
    """
    self.assertEqual(Loud().name(1), 'loud')
    self.assertEqual(LoudRight().name(1), 'loud')

  def test_body_written_dispatcher_shadows(self) -> None:
    """
    Testing that a 'Dispatcher' written in the body of the first base
    shadows the overloads of a later base, just as a plain method would.
    Only a 'Dispatcher' built from '@overload' declarations lets
    overloads from further classes merge in.
    """
    self.assertEqual(ManualFirst().name(1), 'manual')

  def test_foreign_dispatcher_shadows(self) -> None:
    """
    Testing that a 'Dispatcher' held by an ordinary class shadows the
    overloads of a later base as well.
    """
    self.assertEqual(ForeignFirst().name(1), 'foreign')
