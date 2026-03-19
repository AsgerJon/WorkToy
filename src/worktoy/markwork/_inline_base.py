"""
InlineBase subclasses 'BaseObject' and provides the base class for all
inline components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import maybe, textFmt
from ..desc import Field
from ..mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Type

  from . import Block

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]


class InlineBase(BaseObject):
  """
  InlineBase subclasses 'BaseObject' and provides the base class for all
  inline components.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_text__: str = ''

  #  Private Variables
  __inline_text__: MaybeStr = None

  #  Public Variables
  text: StrField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @text.GET
  def getText(self) -> str:
    """
    The getter function for the actual text that should represent this
    instance. It is this method that subclasses should override as
    appropriate.
    """
    return maybe(self.__inline_text__, self.__fallback_text__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @text.SET
  def _setText(self, value: str) -> None:
    self.__inline_text__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, blockType: Type[Block], name: str, ) -> None:
    super().__set_name__(blockType, name)
    blockType.registerInline(self, name, )

  def __str__(self) -> str:
    infoSpec = """<%s: %s>"""
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, self.text))

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s)"""
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, self.text))

  def __bool__(self) -> bool:
    for _ in self.text:
      break
    else:
      return False
    return True
