"""FastMeta provides the metaclass for the FastData class. This metaclass
customize the initial class creation process by returning an instance of
FastSpace from __prepare__ for use as namespace. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import Base
from worktoy.base import BaseMetaclass
from worktoy.ezdata import EZSpace


class EZMeta(BaseMetaclass):
  """FastMeta provides the metaclass for the FastData class. This metaclass
  customize the initial class creation process by returning an instance of
  FastSpace from __prepare__ for use as namespace. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs) -> EZSpace:
    return EZSpace(mcls, name, bases, **kwargs)
