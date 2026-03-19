"""
BlockHook subclasses 'AbstractSpaceHook' and hooks into the class body
execution of block components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..utilities import maybe
from ..mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable

  from . import BlockSpace, Block

  BlocksTuple: TypeAlias = tuple[Block, ...]
  BlocksDict: TypeAlias = dict[str, Block]
  GetBlocksTuple: TypeAlias = Callable
  GetBlocksDict: TypeAlias = Callable


class BlockHook(AbstractSpaceHook):
  """
  BlockHook subclasses 'AbstractSpaceHook' and hooks into the class body
  execution of block components.
  """

  space: BlockSpace

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _getBlocksTupleFactory() -> GetBlocksTuple:
    """
    Factory for the 'getBlocksTuple' method added in the 'postCompilePhase'
    method.
    """

    def getBlocksTuple(self: Block) -> BlocksTuple:
      """
      Auto-generated method for retrieving the tuple of block components
      registered in the block.
      """
      return maybe(self.__blocks_tuple__, ())

    return getBlocksTuple

  @staticmethod
  def _getBlocksDictFactory() -> GetBlocksDict:
    """
    Factory for the 'getBlocksDict' method added in the 'postCompilePhase'
    method.
    """

    def getBlocksDict(self: Block) -> BlocksDict:
      """
      Auto-generated method for retrieving the dict of block components
      registered in the block.
      """
      return maybe(self.__blocks_dict__, {})

    return getBlocksDict

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    setItemPhase is the phase of the class body execution where the class
    namespace is being populated. This method is called for each item being
    set in the class namespace.
    """
    try:
      _ = val.__is_block__
    except AttributeError:
      return False
    else:
      self.space.addBlock(key, val)
      return True

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    compiledSpace['__is_block__'] = True
    blocksTuple = (*self.space.getBlocksTuple(),)
    blocksDict = {**self.space.getBlocksDict(), }
    getBlocksTuple = self._getBlocksTupleFactory()
    getBlocksDict = self._getBlocksDictFactory()
    compiledSpace['getBlocksTuple'] = classmethod(getBlocksTuple)
    compiledSpace['getBlocksDict'] = classmethod(getBlocksDict)
    compiledSpace['__blocks_tuple__'] = blocksTuple
    compiledSpace['__blocks_dict__'] = blocksDict
    for name, block in blocksDict.items():
      compiledSpace[name] = block
    return compiledSpace
