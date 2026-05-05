"""
NetworkPortNum subclasses 'KeeNum' and enumerates the well-known network
port numbers.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class NetworkPortNum(KeeNum):
  """NetworkPortNum enumerates well-known TCP ports."""
  SSH = Kee[int](22)
  SMTP = Kee[int](25)
  HTTP = Kee[int](80)
  HTTPS = Kee[int](443)
  POSTGRES = Kee[int](5432)
  REDIS = Kee[int](6379)
  HTTP_ALT = Kee[int](8080)
