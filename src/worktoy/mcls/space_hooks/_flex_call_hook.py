"""
FlexCallHook wraps plain class-body functions with 'flexCall'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from ...dispatch import flexCall
from . import AbstractSpaceHook


class FlexCallHook(AbstractSpaceHook):
  """
  FlexCallHook subclasses 'AbstractSpaceHook' from the
  'worktoy.mcls.space_hooks' package. It detects plain functions defined in
  the class body and replaces them with 'flexCall' wrappers during
  class creation.

  No namespace in 'worktoy' declares it, so the methods of a 'BaseObject'
  are called exactly as Python calls any method, and a positional
  argument beyond those a method declares raises 'TypeError'. A namespace
  whose classes should drop such arguments instead opts in by declaring
  the hook:

      class FlexSpace(BaseSpace):
        flexCallHook = FlexCallHook()
  """

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    The 'postCompilePhase' method detects plain functions in the
    compiled namespace and replaces each with its 'flexCall' wrapper, so
    that each method of the class drops positional arguments beyond
    those it declares.

    Parameters
    ----------
    compiledSpace : dict
        The namespace dict being assembled.

    Returns
    -------
    dict
        The same dict, with plain functions wrapped by 'flexCall'.
    """

    for key, val in compiledSpace.items():
      if isinstance(val, FunctionType):
        compiledSpace[key] = flexCall(val)

    return compiledSpace
