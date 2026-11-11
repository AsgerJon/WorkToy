"""
AlternativeWarning warns that a promised behaviour has a better way
beside it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import WorkToyWarning

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class AlternativeWarning(WorkToyWarning, UserWarning):
  """
  A library sometimes offers two ways to the same end and has a reason
  to prefer one, while the other stays promised and is not on its way
  out. That is no deprecation, and saying nothing leaves the user on
  the worse way. AlternativeWarning is given in that case: the
  behaviour works as promised, and the warning names it, what to use
  instead, and why.

    reason = 'the till already keeps the sum'
    AlternativeWarning(Till.recount, Till.cash, reason).warn()

  It is offered to the projects built upon 'worktoy' as much as to
  'worktoy' itself: a project subclasses it in a package of its own,
  as the 'WorkToyWarning' docstring describes.

  Attributes
  ----------
  behaviour : Any
    The promised behaviour the user relied on: the class, function or
    descriptor itself, or its dotted name.
  alternative : Any
    What to use instead, handed over the same way.
  reason : str
    Why the alternative is better, worded to follow 'because'.
  """

  __slots__ = ('behaviour', 'alternative', 'reason')

  def __init__(self, behaviour: Any, alternative: Any, reason: str) -> None:
    UserWarning.__init__(self, )
    self.behaviour = behaviour
    self.alternative = alternative
    self.reason = reason

  def __str__(self) -> str:
    infoSpec = """Although '%s' is promised to function, use '%s'
    instead, because %s!"""
    old = self._nameOf(self.behaviour)
    new = self._nameOf(self.alternative)
    info = infoSpec % (old, new, self.reason)
    return textFmt(info)

  __repr__ = __str__
