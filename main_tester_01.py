"""
Testing more stupid typing stuff!!
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from main_tester_00 import Box
from worktoy.desc import AttriBox
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional, Iterator


class Bar:
  good = Box[int]
  cunt = good.__call__
  bad = AttriBox[int](420)


class Priminator:
  __prime_numbers__: Optional[tuple[int, ...]] = None

  @classmethod
  def _createPrimeNumbers(cls, ) -> None:
    setattr(cls, '__prime_numbers__', (2,))

  @classmethod
  def getPrimeNumbers(cls, **kwargs) -> tuple[int, ...]:
    if cls.__prime_numbers__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createPrimeNumbers()
      return cls.getPrimeNumbers(_recursion=True)
    if not isinstance(cls.__prime_numbers__, tuple):
      raise TypeException('prime_numbers', cls.__prime_numbers__, tuple)
    for prime in cls.__prime_numbers__:
      if not isinstance(prime, int):
        break
    else:
      return cls.__prime_numbers__
    raise TypeException('prime', prime, int)

  @classmethod
  def _appendPrimeNumber(cls, prime: int) -> None:
    existing = cls.getPrimeNumbers()
    cls.__prime_numbers__ = (*existing, prime)

  @classmethod
  def _nextPrime(cls, ) -> int:
    primes: tuple[int, ...] = cls.getPrimeNumbers()
    latestPrime: int = primes[-1]
    candidate: int = latestPrime + 1 + latestPrime % 2
    while candidate < latestPrime ** 2:
      for prime in primes:
        if candidate % prime:
          continue
        break
      else:
        break
      candidate += 2
    cls._appendPrimeNumber(candidate)
    return candidate

  def __init__(self, n: Optional[int]) -> None:
    if n is not None:
      if isinstance(n, int):
        if n < 2:
          raise ValueError(f'Cannot create a Priminator with n={n}.')
        while n > len(self) or n > self[-1]:
          self._nextPrime()
      else:
        raise TypeException('n', n, int)

  def __getitem__(self, index: int) -> int:
    return self.getPrimeNumbers()[index]

  def __iter__(self, ) -> Iterator[int]:
    primes = self.getPrimeNumbers()
    yield from primes
    yield self._nextPrime()

  def __len__(self, ) -> int:
    return len(self.getPrimeNumbers())

  def __bool__(self) -> bool:
    return True if len(self) else False

  def __str__(self, ) -> str:
    infoSpec: str = """<Priminator object at 0x%x with %s>"""
    if len(self) == 1:
      primeSpec = """%d"""
      primeInfo = primeSpec % (self[0],)
    elif len(self) == 2:
      primeSpec = """(%d and %d)"""
      primeInfo = primeSpec % (self[0], self[1])
    elif len(self) == 3:
      primeSpec = """(%d, %d and %d)"""
      primeInfo = primeSpec % (self[0], self[1], self[2])
    elif len(self) > 3:
      primeSpec = """(%d, %d, ... %d)"""
      primeInfo = primeSpec % (self[0], self[1], self[-1])
    else:
      return """<Priminator object at 0x%x with no primes>""" % (id(self),)
    return infoSpec % (id(self), primeInfo)

  def __repr__(self, ) -> str:
    infoSpec = """%s(%d)"""
    info = infoSpec % (type(self).__name__, len(self))
    return info
