"""
AccessNum enumerates descriptor access operations.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class AccessNum(KeeNum):
  """
  AccessNum enumerates descriptor access operations.
  """

  GET = Kee[str]('__get__')
  SET = Kee[str]('__set__')
  DELETE = Kee[str]('__delete__')
