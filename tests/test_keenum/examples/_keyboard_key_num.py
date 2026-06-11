"""
KeyboardKeyNum subclasses 'KeeNum' and enumerates the keys on a keyboard.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeyboardKeyNum(KeeNum):
  """KeyboardKeyNum enumerates the keys on a keyboard."""
  A = Kee[str]("""A""")
  B = Kee[str]("""B""")
  C = Kee[str]("""C""")
  D = Kee[str]("""D""")
  E = Kee[str]("""E""")
  F = Kee[str]("""F""")
  G = Kee[str]("""G""")
  H = Kee[str]("""H""")
  I = Kee[str]("""I""")
  J = Kee[str]("""J""")
  K = Kee[str]("""K""")
  L = Kee[str]("""L""")
  M = Kee[str]("""M""")
  N = Kee[str]("""N""")
  O = Kee[str]("""O""")
  P = Kee[str]("""P""")
  Q = Kee[str]("""Q""")
  R = Kee[str]("""R""")
  S = Kee[str]("""S""")
  T = Kee[str]("""T""")
  U = Kee[str]("""U""")
  V = Kee[str]("""V""")
  W = Kee[str]("""W""")
  X = Kee[str]("""X""")
  Y = Kee[str]("""Y""")
  Z = Kee[str]("""Z""")
