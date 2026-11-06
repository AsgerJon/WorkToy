"""
Particle is a plain class with 'FastBox' attributes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox


class Particle:
  """
  A 'FastBox' serves a plain class whose instances have a '__dict__':
  one shared declared value, cast once, or a new value of the field type
  per instance for empty parentheses. 'Particle' declares one of each,
  and a text.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  mass = FastBox[float](1)
  tags = FastBox[list]()
  name = FastBox[str]('particle')
