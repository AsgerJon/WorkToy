"""Tester01"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class CUNT:
  """KILL YOURSELF"""

  @classmethod
  def __getattribute__(cls, key: str) -> Any:
    """LMAO"""
    print(cls, key)
    try:
      out = object.__getattribute__(cls, key)
    except AttributeError as error:
      raise error
    return out

  @classmethod
  def _killClassMethod(cls) -> None:
    """KILL"""

  def __init__(self, *args, **kwargs) -> None:
    self._args = args
    self._kwargs = kwargs

  def _kill(*self, ) -> None:
    """SHIT"""

  def _shit(*self, ) -> None:
    """KILL"""

  # def __getattr__(self, key: str) -> Any:
  #   """LMAO"""
  #   print('cunt')
  #


if __name__ != '__main__':
  setattr(CUNT, '__core_instance__', CUNT())
