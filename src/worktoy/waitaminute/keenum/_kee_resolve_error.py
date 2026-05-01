"""
KeeResolveError subclasses 'Exception' and should be raised by 'KeeNum'
enumerations that implement the '__class_resolve__' classmethod to
indicate the equivalent of returning 'NotImplemented'. The 'KeeMeta'
metaclass catches this exception and attempts fallback resolvers. If they
all fail, the caught exception is raised.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeResolveError(Exception):
  """
  Raised by '__class_resolve__' to decline resolution.

  Equivalent to returning 'NotImplemented' from the resolver. Any
  other exception raised by '__class_resolve__' propagates normally.
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
    infoSpec = """Custom resolver for enumeration '%s' declined to resolve 
    the identifier '%s'!"""
    clsName = self.keeNum.__name__
    identifier = str(self.identifier)
    info = infoSpec % (clsName, identifier)
    return textFmt(info)

  __repr__ = __str__
