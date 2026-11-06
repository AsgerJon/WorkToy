"""
Watched is a worktoy class whose box carries all six access callbacks,
of three kinds of method.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject


class Watched(BaseObject):
  """
  A class reacts to the accesses of its descriptor through methods the
  notification decorators register by name, each called by the kind of
  method the class holds at that name. 'Watched' registers the six
  access callbacks as a plain method, a classmethod, a staticmethod and
  a private method whose name Python mangles, and records every call in
  'log'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  log: list = []

  #  Public Variables
  value = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @value.preGet
  def _beforeRead(self) -> None:
    Watched.log.append(('preGet', type(self).__name__))

  @value.onGet
  def _afterRead(self, value: int) -> None:
    Watched.log.append(('onGet', value))

  @value.preSet
  @classmethod
  def _beforeWrite(cls, value: int) -> None:
    Watched.log.append(('preSet', cls.__name__, value))

  @value.onSet
  @staticmethod
  def _afterWrite(value: int) -> None:
    Watched.log.append(('onSet', value))

  @value.preDelete
  def __beforeDelete(self) -> None:
    Watched.log.append(('preDelete',))

  @value.onDelete
  def _afterDelete(self) -> None:
    Watched.log.append(('onDelete',))
