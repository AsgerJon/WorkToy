from typing import Protocol
from abc import abstractmethod

class CallMeMaybeProtocol(Protocol):
  @abstractmethod
  def __init__(self, *args, **kwargs) -> 'None' -> None:
    ...

  @abstractmethod
  def _setInnerFunction(self, *args, **kwargs) -> 'None' -> None:
    ...

  @abstractmethod
  def _invokeFunction(self, *args, **kwargs) -> 'object' -> None:
    ...

  @abstractmethod
  def __bool__(self) -> 'bool' -> None:
    ...

  @abstractmethod
  def __str__(self) -> 'str' -> None:
    ...

  @abstractmethod
  def __repr__(self) -> 'str' -> None:
    ...

  @abstractmethod
  def __call__(self, *args, **kwargs) -> 'object' -> None:
    ...
