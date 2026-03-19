"""
CodeBlock subclasses 'Block' and allows presentation of code from files in
the Markdown.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from . import Block
from ..waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Never

  from . import InlineText

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  MaybeType: TypeAlias = Optional[type]
  TypeField: TypeAlias = Union[type, Field]


class CodeBlock(Block):
  """
  CodeBlock subclasses 'Block' and allows presentation of code from files in
  the Markdown.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __source_code__: MaybeStr = None

  #  Public Variables
  sourceCode: StrField = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createSourceCode(self, ) -> None:
    """
    Subclasses should implement this method, if they need to dynamically
    generate the source code.
    """

  @sourceCode.GET
  def _getSourceCode(self, **kwargs) -> str:
    if self.__source_code__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createSourceCode()
      return self._getSourceCode(_recursion=True)
    if isinstance(self.__source_code__, str):
      return self.__source_code__
    name, value = '__source_code__', self.__source_code__
    raise TypeException(name, value, str)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def markdown(self) -> str:
    """
    The 'CodeBlock' class entirely rewrites the 'markdown' method.

    Returns
    -------
    str
        The Markdown representation of the block, which is the source code
        of the example class formatted as a code block.
    """
    return str.join('\n', (self.anchor, self.sourceCode))

  @classmethod
  def registerInline(cls, inline: InlineText, name: str) -> Never:
    """
    CodeBlock does not support inline components, so this method raises a
    'TypeError'.
    """
    infoSpec = """'%s' does not support inline components, but received: 
    '%s' at name: '%s'!"""
    clsName = cls.__name__
    raise TypeError(infoSpec % (clsName, str(inline), name))

  registerBlock = registerInline
