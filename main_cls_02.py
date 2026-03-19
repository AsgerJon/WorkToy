"""
Testing __init_subclass__
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import textFmt


def main() -> int:
  class Base:

    @classmethod
    def __subclasshook__(cls, subclass, /):
      print(
        '__subclasshook__ is called with the following arguments: '
        'subclass: %s' % str(
          subclass,
          ),
        )

    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
      infoSpec = """__init_subclass__ is called with the following 
      arguments: args: %s, kwargs: %s"""
      info = infoSpec % (str(args), str(kwargs))
      print(textFmt(info))
      print(cls)

  class Child(Base, object):
    pass

  infoSpec = """Child class has the following bases: %s"""
  info = infoSpec % (str(Child.__bases__))
  print(textFmt(info))

  return 0
