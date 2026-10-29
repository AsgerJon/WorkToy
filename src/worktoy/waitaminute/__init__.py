"""The 'worktoy.waitaminute' package collects every custom exception in
the library. Exceptions are grouped into subpackages by the layer that
raises them ('desc', 'meta', 'dispatch', 'keenum' and 'ezdata'), with a
handful of cross-cutting exceptions
('TypeException', 'MissingVariable', and others) defined at the top level.

The guiding philosophy is fail-fast: 'worktoy' raises a specific, typed
exception rather than falling back silently or returning a sentinel a
caller might overlook. Each exception subclasses the built-in that best
matches its meaning ('TypeError', 'ValueError', 'AttributeError', and so
on) so existing 'except' clauses keep working. Every exception but the
control-flow signals is also a 'WorkToyException', the common base, so
one 'except WorkToyException' catches every exception of the library.

The 'control_flow' subpackage is a thin re-export kept for the 1.x
releases: the control-flow signals moved to 'worktoy.core.control_flow',
beside the sentinels, and 'ControlClassError' to 'meta'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._work_toy_exception import WorkToyException
from ._type_exception import TypeException
from ._variable_not_none import VariableNotNone
from ._unpack_exception import UnpackException
from ._subclass_exception import SubclassException
from ._missing_variable import MissingVariable
from . import desc
from . import meta
from . import dispatch
from . import keenum
from . import ezdata
from . import control_flow

__all__ = [
  'WorkToyException',
  'TypeException',
  'VariableNotNone',
  'UnpackException',
  'SubclassException',
  'MissingVariable',
  'desc',
  'meta',
  'dispatch',
  'keenum',
  'ezdata',
  'control_flow',
]
