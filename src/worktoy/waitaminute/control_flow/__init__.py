"""
The 'worktoy.waitaminute.control_flow' package is a thin re-export kept
for the 1.x releases. The control-flow signals moved to
'worktoy.core.control_flow', beside the sentinels, and the refusal of an
attribute in a signal's class body, 'ControlClassError', moved to
'worktoy.waitaminute.meta' with the other refusals of a class-body line.
Import the names from there.

The names are resolved on access rather than at import, so importing
'worktoy.waitaminute' does not import 'worktoy.core', and the layering
of the packages holds. Once the library raises warnings, a
'FutureWarning' belongs in '__getattr__' below, naming the new home of
the name asked for.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

__all__ = [
  'ControlClassError',
  'ControlSpace',
  'MetaFlow',
  'ControlFlow',
  'SkipSet',
]


def __getattr__(name: str) -> Any:
  """Resolves a name of the family from its new home, or refuses it as a
  module refuses an attribute it does not have."""
  if name == 'ControlClassError':
    from ..meta import ControlClassError
    return ControlClassError
  if name in ('ControlSpace', 'MetaFlow', 'ControlFlow', 'SkipSet'):
    from ...core import control_flow
    return getattr(control_flow, name)
  infoSpec = "module '%s' has no attribute '%s'"
  raise AttributeError(infoSpec % (__name__, name))
