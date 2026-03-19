"""
InlineLink subclasses 'InlineBase' and encapsulates a link to another
place in the present document or to an external URL.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import THIS
from ..utilities import textFmt, maybe
from ..desc import Field, AttriBox
from ..dispatch import overload
from . import InlineText, InlineBase
from ..waitaminute.desc import ProtectedError

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Any, Self, Iterator

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  StrBox: TypeAlias = Union[str, AttriBox]


class InlineLink(InlineBase):
  """
  InlineLink subclasses 'InlineBase' and encapsulates a link to another
  place in the present document or to an external URL.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __tool_tip__: MaybeStr = None
  __link_text__: MaybeStr = None

  #  Public Variables
  url: StrBox = AttriBox[str]()
  linkText: StrField = Field()
  toolTip: StrField = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @linkText.GET
  def _getLinkText(self) -> str:
    return maybe(self.__link_text__, self.url)

  @toolTip.GET
  def _getToolTip(self) -> str:
    return maybe(self.__tool_tip__, self.linkText)

  def getText(self, ) -> str:
    if str.startswith(self.url, 'http'):
      infoSpec = """[%s](%s "%s")"""
      infoSpec = """<a href="%s" title="%s">%s</a>"""
    else:
      infoSpec = """[%s](#%s "%s")"""
      infoSpec = """<a href="#%s" title="%s">%s</a>"""
    return infoSpec % (self.url, self.toolTip, self.linkText)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @linkText.SET
  def _setLinkText(self, value: str) -> None:
    self.__link_text__ = value

  @toolTip.SET
  def _setToolTip(self, value: str) -> None:
    self.__tool_tip__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @url.preDelete
  def _protect(self, ) -> None:
    raise ProtectedError(self, getattr(type(self), 'url'), self.url)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.url = other.url
    self.linkText = other.linkText
    self.toolTip = other.toolTip

  @overload(str, str, str)
  def __init__(self, url: str, linkText: str, tip: str) -> None:
    self.url = url
    self.linkText = linkText
    self.toolTip = tip

  @overload(str, str)
  def __init__(self, url: str, linkText: str) -> None:
    self.url = url
    self.linkText = linkText

  @overload(str)
  def __init__(self, url: str) -> None:
    self.url = url

  @overload()
  def __init__(self) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  OPTIONAL METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  REQUIRED METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
