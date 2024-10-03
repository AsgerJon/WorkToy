"""FastMeta provides the metaclass for the FastData class. This metaclass
customize the initial class creation process by returning an instance of
FastSpace from __prepare__ for use as namespace. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseMetaclass, Bases
from worktoy.base import FastSpace


class FastMeta(BaseMetaclass):
  """FastMeta provides the metaclass for the FastData class. This metaclass
  customize the initial class creation process by returning an instance of
  FastSpace from __prepare__ for use as namespace. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> FastSpace:
    return FastSpace(mcls, name, bases, **kwargs)
