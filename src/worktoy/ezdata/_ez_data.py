"""
EZData leverages the 'worktoy' library to provide a dataclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import EZMeta

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass

Func = type('_', (type,), dict(__instancecheck__=callable))('_', (), {})


def trustMeBro(callMeMaybe: Func) -> Func:
  """
  This is a decorator that can be used to mark a function as a root
  function in the EZData class.
  """
  callMeMaybe.__is_root__ = True
  return callMeMaybe


class EZData(metaclass=EZMeta):
  """
  EZData is a dataclass that provides a simple way to define data
  structures with validation and serialization capabilities.
  """
  pass

  @trustMeBro
  def __init__(self, *args, **kwargs) -> None:
    """
    Here for type hinting purposes only!
    """
