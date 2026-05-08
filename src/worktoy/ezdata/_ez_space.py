"""``EZSpace`` is the namespace class used by ``EZMeta``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ..mcls import BaseSpace
from ._ez_space_hook import EZSpaceHook


class EZSpace(BaseSpace):
  """Namespace for ``EZData`` classes; carries the ``EZSpaceHook``."""

  ezHook = EZSpaceHook()
