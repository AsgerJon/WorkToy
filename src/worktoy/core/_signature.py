"""Signature is a class representing the type signature of instances of
CallMeMaybe. """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn


class Signature:
  """Signature is a class representing the type signature of instances of
  CallMeMaybe.
  When invoking: someFunc(1, 2, 3) use:
    res = someFunc(1, 2, 3)
    sig = Signature()
    res = sig @ (1, 2, 3) >> someFunc
    This creates an instance of Signature matching 'someFunc'.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    self._domain = None
    self._range = None
    self._lock = False

  def fromPrototype(self, *args) -> NoReturn:
    """When invoking: someFunc(1, 2, 3) use:
    res = someFunc(1, 2, 3)
    sig = Signature()
    res = sig @ (1, 2, 3) >> someFunc
    This creates an instance of Signature matching 'someFunc'. """
