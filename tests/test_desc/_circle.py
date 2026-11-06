"""
Circle is a worktoy class with a 'Field' read, written and deleted
through methods, and a read-only one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseObject


class Circle(BaseObject):
  """
  A 'Field' computes or guards an attribute through methods of the
  class, found by name at each access. 'Circle' keeps its radius in a
  box, reads it through a getter, writes it through two setters, the
  second of which records every write in 'written', deletes it through
  a deleter, and computes 'area' from it through a getter alone.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  store = AttriBox[float](1.0)
  written = AttriBox[list]([])

  #  Virtual Variables
  radius = Field()
  area = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @radius.GET
  def _getRadius(self) -> float:
    return self.store

  @area.GET
  def _getArea(self) -> float:
    return 3.0 * self.radius * self.radius

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @radius.SET
  def _setRadius(self, value: float) -> None:
    self.store = value

  @radius.SET
  def _noteRadius(self, value: float) -> None:
    self.written.append(value)

  @radius.DELETE
  def _delRadius(self) -> None:
    del self.store
