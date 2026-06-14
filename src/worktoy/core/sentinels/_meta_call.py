"""
METACALL sentinel specifies that a class defers to the metaclass for the
class dunder hooks.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class METACALL(Sentinel):
  """
  METACALL marks a class-level dunder hook as deferred to the metaclass.
  When 'AbstractMetaclass' finds this sentinel as the value of a hook
  such as '__class_str__' or '__class_iter__', it falls back to its own
  implementation instead of calling the hook on the class.
  """
