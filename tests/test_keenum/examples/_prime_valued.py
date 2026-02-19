"""
This subclass has no flags, but provides a '_getValue' reimplementation
that associates each flag with a prime number beginning with 2. The
value of each member is then the product of the primes associated with
the flags that are HIGH for that member.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.keenum import KeeFlags


class PrimeValued(KeeFlags):
  """
  This subclass has no flags, but provides a '_getValue' reimplementation
  that associates each flag with a prime number beginning with 2. The
  value of each member is then the product of the primes associated with
  the flags that are HIGH for that member.
  """

  @staticmethod
  def isPrime(p: int) -> bool:
    c = 2
    while c * c <= p:
      if p % c == 0:
        break
      c += 1
    else:
      return True
    return False

  @classmethod
  def nextPrime(cls, p0: int) -> int:
    p = p0 + (2 if p0 % 2 else 1)
    while cls.isPrime(p):
      p += 2
    return p

  @classmethod
  def indexPrime(cls, index: int) -> int:
    p = 2
    for _ in range(index):
      p = cls.nextPrime(p)
    return p

  def _getValue(self, ) -> int:
    out = 1
    for flag in self.highs:
      out *= self.indexPrime(flag.index)
    return out

  @overload(int, int)
  def coverageGymnastics(self, a: int, b: int) -> int:
    return a + b

  @overload(str, str)
  def coverageGymnastics(self, a: str, b: str) -> int:
    return int(a) + int(b)
