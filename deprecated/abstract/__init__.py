"""The 'worktoy.abstract' module provides abstract functionality used
across the 'worktoy' library. The decorators found herein require specific
metaclass level support to function such as provide by the 'worktoy.meta'
module. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_flag import AbstractFlag
from ._abstract import Abstract, abstract
