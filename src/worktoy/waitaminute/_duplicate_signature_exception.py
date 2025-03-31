"""DuplicateSignatureException subclasses KeyError and indicates that an
overload procedure was attempted with a duplicate type signature."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.static import TypeSig


class DuplicateSignatureException(KeyError):
  """DuplicateSignatureException subclasses KeyError and indicates that an
  overload procedure was attempted with a duplicate type signature."""

  def __init__(self, typeSig: TypeSig) -> None:
    e = """Encountered a duplicate type signature: '%s'"""
    KeyError.__init__(self, monoSpace(e % typeSig))
