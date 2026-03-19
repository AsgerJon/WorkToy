"""
InstallBlock subclasses 'CodeBlock' from the 'worktoy.markwork' package
and provides an example by showing how one might install 'worktoy' using:
[REDACTED].
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import CodeBlock

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class InstallBlock(CodeBlock):
  """
  InstallBlock subclasses 'CodeBlock' from the 'worktoy.markwork' package
  and provides an example by showing how one might install 'worktoy' using:
  [REDACTED].
  """

  def _createSourceCode(self, ) -> None:
    """Sets the source code verbatim."""
    self.__source_code__ = """pip install worktoy"""
