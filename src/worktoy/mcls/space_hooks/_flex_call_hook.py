"""
FlexCallHook wraps plain class-body functions with 'flexCall'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ...dispatch import flexCall
from . import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  pass


class FlexCallHook(AbstractSpaceHook):
  """
  FlexCallHook subclasses 'AbstractSpaceHook' from the
  'worktoy.mcls.space_hooks' package. It detects plain functions defined in
  the class body and replaces them with 'flexCall' wrappers during
  class creation.
  """

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    This implementation detects plain functions defined in the class body
    and replaces them with 'flexCall' objects, allowing them to be flexibly
    overloaded.
    """

    for key, val in compiledSpace.items():
      if isinstance(val, FunctionType):
        compiledSpace[key] = flexCall(val)

    return compiledSpace
