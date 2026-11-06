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
  A namespace may want every method of its classes to accept positional
  arguments beyond those it declares, dropping the surplus, as the
  notification callbacks of 'BaseDescriptor' do. No namespace of worktoy
  wants it, so the methods of a 'BaseObject' are called as Python calls
  any method, and a namespace opting in declares the hook:

    class FlexSpace(BaseSpace):
      flexCallHook = FlexCallHook()

  Implementation
  --------------

  After the body is merged, every plain function of the class dictionary
  is replaced by its 'flexCall' wrapper; dunder methods are left alone.
  """

  def postCompilePhase(self, compiledSpace: dict) -> dict:

    for key, val in compiledSpace.items():
      if isinstance(val, FunctionType):
        compiledSpace[key] = flexCall(val)

    return compiledSpace
