"""WorkToy - Core - Math
Module providing math tools."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

factorial = lambda n: 1 if n < 2 else n * (n - 1)
PI = 3.141592653589793
EXP1 = [1 / factorial(i) for i in range(16)]
