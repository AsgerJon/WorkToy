"""
ControlClassError is raised when a 'ControlFlow' subclass defines a
disallowed attribute.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Type, TypeAlias
  from ...core.control_flow import ControlSpace, MetaFlow

  Meta: TypeAlias = Type[MetaFlow]


class ControlClassError(WorkToyException, TypeError):
  """
  ControlClassError is raised when a 'ControlFlow' subclass defines a
  disallowed attribute. Only '__str__' and '__repr__' may be defined in
  the class body; the dunders '__firstlineno__',
  '__static_attributes__', '__classcell__' and '__classdictcell__' are
  also permitted, and so is any name 'Exception' holds as an attribute
  that is not callable, such as '__doc__' and '__module__'. Any other
  attribute raises this exception. It subclasses 'TypeError'; the
  signals it guards live in 'worktoy.core.control_flow'.
  """

  __slots__ = ('space', 'badKey')

  def __init__(self, space: ControlSpace, badKey) -> None:
    self.space = space
    self.badKey = badKey
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The class body of '%s', a signal based on '%s', binds
    '%s'."""
    rule = """A control-flow signal is used by its type alone and carries
    nothing, so its body holds a docstring, and may define '__str__' and
    '__repr__', but nothing else of its own."""
    mcls: Meta = self.space.__metaclass__
    root = mcls.getRootClass()
    rootName = root.__name__
    clsName = self.space.__class_name__
    badKey = self.badKey
    info = infoSpec % (clsName, rootName, badKey)
    return textFmt(info, rule)

  __repr__ = __str__
