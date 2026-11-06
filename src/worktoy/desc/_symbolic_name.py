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

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Optional, Union, Iterator, Any

  StrTuple: TypeAlias = tuple[str, ...]
  StrTupleStr: TypeAlias = Union[str, StrTuple]
  MaybeStrTuple: TypeAlias = Optional[StrTuple]


class SymbolicName(Object):
  """
  One name often has to be written in several conventions, a setting
  'fontSize' in code, 'font_size' in a file and 'FONT_SIZE' in the
  environment, and the spellings must stay in step. The name is best
  kept as its words, with every spelling made from them, and two names of
  the same words must count as one name whatever their case.

  Implementation
  --------------

  The words are kept as given; 'snake', 'screamingSnake', 'kebab',
  'screamingKebab', 'pascal' and 'camel' render them. Every rendering
  sets the case itself, and a word is capitalized as 'str.capitalize'
  does, so 'HTTPServer' becomes 'Httpserver' in Pascal case; an acronym
  meant to survive is given as a word of its own. Equality and hash go
  by the lowercased words in order. A name supports 'len', iteration,
  indexing, slicing and 'in' for a word, ignoring case. As an 'Object',
  a 'SymbolicName' placed in a class body is a read-only class variable.

  Attributes
  ----------

  words : tuple[str, ...]
    The words as given.

  snake, screamingSnake, kebab, screamingKebab, pascal, camel : str
    The renderings.
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
    tail = str.join('', [word.capitalize() for word in rest])
    return """%s%s""" % (first.lower(), tail)

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
    for word in words:
      if not isinstance(word, str):
        raise TypeException('word', word, str)
    object.__setattr__(self, '__part_words__', words)

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
    """
    A word belongs to a name whatever its case, as equality ignores case.

    Parameters
    ----------

    item : str
      The word; anything but a string is in no name.

    Returns
    -------

    bool
      Whether a word of the name equals 'item', ignoring case.
    """
    if not isinstance(item, str):
      return False
    return True if item.lower() in self._getKey() else False

  def _getKey(self) -> StrTuple:
    return (*(word.lower() for word in self.words),)

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, SymbolicName):
      return NotImplemented
    return True if self._getKey() == other._getKey() else False

  def __hash__(self) -> int:
    return hash(self._getKey())
