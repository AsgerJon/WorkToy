"""
TestStrictLoad tests the keyword argument 'strict' in the 'overload'
decorator. When 'strict' is set to True, the overload will only match the
exact type signature, and will not allow for flexible matching or type
casting.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject
from worktoy.dispatch import overload
from worktoy.waitaminute.dispatch import DispatchException
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class Chill(BaseObject):

  @overload()
  def __init__(self, ) -> None:
    self.value = 69

  @overload(int)
  def __init__(self, value: int) -> None:
    self.value = value


class OkBro(BaseObject):

  @overload()
  def __init__(self, ) -> None:
    self.value = 420

  @overload(int, strict=True)
  def __init__(self, value: int) -> None:
    self.value = value


class TestStrictLoad(OverloadTest):
  """
  TestStrictLoad tests the keyword argument 'strict' in the 'overload'
  decorator. When 'strict' is set to True, the overload will only match the
  exact type signature, and will not allow for flexible matching or type
  casting.
  """

  def test_init(self) -> None:
    """Tests the initialization of the Chill and OkBro classes."""

    chill = Chill('420')
    chill2 = Chill()
    self.assertEqual(chill.value, 420)
    self.assertEqual(chill2.value, 69)
    okBro = OkBro(False)  # subclass of int
    okBro2 = OkBro()
    self.assertEqual(okBro.value, False)
    self.assertEqual(okBro2.value, 420)

    with self.assertRaises(DispatchException) as context:
      okBro = OkBro('1337')
    e = context.exception
    self.assertIs(e.dispatch, OkBro.__init__)
