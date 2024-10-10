"""The 'worktoy' package provides a collection of utilities leveraging
advanced python features including custom metaclasses and the descriptor
protocol. The readme file included provides detailed documentation on the
included features. The modules provided depend on each other in
implementation, but can be used independently. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from . import text
from . import parse
from . import meta
from . import desc
from . import base
from . import ezdata
from . import keenum

__all__ = ['desc', 'ezdata', 'keenum', 'meta', 'base', 'parse', 'text']
