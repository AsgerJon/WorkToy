"""InfoGroup provides a grouping for info strings."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy._WORK_IN_PROGRESS.info import InfoMeta, InfoField

try:
  from typing import Callable, Any
except ImportError:
  Callable = object


class InfoGroup(metaclass=InfoMeta):
  """Info group categorizes the info strings."""

  name = InfoField('name', 'defaultGroupName')
  members = InfoField('members', [])

  def __init__(self, name: str) -> None:
    self.name = name

  def __str__(self, ) -> str:
    """String representation"""
    return """%s('%s')""" % (self.__class__.__name__, self.name)

  def __repr__(self, ) -> str:
    """String representation"""
    return """%s.%s""" % (self.__class__.__name__, self.name)


BaseGroup = InfoGroup('base')
