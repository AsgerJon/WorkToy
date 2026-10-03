"""
DuplicateSentinel is raised when a class statement declares a sentinel at
a name a sentinel already holds.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional


class DuplicateSentinel(NoPickle, TypeError):
  """
  DuplicateSentinel is raised when a class statement declares a sentinel
  at a name that a sentinel already holds. A sentinel defines one concept
  for the whole process, and 'SentinelMeta' keeps every sentinel in one
  registry by name, so a second class statement at the name, in another
  module or in the same one, is not a second sentinel of the concept but
  a mistake: the existing sentinel is the one to import. The second
  class statement used to receive the existing sentinel without a word,
  docstring and module included, so two unrelated modules each declaring
  a 'PENDING' shared one object, and a value of the one passed the
  identity checks of the other. It subclasses 'TypeError', as
  'IllegalInstantiation' does for the other misuse of a sentinel class.

  Attributes
  ----------
  sentinelName : str
    The name both class statements declare.
  existing : type
    The sentinel already registered under the name; its '__module__'
    says where it was declared.
  module : str or None
    The module of the class statement that was refused, or None when the
    namespace it was built from names none, as a plain dict given to
    'SentinelMeta' by hand does not.
  """

  __slots__ = ('sentinelName', 'existing', 'module')

  def __init__(
      self,
      sentinelName: str,
      existing: type,
      module: Optional[str] = None,
  ) -> None:
    self.sentinelName = sentinelName
    self.existing = existing
    self.module = module
    TypeError.__init__(self, )

  def __str__(self) -> str:
    spec = """A sentinel named '%s' already exists, declared in '%s', but
    %s declares another. A sentinel defines one concept for the whole
    process, so the name may hold only one; import the existing sentinel
    instead."""
    if self.module is None:
      second = 'a class statement'
    else:
      second = """the class statement in '%s'""" % self.module
    existingModule = getattr(self.existing, '__module__', None)
    info = spec % (self.sentinelName, existingModule, second)
    return textFmt(info)

  __repr__ = __str__
