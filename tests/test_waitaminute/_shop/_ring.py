"""
The 'ring' function is code of the 'worktoy_shop' stand-in project that
warns its caller.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._shop_risk import ShopRisk


def ring(price: int) -> str:
  """
  The 'ring' function rings a sale and gives a 'ShopRisk' at the line
  of its caller.
  """
  ShopRisk('price', price, 'a till that pays the customer').warn()
  return 'sold'
