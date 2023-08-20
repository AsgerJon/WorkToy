"""LMAO"""
from __future__ import annotations

from typing import Protocol, Never


class CallMeMaybe(Protocol):
  """LMAO"""
  def __init__(self, *args, **kwargs) -> None:
    ...

  def _setInnerFunction(self, *args, **kwargs) -> None:
    ...

  def _invokeFunction(self, *args, **kwargs) -> object:
    ...

  def __bool__(self) -> bool:
    ...

  def __str__(self) -> str:
    ...

  def __repr__(self) -> str:
    ...

  def __call__(self, *args, **kwargs) -> object:
    ...

  def __set_name__(self, owner: type, name: str) -> None:
    ...

  def __get__(self, obj: object, owner: type) -> CallMeMaybe:
    ...

  def __set__(self, *_) -> Never:
    ...

  def __delete__(self, *_) -> Never:
    ...
