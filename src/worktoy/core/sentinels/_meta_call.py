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
  A class built by 'AbstractMetaclass' may define hooks such as
  '__class_len__' that the metaclass consults for operations on the class
  itself. The metaclass needs to tell a class defining a hook from one
  that does not with one cheap comparison, and a subclass needs a way to
  undo a hook it inherits.

  Implementation
  --------------

  'NamespaceHook' gives every hook nothing defines the value 'METACALL',
  and the metaclass then performs the operation as for a plain class. A
  subclass setting an inherited hook to 'METACALL' hands the operation
  back to the metaclass.
  """
