"""
The 'worktoy.waitaminute.control_flow' package is a thin re-export kept
for the 1.x releases. The control-flow signals moved to
'worktoy.core.control_flow', beside the sentinels, and the refusal of an
attribute in a signal's class body, 'ControlClassError', moved to
'worktoy.waitaminute.meta' with the other refusals of a class-body line.
Import the names from there.

The names are resolved on access rather than at import, so importing
'worktoy.waitaminute' does not import 'worktoy.core', and the layering
of the packages holds. The package is deprecated: each name read from
it is handed out as before, with a 'DeprecatedPromise' naming the new
home of the name, given at the line that read it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import DeprecatedPromise

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

__all__ = [
  'ControlClassError',
  'ControlSpace',
  'MetaFlow',
  'ControlFlow',
  'SkipSet',
]


def _deprecate(name: str, home: str) -> None:
  """The '_deprecate' function gives the deprecation notice of a name
  read from this package, naming the package it lives in now."""
  feature = """%s.%s""" % (__name__, name)
  info = """Import it from '%s', where it lives now.""" % home
  DeprecatedPromise(feature, info).warn()


def __getattr__(name: str) -> Any:
  """Resolves a name of the family from its new home with a deprecation
  notice, or refuses it as a module refuses an attribute it does not
  have."""
  if name == 'ControlClassError':
    _deprecate(name, 'worktoy.waitaminute.meta')
    from ..meta import ControlClassError
    return ControlClassError
  if name in ('ControlSpace', 'MetaFlow', 'ControlFlow', 'SkipSet'):
    _deprecate(name, 'worktoy.core.control_flow')
    from ...core import control_flow
    return getattr(control_flow, name)
  infoSpec = "module '%s' has no attribute '%s'"
  raise AttributeError(infoSpec % (__name__, name))
