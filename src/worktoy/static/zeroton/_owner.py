"""
'OWNER' provides a companion to 'THIS' allowing references to both a class
and an instance of a class respectively. This relationship is emphasized,
is reflected by 'THIS' being recognized by 'OWNER' as an instance of it.

For example:

import sys

def main() -> int:
  if isinstance(THIS, OWNER):
    return 0
  return 1

if __name__ == '__main__':
  sys.exit(main())  # Returns 0, as 'THIS' is an instance of 'OWNER'
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...text import monoSpace

from . import Zeroton, THIS


class OWNER(metaclass=Zeroton):
  """Similar to THIS, but referring to the bound class object instead. """

  @classmethod
  def __class_str__(cls, ) -> str:
    """Return the class name of the class."""
    infoSpec = """The '%s' Zeroton is a placeholder for the class object 
    of the surrounding scope. When used in the same context as 'THIS', 
    it refers to the class object of the surrounding scope and 'THIS' 
    refers to the instance of the class."""
    return monoSpace(infoSpec % cls.__name__)

  @classmethod
  def __class_instancecheck__(cls, obj: object) -> bool:
    """When 'OWNER' and 'THIS' occurs in the same context, generally,
    'THIS' is a placeholder for an instance of the class for which 'OWNER'
    is a placeholder. """
    return True if cls is obj or obj is THIS else False
