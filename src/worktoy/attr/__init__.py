"""The 'worktoy.attr' module provides implementations of the descriptor
protocol for use in the 'worktoy' library. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_descriptor import AbstractDescriptor
from ._abstract_field import AbstractField
from ._field import Field
from ._abstract_box import AbstractBox
from ._attri_box import AttriBox
from ._explicit_box import ExplicitBox
