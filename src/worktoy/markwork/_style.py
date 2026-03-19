"""
Style subclasses 'BaseObject' and encapsulates the HTML tags used to style
other components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import operator
from typing import TYPE_CHECKING

from . import HeaderNum
from ..core.sentinels import THIS
from ..desc import AttriBox
from ..dispatch import overload
from ..keenum import KeeBox
from ..mcls import BaseObject
from ..utilities import joinWords, textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable, Type, Self
  from . import ParagraphBlock

  BoolBox: TypeAlias = Union[bool, AttriBox]
  HeaderBox: TypeAlias = Union[HeaderNum, KeeBox]


class Style(BaseObject):
  """
  Style subclasses 'BaseObject' and encapsulates the HTML tags used to style
  other components.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __italic_keys__ = (
    'italic',
    'italics',
    'emphasis',
    'emphasize',
    'emphasized',
    'emph',
    'em',
    )
  __bold_keys__ = (
    'bold',
    'strong',
    'strongly',
    'stronger',
    'strongest',
    'b',
    )
  __underline_keys__ = (
    'underline',
    'underlined',
    'underlining',
    'u',
    )
  __strikethrough_keys__ = (
    'strikethrough',
    'strikethru',
    'struckthrough',
    'struckthru',
    's',
    'strike',
    'del',
    'deletion',
    'deleted',
    )
  __key_groups__ = dict(
    italic=__italic_keys__,
    bold=__bold_keys__,
    underline=__underline_keys__,
    strikethrough=__strikethrough_keys__,
    )
  __key_types__ = dict(
    italic=bool,
    bold=bool,
    underline=bool,
    strikethrough=bool,
    )
  __key_defaults__ = dict(
    italic=False,
    bold=False,
    underline=False,
    strikethrough=False,
    )

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  italic: BoolBox = AttriBox[bool](False)
  bold: BoolBox = AttriBox[bool](False)
  underline: BoolBox = AttriBox[bool](False)
  strikethrough: BoolBox = AttriBox[bool](False)

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    infoSpec = """<%s: %s>"""
    keys = self.__key_groups__.keys()
    values = (*(getattr(self, key) for key in keys),)
    attrs = joinWords(*('%s=%s' % (k, v) for k, v in zip(keys, values)))
    return textFmt(infoSpec % (type(self).__name__, attrs))

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s)"""
    keys = self.__key_groups__.keys()
    values = (*(getattr(self, key) for key in keys),)
    attrs = joinWords(*('%s=%s' % (k, v) for k, v in zip(keys, values)))
    return textFmt(infoSpec % (type(self).__name__, attrs))

  def __getitem__(self, key: str) -> bool:
    for name, keys in self.__key_groups__.items():
      if key in keys:
        return getattr(self, name)
    raise KeyError(key)

  def __setitem__(self, key: str, value: bool) -> None:
    keyGroups = self.__key_groups__.items()
    for (name, keys) in keyGroups:
      type_ = self.__key_types__[name]
      if key in keys:
        if not isinstance(value, type_):
          raise TypeException(name, value, type_)
        return setattr(self, name, value)
    else:
      raise KeyError(key)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(bool, bool, bool, bool)
  def __init__(
      self,
      italic: bool,
      bold: bool,
      underline: bool,
      strikethrough: bool,
      **_,
      ) -> None:
    self.italic = italic
    self.bold = bold
    self.underline = underline
    self.strikethrough = strikethrough

  @overload(bool, bool, bool)
  def __init__(
      self,
      italic: bool,
      bold: bool,
      underline: bool,
      **kwargs,
      ) -> None:
    self.italic = italic
    self.bold = bold
    self.underline = underline
    if kwargs:
      kwargs['italic'] = italic
      kwargs['bold'] = bold
      kwargs['underline'] = underline
      self.__init__(**kwargs)

  @overload(bool, bool)
  def __init__(
      self,
      italic: bool,
      bold: bool,
      **kwargs,
      ) -> None:
    self.italic = italic
    self.bold = bold
    if kwargs:
      kwargs['italic'] = italic
      kwargs['bold'] = bold
      self.__init__(**kwargs)

  @overload(bool)
  def __init__(
      self,
      italic: bool,
      **kwargs,
      ) -> None:
    self.italic = italic
    if kwargs:
      kwargs['italic'] = italic
      self.__init__(**kwargs)

  @overload(THIS)
  def __init__(self, other: Self, **_) -> None:
    self.italic = other.italic
    self.bold = other.bold
    self.underline = other.underline
    self.strikethrough = other.strikethrough

  @overload()
  def __init__(self, **kwargs) -> None:
    groups = self.__key_groups__.items()
    for name, keys in groups:
      type_ = self.__key_types__[name]
      defVal = self.__key_defaults__[name]
      for key in keys:
        if key in kwargs:
          value = kwargs[key]
          if not isinstance(value, type_):
            raise TypeException(name, value, type_)
          setattr(self, name, value)
          break
      else:
        setattr(self, name, defVal)

  @classmethod
  def _resolveOther(cls, other: Self) -> Self:
    return other if isinstance(other, cls) else NotImplemented

  def __eq__(self, other: Self) -> bool:
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    for key in self.__key_groups__.keys():
      if getattr(self, key) != getattr(other, key):
        return False
    return True

  def _binaryOp(self, other: Self, op: Callable) -> Self:
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    keys = self.__key_groups__.keys()
    out = cls()
    for key in keys:
      selfVal = getattr(self, key)
      otherVal = getattr(other, key)
      value = op(selfVal, otherVal)
      setattr(out, key, value)
    return out

  def __and__(self, other: Self) -> Self:
    return self._binaryOp(other, operator.and_)

  def __or__(self, other: Self) -> Self:
    return self._binaryOp(other, operator.or_)

  def __xor__(self, other: Self) -> Self:
    return self._binaryOp(other, operator.xor)

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

  def apply(self, content: str) -> str:
    """
    Applies the style to the given content and returns the styled content.
    """
    openTag: str
    closeTag: str
    tags = []
    if self.italic:
      tags.append(('<i>', '</i>'))
    if self.bold:
      tags.append(('<b>', '</b>'))
    if self.underline:
      tags.append(('<u>', '</u>'))
    if self.strikethrough:
      tags.append(('<s>', '</s>'))
    owner = self.getFieldOwner()
    try:
      header = getattr(owner, '__header_level__')
    except AttributeError:
      header: HeaderNum = HeaderNum.PARAGRAPH
    level = header.value
    tags.append(('<%s>' % level, '</%s>' % level))
    for openTag, closeTag in tags:
      content = """%s%s%s""" % (openTag, content, closeTag)
    return content
