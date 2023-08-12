"""CallMeMaybe is a class representing callable objects"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable


class CallMeMaybe(Callable[..., Any]):
  """CallMeMaybe is a class representing callable objects"""


def decorator(func: CallMeMaybe) -> CallMeMaybe:
  """Some decorator"""


isinstance(lambda x: x, CallMeMaybe)  # should be True at RunTime

decorator(lambda x: x)  # but here PyCharm indicates an error!

# PyCharm says:
#  Expected type 'CallMeMaybe', got '(x: Any) -> Any' instead
