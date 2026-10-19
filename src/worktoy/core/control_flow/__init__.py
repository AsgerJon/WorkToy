"""
The 'worktoy.core.control_flow' package provides the control-flow
signals, exceptions raised to steer a protocol rather than to report a
failure, much like 'StopIteration' and 'GeneratorExit'. A signal is a
stateless class used by its type alone, as a sentinel is used by its
identity, which is why the two families sit side by side in 'core'.

- MetaFlow: the metaclass behind the signals, based on 'MetaType' as
  every metaclass of the library is. It refuses every attribute in a
  signal's class body but '__str__' and '__repr__', through
  'ControlSpace', and keeps one root class.
- ControlSpace: the namespace object 'MetaFlow' prepares for a signal.
- ControlFlow: the root signal every other signal is based on.
- SkipSet: the one signal the library raises itself, from a
  descriptor's 'hookPreSet', telling 'Object.__set__' to skip the write.

The refusal of an attribute in a signal's class body, 'ControlClassError',
is an error and lives in 'worktoy.waitaminute.meta' with the other
refusals of a class-body line. The family lived in
'worktoy.waitaminute.control_flow' before; that package re-exports these
names for the 1.x releases.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._control_space import ControlSpace
from ._meta_flow import MetaFlow
from ._control_flow import ControlFlow
from ._skip_set import SkipSet

__all__ = [
  'ControlSpace',
  'MetaFlow',
  'ControlFlow',
  'SkipSet',
]
