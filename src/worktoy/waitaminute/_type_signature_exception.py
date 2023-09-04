"""WorkToy - Wait A Minute! - TypeSignatureException
This exception is intended for use with overloaded functions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class TypeSignatureException(MetaXcept):
  """WorkToy - Wait A Minute! - TypeSignatureException
  This exception is intended for use with overloaded functions."""

  def __init__(self, signature: tuple[type], *args, **kwargs) -> None:
    MetaXcept.__init__(self, signature, *args, **kwargs)
    self._signature = signature  # Types received

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    body = """Failed to match signature"""
    return '%s\n%s' % (header, self.justify(body))
