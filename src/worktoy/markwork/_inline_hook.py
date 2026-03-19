"""
InlineHook subclasses 'AbstractSpaceHook' and provides the hook for inline
components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..mcls.space_hooks import AbstractSpaceHook
from ..utilities import maybe
from . import InlineBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable

  from . import BlockSpace, Block

  InlinesTuple: TypeAlias = tuple[InlineBase, ...]
  InlinesDict: TypeAlias = dict[str, InlineBase]
  GetInlinesTuple: TypeAlias = Callable[..., Any]
  GetInlinesDict: TypeAlias = Callable[..., Any]
  GetInlines: TypeAlias = Callable[[Block], InlinesTuple]


class InlineHook(AbstractSpaceHook):
  """
  InlineHook subclasses 'AbstractSpaceHook' and provides the hook for
  inline components.
  """

  space: BlockSpace

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _getInlinesTupleFactory() -> GetInlinesTuple:
    """
    Factory for the 'getInlinesTuple' method added in the
    'postCompilePhase' method.
    """

    def getInlinesTuple(self: Block) -> InlinesTuple:
      """
      Auto-generated method for retrieving the tuple of inline components
      registered in the block.
      """
      return maybe(self.__inlines_tuple__, ())

    return getInlinesTuple

  @staticmethod
  def _getInlinesDictFactory() -> GetInlinesDict:
    """
    Factory for the 'getInlinesDict' method added in the
    'postCompilePhase' method.
    """

    def getInlinesDict(self: Block) -> InlinesDict:
      """
      Auto-generated method for retrieving the dict of inline components
      registered in the block.
      """
      return maybe(self.__inlines_dict__, dict())

    return getInlinesDict

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    setItemPhase is the phase of the class body execution where the class
    namespace is being populated. This method is called for each item being
    set in the class namespace.
    """
    if isinstance(val, InlineBase):
      self.space.addInline(key, val)
      return True
    return False

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    inlinesTuple = (*self.space.getInlinesTuple(),)
    inlinesDict = {**self.space.getInlinesDict(), }
    getInlinesTuple = self._getInlinesTupleFactory()
    getInlinesDict = self._getInlinesDictFactory()
    compiledSpace['__inlines_tuple__'] = inlinesTuple
    compiledSpace['__inlines_dict__'] = inlinesDict
    compiledSpace['getInlinesTuple'] = classmethod(getInlinesTuple)
    compiledSpace['getInlinesDict'] = classmethod(getInlinesDict)
    for name, inline in inlinesDict.items():
      compiledSpace[name] = inline
    return compiledSpace
