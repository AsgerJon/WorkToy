"""
PickleException is raised when an object defined by 'worktoy' is pickled,
or when a pickle stream tries to restore state into one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class PickleException(NoPickle, TypeError):
  """
  PickleException is raised when an object defined by 'worktoy' is
  pickled, or when a pickle stream tries to restore state into one.
  Unpickling rebuilds an object from the state stored with it without
  calling its class, so every check the class and its metaclass perform
  on construction and on assignment is skipped: an enumeration member
  comes back as a second member that equals none of the real ones, and a
  frozen or type-enforced object holds whatever the stream says. No
  object 'worktoy' defines supports pickling, this exception included.
  It subclasses 'TypeError', as the refusal Python raises for an object
  it cannot pickle.

  Attributes
  ----------
  obj : Any
    The object that refused the pickle protocol.
  action : str
    What was refused: 'pickled' for turning the object into a pickle,
    'unpickled' for restoring state into it from one.
  """

  __slots__ = ('obj', 'action')

  def __init__(self, obj: Any, action: str) -> None:
    self.obj = obj
    self.action = action
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Objects of type '%s' cannot be %s! No object defined by
    'worktoy' supports pickling, since unpickling rebuilds an object
    without calling its class and so skips every check the class
    performs."""
    info = infoSpec % (type(self.obj).__name__, self.action)
    return textFmt(info)

  __repr__ = __str__
