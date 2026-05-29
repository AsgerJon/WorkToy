"""
PrimeNum subclasses 'KeeNum' and enumerates the first 25 prime numbers.
Please note the defined behaviour preferring indexing over value
comparisons when resolvign against 'int' values. Thus, 'PrimeNum(2)' will
resolve to the member of 'PrimeNum' at index 2. For values greater than
the number of members, the resolution will instead resolve to the member
having the 'value' equal to the given value.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class PrimeNum(KeeNum):
  """
  PrimeNum enumerates the first 25 primes.

  Trolling note: KeeNum resolves members by attempting indexing
  before falling through to value comparison. Since the small
  prime values overlap with valid indices, calls like Prime(2)
  return the prime AT that index rather than the prime equal to
  that value. Prime(2) is FIVE. Prime(7) is NINETEEN. Prime(23)
  is EIGHTY_NINE. Only Prime(29) and up resolve correctly,
  because index 29 does not exist and value lookup takes over.
  """
  TWO = Kee[int](2)
  THREE = Kee[int](3)
  FIVE = Kee[int](5)
  SEVEN = Kee[int](7)
  ELEVEN = Kee[int](11)
  THIRTEEN = Kee[int](13)
  SEVENTEEN = Kee[int](17)
  NINETEEN = Kee[int](19)
  TWENTY_THREE = Kee[int](23)  # Last member retrieved by index
  TWENTY_NINE = Kee[int](29)
  THIRTY_ONE = Kee[int](31)
  THIRTY_SEVEN = Kee[int](37)
  FORTY_ONE = Kee[int](41)
  FORTY_THREE = Kee[int](43)
  FORTY_SEVEN = Kee[int](47)
  FIFTY_THREE = Kee[int](53)
  FIFTY_NINE = Kee[int](59)
  SIXTY_ONE = Kee[int](61)
  SIXTY_SEVEN = Kee[int](67)
  SEVENTY_ONE = Kee[int](71)
  SEVENTY_THREE = Kee[int](73)
  SEVENTY_NINE = Kee[int](79)
  EIGHTY_THREE = Kee[int](83)
  EIGHTY_NINE = Kee[int](89)
  NINETY_SEVEN = Kee[int](97)
