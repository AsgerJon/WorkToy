"""
KeeResolveError is raised when a 'KeeNum' enumeration cannot resolve an
identifier to a member.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeResolveError(NoPickle, Exception):
  """
  Raised when an enumeration cannot resolve an identifier to one of its
  members. It is the terminal signal of the resolution machinery: every
  applicable tier (identity, name, the optional '__class_resolve__'
  hook, positional index, and value) has been tried and none produced a
  member. A '__class_resolve__' hook declines by returning
  'NotImplemented', not by raising this; the machinery then raises it
  once the remaining tiers also miss. A 'KeeFlags' class raises it for
  every miss as well, by name, index or value, so one 'except' clause
  covers both enumerations.

  Attributes
  ----------
  keeNum : type
    The enumeration class against which resolution was attempted.
  identifier : Any
    The identifier that matched no member.
  """

  __slots__ = ('keeNum', 'identifier')

  def __init__(
      self,
      cls: type,
      identifier: Any,
  ) -> None:
    self.keeNum = cls
    self.identifier = identifier

  def __str__(self, ) -> str:
    infoSpec = """Enumeration '%s' could not resolve the identifier '%s'
    to any of its members!"""
    clsName = self.keeNum.__name__
    identifier = str(self.identifier)
    info = infoSpec % (clsName, identifier)
    return textFmt(info)

  __repr__ = __str__
