"""
KeeSpace provides the namespace object for the KeeMeta metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..mcls import AbstractNamespace
from . import KeeHook  # Private to module

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeeSpace(AbstractNamespace):
  """
  KeeSpace provides the namespace object for the KeeMeta metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  keeHook = KeeHook()
