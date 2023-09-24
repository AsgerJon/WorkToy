"""WorkToy - Core - AbstractTemplate
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.worktoyclass import WorkToyClass


class AbstractTemplate(WorkToyClass):
  """WorkToy - Core - AbstractTemplate
  Code writing assistant"""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)

  @abstractmethod
  def getTags(self) -> dict[str, str]:
    """Getter-function for the dictionary mapping tags to replacements"""

  def render(self, base: str) -> str:
    """Applies tags to base"""
    out = base
    for key, val in self.getTags().items():
      out = out.replace(key, val)
    return out
