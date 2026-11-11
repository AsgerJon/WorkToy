"""
DeprecatedPromise warns that a feature is no longer promised from the
next major update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import WorkToyWarning

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class DeprecatedPromise(WorkToyWarning, FutureWarning):
  """
  What 'worktoy' owes the projects built upon it is what it promises
  them, and a promise holds for every release of a major version. A
  feature can therefore leave the promises only at the next major
  update, and a project relying on it must hear so in time, from a
  release of the major version it runs on. DeprecatedPromise is that
  notice, the deprecation of a feature. It is a 'FutureWarning', since
  Python hides a 'DeprecationWarning' from everyone but the author of
  the file that runs, and the feature works as it did while the notice
  is given. A deprecation is rare and each one is written by hand: the
  opening sentence is the same for all, and the description after it
  is the text of that one deprecation, such as what to write instead
  or where to read more.

    DeprecatedPromise(KeeBox, "Declare the field with ...").warn()

  A project built upon 'worktoy' deprecates a feature of its own by
  subclassing DeprecatedPromise in a package of its own, as the
  'WorkToyWarning' docstring describes.

  Attributes
  ----------
  feature : Any
    The feature that is no longer promised from the next major update:
    the class, function or descriptor itself, or its dotted name where
    there is no object to hand over, as for a name that moved.
  description : str
    What the author has to say about this one deprecation. It may be
    empty.
  """

  __slots__ = ('feature', 'description')

  def __init__(self, feature: Any, description: str = '') -> None:
    FutureWarning.__init__(self, )
    self.feature = feature
    self.description = description

  def __str__(self) -> str:
    infoSpec = """Deprecation alert: '%s' is no longer a promised feature
    beginning with the next major update. %s"""
    name = self._nameOf(self.feature)
    info = infoSpec % (name, self.description)
    return textFmt(info)

  __repr__ = __str__
