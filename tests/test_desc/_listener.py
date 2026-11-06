"""
Listener is a 'Watched' overriding two callbacks as other kinds of method.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Watched


class Listener(Watched):
  """
  A callback is found by name on the class of the instance at each
  access, so a subclass overrides it by defining the name again, as any
  kind of method. 'Listener' overrides the plain 'onGet' method with a
  staticmethod and the 'preSet' classmethod with a plain method.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _afterRead(value: int) -> None:
    Watched.log.append(('sub-onGet', value))

  def _beforeWrite(self, value: int) -> None:
    Watched.log.append(('sub-preSet', value))
