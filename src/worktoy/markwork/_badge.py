"""
Badge subclasses 'InlineText' and provides Markdown badges.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import THIS
from ..desc import AttriBox, Field
from ..dispatch import overload
from ..utilities import maybe
from . import InlineBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Self

  MaybeStr: TypeAlias = Optional[str]
  StrBox: TypeAlias = Union[str, AttriBox]
  StrField: TypeAlias = Union[str, Field]


class Badge(InlineBase):
  """
  Badge subclasses 'InlineText' and provides Markdown badges.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __alt_text__: MaybeStr = None

  #  Public Variables
  imgUrl: StrBox = AttriBox[str]('')
  altText: StrField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @altText.GET
  def _getAltText(self) -> str:
    return maybe(self.__alt_text__, self.imgUrl)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @altText.SET
  def _setAltText(self, value: str) -> None:
    self.__alt_text__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getText(self) -> str:
    """
    Returns the syntax for an inline image in Markdown
    """
    # infoSpec = """![%s](%s)"""
    infoSpec = """<img alt="%s" src="%s">"""
    return infoSpec % (self.altText, self.imgUrl)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.imgUrl = other.imgUrl
    self.altText = other.altText

  @overload(str, str)
  def __init__(self, url: str, alt: str) -> None:
    self.imgUrl = url
    self.altText = alt

  @overload(str)
  def __init__(self, url: str) -> None:
    self.imgUrl = url

  @overload()
  def __init__(self) -> None:
    pass
