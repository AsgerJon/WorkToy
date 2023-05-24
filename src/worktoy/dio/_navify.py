"""Navify is a subclass of Juicify providing path related decorators"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import os
from typing import Any

from worktoy.core import CallMeMaybe
from worktoy.field import Juicify


class Navify(Juicify):
  """Navify is a subclass of Juicify providing path related decorators"""

  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence

  def __init__(self, *args, **kwargs) -> None:
    Juicify.__init__(self, *args, **kwargs)

  def baseFactory(self, cls: type) -> CallMeMaybe:
    """Base factory"""

    def func(instance: Any) -> Any:
      """Parent directory"""
      flag = getattr(getattr(instance, '__class__'), '__pathified__', False)
      if not flag:
        msg = """Object %s is not an instance of a pathified class!"""
        raise AttributeError(msg % instance)
      prevPath = getattr(instance, '_pathName', False)
      if not prevPath:
        msg = """Failed to find _pathName attribute on object %s!"""
        raise AttributeError(msg % instance)
      return instance

    return func

  def mainFactory(self, cls: type) -> CallMeMaybe:
    """Main factory"""

    def func(instance: Any) -> Any:
      """Parent directory"""
      prevPath = getattr(instance, '_pathName', False)
      setattr(instance, '_pathName', os.path.dirname(prevPath))
      return instance

    return func
