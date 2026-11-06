"""
LoggedMeta is a metaclass based on 'AbstractMetaclass' whose namespace is
'LoggedSpace'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass

from . import LoggedSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class LoggedMeta(AbstractMetaclass):
  """
  A metaclass supplies another namespace by reimplementing '__prepare__'
  alone. 'LoggedMeta' returns a 'LoggedSpace', so every class it builds
  leaves a record of its construction in 'LoggingHook.log'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> LoggedSpace:
    return LoggedSpace(mcls, name, bases, **kwargs)
