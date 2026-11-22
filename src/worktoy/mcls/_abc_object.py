"""
ABCObject is the base of the classes that declare abstract methods.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import BaseObject, ABCMeta


class ABCObject(BaseObject, metaclass=ABCMeta):
  """
  A class that declares methods with '@abstract' is built by 'ABCMeta',
  and would otherwise name that metaclass in its class statement, each
  time. It needs a base to be based on instead, as a worktoy class is
  based on 'BaseObject' and names no metaclass:

    class Model(ABCObject):

      @abstract
      def rowCount(self) -> int: ...

  Implementation
  --------------

  'ABCObject' is 'BaseObject' built by 'ABCMeta', with a body of its
  own that holds nothing: it is to 'ABCMeta' what 'BaseObject' is to
  'BaseMeta'. A class based on it is built by 'ABCMeta' in turn, and
  keeps everything a 'BaseObject' gives. It declares nothing abstract
  itself, so it is no abstract class, and an object may be made of it,
  as of 'BaseObject'.
  """
