"""
Nudge is a control-flow signal of a project, with a text of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.control_flow import ControlFlow


class Nudge(ControlFlow):
  """
  A project declares a signal of its own as a subclass of 'ControlFlow'
  with a docstring, and may give it a '__str__'. 'Nudge' does both.
  """

  def __str__(self) -> str:
    return 'nudge!'
