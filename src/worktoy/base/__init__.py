"""The 'worktoy.base' module provides the base object class that leverages
the rest of the 'worktoy' library to provide convenient and powerful
functionality. The 'BaseObject' provides a general base class for most
use cases. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._load_space import LoadSpace
from ._base_metaclass import BaseMetaclass
from ._base_object import BaseObject
