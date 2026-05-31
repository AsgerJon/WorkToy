"""
SymbolicName presents an array of words in several name formats.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..utilities import textFmt
from ..waitaminute import MissingVariable, TypeException
from . import Field

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Iterator

  StrTuple: TypeAlias = tuple[str, ...]
  StrTupleStr: TypeAlias = Union[str, StrTuple]
  MaybeStrTuple: TypeAlias = Optional[StrTuple]


class SymbolicName(Object):
  """
  SymbolicName provides different representations of an array of words. The
  following representations are provided:
  - 'snake_case': The words are concatenated with underscores and all
    characters are lowercase.
  - 'SCREAMING_SNAKE_CASE': The words are concatenated with underscores and
    all characters are uppercase.
  - 'kebab-case': The words are concatenated with hyphens and all characters
    are lowercase.
  - 'SCREAMING-KEBAB-CASE': The words are concatenated with hyphens and all
    characters are uppercase.
  - 'PascalCase': The words are concatenated without any separators and
    the first character of each word is uppercase.
  - 'camelCase': The words are concatenated without any separators, the
    first character of the first word is lowercase, and the first
    character of each subsequent word is uppercase.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __part_words__: MaybeStrTuple = None

  #  Public Variables
  words: Field[StrTuple] = Field()

  #  Virtual Variables
  snake: Field[str] = Field()
  pascal: Field[str] = Field()
  camel: Field[str] = Field()
  kebab: Field[str] = Field()
  screamingSnake: Field[str] = Field()
  screamingKebab: Field[str] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @words.GET
  def _getWords(self) -> StrTuple:
    if self.__part_words__ is None:
      raise MissingVariable(self, 'words', tuple)
    return self.__part_words__

  @snake.GET
  def _getSnake(self) -> str:
    return '_'.join(self.words).lower()

  @pascal.GET
  def _getPascal(self) -> str:
    return ''.join(word.capitalize() for word in self.words)

  @kebab.GET
  def _getKebab(self) -> str:
    return '-'.join(self.words).lower()

  @camel.GET
  def _getCamel(self) -> str:
    if not self.words:
      return ''
    first, *rest = self.words
    if not rest:
      return first.lower()
    return """%s%s""" % (first.lower(), type(self)(*rest, ).pascal)

  @screamingSnake.GET
  def _getScreamingSnake(self, ) -> str:
    return str.upper(self.snake)

  @screamingKebab.GET
  def _getScreamingKebab(self, ) -> str:
    return str.upper(self.kebab)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *words: str) -> None:
    self.__part_words__ = words

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __bool__(self) -> bool:
    return True if self.words else False

  def __len__(self, ) -> int:
    return len(self.words)

  def __iter__(self, ) -> Iterator[str]:
    yield from self.words

  def _resolveIndex(self, index: int) -> str:
    words = (*self,)
    if index < 0:
      index += len(words)
    if 0 <= index < len(words):
      return words[index]
    raise IndexError(index)

  def _resolveSlice(self, index: slice) -> tuple[str, ...]:
    return (*self,)[index]

  def __getitem__(self, identifier: int) -> StrTupleStr:
    if isinstance(identifier, int):
      return self._resolveIndex(identifier)
    if isinstance(identifier, slice):
      return self._resolveSlice(identifier)
    raise TypeException('identifier', identifier, int, slice)

  def __str__(self, ) -> str:
    infoSpec = """<%s: %s>"""
    clsName = type(self).__name__
    wordsStr = ', '.join(["""'%s'""" % w for w in self.words])
    return textFmt(infoSpec % (clsName, wordsStr))

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s)"""
    clsName = type(self).__name__
    wordsStr = ', '.join(["""'%s'""" % w for w in self.words])
    return textFmt(infoSpec % (clsName, wordsStr))

  def __contains__(self, item: str) -> bool:
    return True if item in self.words else False
