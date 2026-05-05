"""
ChessPieceNum subclasses 'KeeNum' and enumerates the chess piece categories.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee


class ChessPieceNum(KeeNum):
  """ChessPieceNum enumerates the six chess piece types."""
  PAWN = Kee[str]("""Bonde""")
  KNIGHT = Kee[str]("""Springer""")
  BISHOP = Kee[str]("""Løber""")
  ROOK = Kee[str]("""Tårn""")
  QUEEN = Kee[str]("""Dronning""")
  KING = Kee[str]("""Konge""")
