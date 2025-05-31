"""
Some tester classes
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class AnvilNode:
  """
  Represents an item or book created by merging two sources.
  """

  def __init__(self,
               left: 'AnvilNode | None',
               right: 'AnvilNode | None',
               enchants: dict[str, int],
               *,
               isBook: bool = True):
    self.left = left
    self.right = right
    self.enchants = enchants
    self.isBook = isBook
    self.pwp = 0
    self.cost = 0

    if left is not None and right is not None:
      self._merge(left, right)

  def _merge(self, a: 'AnvilNode', b: 'AnvilNode') -> None:
    pwpA = a.pwp
    pwpB = b.pwp
    enchA = dict(a.enchants)
    enchB = dict(b.enchants)

    # Compute cost and updated enchants
    try:
      newPwp, cost, merged = mergeBookToItem(pwpA, pwpB,
                                             enchA, enchB)
    except ValueError as error:
      raise ValueError(f"Merge failed: {error}")

    self.enchants = merged
    self.pwp = newPwp
    self.cost = cost

  def getTotalCost(self) -> int:
    """
    Returns total cumulative cost for building this node.
    """
    if self.left is None and self.right is None:
      return 0
    total = self.cost
    if self.left is not None:
      total += self.left.getTotalCost()
    if self.right is not None:
      total += self.right.getTotalCost()
    return total

  def __str__(self) -> str:
    return f"[PWP={self.pwp} Cost={self.cost} {self.enchants}]"
