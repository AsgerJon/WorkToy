"""
AccessNum enumerates descriptor access operations.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import KeeNum, Kee


class AccessNum(KeeNum):
  """
  AccessNum enumerates descriptor access operations.
  """

  GET = Kee[str]('__get__')
  SET = Kee[str]('__set__')
  DELETE = Kee[str]('__delete__')
