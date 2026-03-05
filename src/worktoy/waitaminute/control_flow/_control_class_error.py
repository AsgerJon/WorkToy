"""
ControlClassError is a custom exception class raised to indicate that a
'ControlFlow' subclass is implementing disallowed attributes. Only
'__str__' and '__repr__' are allowed.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, TypeAlias
  from . import ControlSpace, MetaFlow

  Meta: TypeAlias = Type[MetaFlow]


class ControlClassError(TypeError):
  """
  ControlClassError is a custom exception class raised to indicate that a
  'ControlFlow' subclass is implementing disallowed attributes. Only
  '__str__' and '__repr__' are allowed.
  """

  __slots__ = ('space', 'badKey')

  def __init__(self, space: ControlSpace, badKey) -> None:
    self.space = space
    self.badKey = badKey
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """When creating class '%s', a subclass of '%s', 
    tried implementing attribute '%s'! Only '__str__' and '__repr__' are 
    allowed."""
    mcls: Meta = self.space.__metaclass__
    root = mcls.getRootClass()
    rootName = root.__name__
    clsName = self.space.__class_name__
    badKey = self.badKey
    return infoSpec % (clsName, rootName, badKey)

  __repr__ = __str__
