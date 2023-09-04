"""WorkSide - Style data - Font weights
This file contains a list of names of font weights used to create the
symbolic classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

WEIGHTS = {
  'thin': 100,
  'extraLight': 200,
  'light': 300,
  'normal': 400,
  'medium': 500,
  'demiBold': 600,
  'bold': 700,
  'extraBold': 800,
  'black': 900,
}

WEIGHTS = {k: v for (v, k) in enumerate(WEIGHTS.keys())}
