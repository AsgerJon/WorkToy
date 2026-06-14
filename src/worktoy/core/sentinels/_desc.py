"""
DESC sentinel provides a placeholder for the descriptor object in the
descriptor flow along with THIS and OWNER.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class DESC(Sentinel):
  """
  DESC is a sentinel placeholder for the descriptor object itself, used
  in deferred 'AttriBox' constructor arguments alongside THIS and OWNER.
  At access time it is replaced by the descriptor mediating the
  attribute access.
  """
