"""The empty function returns True if all args are None. If even one is
not None, False is returned"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def empty(*args) -> bool:
  """The empty function returns True if all args are None. If even one is
  not None, False is returned
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  for arg in args:
    if arg is not None:
      return False
  return True
