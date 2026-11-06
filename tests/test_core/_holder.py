"""
Holder is a worktoy class whose box builds an 'Item' per instance.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import Item

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Holder(BaseObject):
  """
  While a box reads, the value it built can ask for the instance and the
  owner of the read through the box. 'Holder' asks on behalf of its
  'item' from an 'onGet' callback and keeps the answers in 'seenInstance'
  and 'seenOwner'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  item = AttriBox[Item]()
  seenInstance = AttriBox[object](None)
  seenOwner = AttriBox[object](None)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @item.onGet
  def _askItem(self, value: Any) -> None:
    self.seenInstance = value.getContextInstance()
    self.seenOwner = value.getContextOwner()
