"""
FutureNotation provides a dataclass setting slots as annotations as
strings using 'from __future__ import annotations'. This means that the
type annotated are not actually available in the scope of the class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from worktoy.ezdata import EZData

#  The FutureInteger does exist, just not in this scope. TYPE_CHECKING
#  means not at runtime. This is why we always have '# pragma: no cover'
#  so they are not included in the coverage report, as their purpose is
#  specifically to not happen at runtime.
if TYPE_CHECKING:  # pragma: no cover
  from . import FutureInteger


class FutureNotation(EZData):
  """
  FutureNotation provides a dataclass setting slots as annotations as
  strings using 'from __future__ import annotations'.
  """

  A: FutureInteger
  B: FutureInteger
  C: FutureInteger
  D: FutureInteger
  E: FutureInteger
  F: FutureInteger
