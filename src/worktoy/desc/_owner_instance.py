"""Owner is a Zeroton object indicating the owner of the descriptor
instance.  """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import ZerotonMetaclass


class THIS(metaclass=ZerotonMetaclass):
  """Instance is a Zeroton object indicating the instance owning the
  descriptor instance.  """


class _Meta(ZerotonMetaclass):
  """This metaclass makes the SCOPE object consider the 'THIS' object as
  an instance of itself."""

  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    return True if instance is THIS else False


class SCOPE(metaclass=_Meta):
  """SCOPE is a Zeroton object indicating the class owning the descriptor
  instance.  """


class Owner(metaclass=ZerotonMetaclass):
  """Owner is a Zeroton object indicating the class owning the descriptor
  instance.  """
