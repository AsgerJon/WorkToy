"""EZData provides a dataclass specifically designed for inline class
  creation."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.meta import CallMeMaybe, AbstractNamespace, AbstractMetaclass
from worktoy.base import FastMeta
from worktoy.ezdata import EZMeta, EZSpace


class EZMeta(AbstractMetaclass):
  """EZMeta provides the metaclass used by the EZData class. """

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple[type, ...],
                  **kwargs) -> EZSpace:
    """Prepare the namespace for the EZData class."""
    return EZSpace(mcls, name, bases, **kwargs)


class EZData(FastMeta):
  """EZData provides a dataclass specifically designed for inline class
  creation."""

  __ez_data__ = True

  def __call__(cls, *args, **kwargs) -> Any:
    """When calling the EZData class specifically, a new class derived
    from EZMeta is created. This permits the EZData class object to be
    used to create new classes inline. This requires the following syntax:
    Point = EZData(x=0.0, y=0.0)
    In the above, the field classes of the attributes are inferred from
    the given default values. A more flexible alternative is to define
    AttriBox instances in the call:
    Point = EZData(x=AttriBox[float](), y=AttriBox[float]())"""
