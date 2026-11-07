"""
attribute_ladder.py times one read and one write of an attribute of
each kind worktoy offers beside the plain ones Python offers, so that
the cost of a box is a measured number rather than a feeling.

Run it with the interpreter whose number is wanted, from the repository
root, with 'src' on the path:

    PYTHONPATH=src python -B bin/dev_tooling/bench/attribute_ladder.py

Each row is the best of three runs of 600000 accesses, in nanoseconds
per access. The results of 2026-11-07 on 3.7, 3.14 and 3.15 are in
attribute_ladder_results.md beside this file.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import timeit

from worktoy.mcls import BaseObject
from worktoy.desc import AttriBox, FastBox, Field


class Plain:
  """An attribute in the instance dictionary."""

  def __init__(self) -> None:
    self.x = 1


class Slotted:
  """An attribute in a slot."""
  __slots__ = ('x',)

  def __init__(self) -> None:
    self.x = 1


class WithProperty:
  """A property reading one attribute and adding one."""

  def __init__(self) -> None:
    self._x = 1

  @property
  def y(self) -> int:
    return self._x + 1


class Fast:
  """A FastBox: one check, one store."""
  x = FastBox[int](1)


class Boxed(BaseObject):
  """An AttriBox and a Field whose getter reads the box and adds one."""
  x = AttriBox[int](1)
  y = Field()

  @y.GET
  def _getY(self) -> int:
    return self.x + 1


def main() -> int:
  """Time every row and print the table"""
  objects = dict(plain=Plain(), slotted=Slotted(), prop=WithProperty(),
                 fast=Fast(), boxed=Boxed())
  for obj in objects.values():
    obj.x = 1
  count = 600000
  rows = [
    ('plain attribute (instance dict)', 'plain', 'x', True),
    ('plain attribute, __slots__', 'slotted', 'x', True),
    ('FastBox[int]', 'fast', 'x', True),
    ('AttriBox[int] on BaseObject', 'boxed', 'x', True),
    ('property (reads _x + 1)', 'prop', 'y', False),
    ('Field with GET (reads x + 1)', 'boxed', 'y', False),
  ]
  print('Python %d.%d.%d' % sys.version_info[:3])
  print('%-34s %9s %9s' % ('', 'read', 'write'))
  for label, key, attr, writable in rows:
    space = {'o': objects[key]}
    read = min(timeit.repeat('o.%s' % attr, globals=space,
                             number=count, repeat=3)) / count * 1e9
    if writable:
      write = min(timeit.repeat('o.%s = 2' % attr, globals=space,
                                number=count, repeat=3)) / count * 1e9
      print('%-34s %6.0f ns %6.0f ns' % (label, read, write))
    else:
      print('%-34s %6.0f ns %9s' % (label, read, '-'))
  return 0


if __name__ == '__main__':
  sys.exit(main())
