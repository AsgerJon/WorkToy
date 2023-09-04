"""WorkSide - Widgets - ActSym
Symbolic class representation mouse button actions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.sym import BaseSym, SYM


class ActSym(BaseSym):
  """WorkSide - Widgets - ActSym
  Symbolic class representation mouse button actions."""

  value = 0

  null = SYM.auto()
  null.value = 0

  pressed = SYM.auto()
  pressed.value = 2

  released = SYM.auto()
  released.value = 3

  singleClicked = SYM.auto()
  singleClicked.value = 5

  pressHold = SYM.auto()
  pressHold.value = 7

  doubleClicked = SYM.auto()
  doubleClicked.value = 11

  dropped = SYM.auto()
  dropped.value = 13

  dragged = SYM.auto()
  dragged.value = 17

  tripleClicked = SYM.auto()
  tripleClicked.value = 19

  shake = SYM.auto()
  shake.value = 23

  wheelUp = SYM.auto()
  wheelUp.value = 29

  wheelDown = SYM.auto()
  wheelDown.value = 31

  entered = SYM.auto()
  entered.value = 37

  exited = SYM.auto()
  exited.value = 41

  stopMove = SYM.auto()
  stopMove.value = 43

  startMove = SYM.auto()
  stopMove.value = 47
