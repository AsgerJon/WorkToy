from typing import Protocol
from abc import abstractmethod

class TestProtocol(Protocol):
  @abstractmethod
  def method1(x) -> None:
    ...

  @abstractmethod
  def method2(x, y) -> None:
    ...
