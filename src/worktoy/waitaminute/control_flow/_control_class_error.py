"""
ControlClassError is raised when a 'ControlFlow' subclass defines a
disallowed attribute.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, TypeAlias
  from . import ControlSpace, MetaFlow

  Meta: TypeAlias = Type[MetaFlow]


class ControlClassError(NoPickle, TypeError):
  """
  ControlClassError is raised when a 'ControlFlow' subclass defines a
  disallowed attribute. Only '__str__' and '__repr__' may be defined in
  the class body; the dunders '__firstlineno__', '__namespace__',
  '__static_attributes__', '__classcell__' and '__classdictcell__' are
  also permitted, and so is any name 'Exception' holds as an attribute
  that is not callable, such as '__doc__' and '__module__'. Any other
  attribute raises this exception.
  """

  __slots__ = ('space', 'badKey')

  def __init__(self, space: ControlSpace, badKey) -> None:
    self.space = space
    self.badKey = badKey
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """When creating class '%s', a subclass of '%s', tried
    implementing attribute '%s'! Only '__str__' and '__repr__' are
    allowed."""
    mcls: Meta = self.space.__metaclass__
    root = mcls.getRootClass()
    rootName = root.__name__
    clsName = self.space.__class_name__
    badKey = self.badKey
    info = infoSpec % (clsName, rootName, badKey)
    from ...utilities import textFmt
    return textFmt(info)

  __repr__ = __str__
