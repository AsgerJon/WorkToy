"""
InlineLorem subclasses 'InlineText' providing randomly generated 'lorem
ipsum' text.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.sentinels import THIS
from ..desc import AttriBox, Field
from ..dispatch import overload
from ..lorem_ipsum import Sentence
from . import InlineText
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Never, Self

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]

  SentenceBox: TypeAlias = Union[Sentence, AttriBox]


class InlineLorem(InlineText):
  """
  InlineLorem subclasses 'InlineText' providing randomly generated 'lorem
  ipsum' text.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_count__: int = 120

  #  Private Variables
  __cached_text__: MaybeStr = None

  #  Public Variables
  cached: StrField = Field()
  lorem: SentenceBox = AttriBox[Sentence]()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createCache(self, ) -> None:
    self.lorem.reset()
    self.__cached_text__ = str(self.lorem)

  @cached.GET
  def _getCache(self, **kwargs) -> str:
    if self.__cached_text__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createCache()
      return self._getCache(_recursion=True)
    return self.__cached_text__

  def getText(self) -> str:
    return self.cached

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)  # Disabled
  def __init__(self, *_) -> Never:
    infoSpec = """'%s' cannot be instantiated on 'str' arguments! It is 
    intended to automatically generate 'lorem ipsum' text."""
    clsName = type(self).__name__
    info = textFmt(infoSpec % clsName)
    raise TypeError(info)

  @overload(int)
  def __init__(self, count: int) -> None:
    self.lorem.charCount = count

  @overload()
  def __init__(self) -> None:
    self.lorem.charCount = self.__fallback_count__

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.lorem.charCount = other.lorem.charCount
