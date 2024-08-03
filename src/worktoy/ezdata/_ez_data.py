"""EZData provides a dataclass implementation. Subclasses of EZData must
place instances of AttriBox for each desired field. The order by which
they appear in the class body denote the order by which initial values
should be passed to the constructor. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZMeta


class EZData(metaclass=EZMeta):
  """EZData provides a dataclass implementation. Subclasses of EZData must
  place instances of AttriBox for each desired field. The order by which
  they appear in the class body denote the order by which initial values
  should be passed to the constructor. """

  def __init__(self, *args, **kwargs) -> None:
    """This method is replaced during class creation. """
