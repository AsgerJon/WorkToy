"""Decorators are classes supporting decorations of other classes and
functions"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn, Any

from worktoy.core import TypeBag, CallMeMaybe
from worktoy.waitaminute import n00bError, ValidationError

Target = TypeBag(CallMeMaybe, type)


class Decorator:
  """Decorators are classes supporting decorations of other classes and
  functions
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __call__(self, target: Target) -> Target:
    """This method is called when the instance is applied to the target.
    If the class is place above a function or class definition, without
    instantiation, it is instead the __init__ that is called."""
    self.validate(target)
    self.decorate(target)
    return target

  @abstractmethod
  def validate(self, target: Target) -> NoReturn:
    """This abstractmethod validates the target. Subclasses must implement
    this method according to what targets may be decorated. Please note
    that bugs relating to improper application of decorators can be
    exceedingly difficult to identify.

    Developers are adviced to let this method raise an error if a target
    fails validation instead of silently ignoring it. Another source of
    difficult bugs are when a target is unexpectedly not decorated."""

  @abstractmethod
  def decorate(self, target: Target) -> Target:
    """This abstractmethod determines exactly what is to be done to each
    target. Please note that this method must return the target."""
