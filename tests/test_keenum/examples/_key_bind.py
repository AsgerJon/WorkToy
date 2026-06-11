"""
KeyBind subclasses 'BaseObject' and provides an example use of 'KeeBox'
descriptors.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.keenum import KeeBox
from . import KeyboardModifier, KeyboardKeyNum

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeyBind(BaseObject):
  """
  KeyBind is an example of a class that uses 'KeeBox' descriptors to define
  its attributes.

  Attributes
  ----------
  mod : KeyboardModifier
    The keyboard modifier (e.g., Shift, Ctrl, Alt).

  key : KeyboardKeyNum
    The key on the keyboard (e.g., A, B, C).

  Examples
  --------
  >>> kb1 = KeyBind(KeyboardModifier.SHIFT, KeyboardKeyNum.A)
  >>> print(kb1)
  SHIFT+A
  >>> kb2 = KeyBind(KeyboardKeyNum.B)
  >>> print(kb2)
  B
  >>> kb3 = KeyBind("CTRL+C")
  >>> print(kb3)
  CTRL+C
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  mod = KeeBox[KeyboardModifier]()
  key = KeeBox[KeyboardKeyNum]()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload.flex(KeyboardModifier, KeyboardKeyNum)
  def __init__(self, _mod: KeyboardModifier, _key: KeyboardKeyNum) -> None:
    self.key, self.mod = _key, _mod

  @overload(KeyboardKeyNum)
  def __init__(self, _key: KeyboardKeyNum) -> None:
    self.key = _key

  @overload(str)
  def __init__(self, _keyBindStr: str) -> None:
    modStr, keyStr = _keyBindStr.split('+')
    self.mod = KeyboardModifier[modStr]
    self.key = KeyboardKeyNum[keyStr]

  @overload()
  def __init__(self) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self) -> str:
    if self.mod:
      infoSpec = """%s+%s"""
    else:
      infoSpec = """%s%s"""
    modStr = self.mod.name if self.mod else ''
    keyStr = self.key.name
    return infoSpec % (modStr, keyStr)

  def __repr__(self) -> str:
    if self.mod:
      infoSpec = """%s(%s, %s)"""
    else:
      infoSpec = """%s(%s%s)"""
    clsName = type(self).__name__
    modStr = self.mod.name if self.mod else ''
    keyStr = self.key.name
    return infoSpec % (clsName, keyStr, modStr,)
