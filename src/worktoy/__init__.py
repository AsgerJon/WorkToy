"""The 'worktoy' package provides a collection of utilities leveraging
advanced python features including custom metaclasses and the descriptor
protocol. The readme file included provides detailed documentation on the
included features. The modules provided depend on each other in
implementation, but can be used independently.

The package consists of the following modules:
- utilities: A set of general-purpose utility functions and classes.
- waitaminute: Tools for managing execution flow and timing.
- core: Core functionalities and base classes for the package.
- desc: Descriptor protocol utilities.
- dispatch: Function and method dispatching used by overload system.
- mcls: Custom metaclass implementations.
- lorem_ipsum: Lorem ipsum text generation utilities.
- markwork: Markdown rendering utilities.
- num: Enumeration utilities.
- ezdata: Dataclass implementation.
- work_io: Input/output utilities for file and directory management.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import utilities
from . import waitaminute
from . import core
from . import dispatch
from . import desc
from . import mcls
from . import lorem_ipsum
from . import keenum
from . import ezdata
from . import work_io
from . import work_test

__all__ = [
  'utilities',
  'waitaminute',
  'core',
  'dispatch',
  'desc',
  'mcls',
  'lorem_ipsum',
  'keenum',
  'ezdata',
  'work_io',
  'work_test',
]
