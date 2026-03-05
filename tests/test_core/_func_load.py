"""
FuncLoad is a class that can be instantiated with several type signatures
including a function type signature. It is used to test the overload
mechanism in the dispatch module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import Function
from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.dispatch import overload

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class FuncLoad(BaseObject):
  """
  FuncLoad is a class that can be instantiated with several type signatures
  including a function type signature. It is used to test the overload
  mechanism in the dispatch module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __init_object__ = None
  __init_load__ = None

  #  Public Variables
  init = Field()
  load = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @init.GET
  def _getInitObject(self) -> Any:
    return self.__init_object__

  @load.GET
  def _getInitLoad(self) -> bool:
    return True if self.__init_load__ else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  @overload(str)
  @overload(float)
  def __init__(self, *args, ) -> None:
    self.__init_object__ = args[0]
    self.__init_load__ = False

  @overload(Function)
  def __init__(self, func: Function, ) -> None:
    self.__init_object__ = func
    self.__init_load__ = True
