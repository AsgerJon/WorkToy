"""The 'worktoy.desc' implements the descriptor protocol with lazy
instantiation. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_field import AbstractField
from ._base_field import BaseField

from ._core_descriptor import AbstractBox
from ._abstract_descriptor import NotifyBox
from ._bag import Bag
from ._field import Field
from ._attri_box import AttriBox
from ._explicit_box import ExplicitBox
