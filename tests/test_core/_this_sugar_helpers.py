"""
Helpers for 'TestThisReference' and 'TestThisHandover' using the
subscripted decorator spelling '@THIS[Parent].x.onGet', which is syntax
only from Python 3.9 on, where PEP 614 let a decorator be any
expression. The two test modules import this module behind a
'sys.version_info' guard, so on Python 3.7 and 3.8 this file is never
parsed, and the tests calling into it are skipped there.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from worktoy.desc import AttriBox


# noinspection PyCompatibility
def decorateEveryHook(grand: type, log: list) -> type:
  """
  The 'decorateEveryHook' function returns a subclass of 'grand' whose
  body decorates the inherited 'x' through 'THIS[grand]' with each of
  the seven notification decorators, every callback appending to 'log'.
  """

  class Child(grand):
    """Child decorates the clone of 'x' seven times."""

    # noinspection PyCompatibility
    @THIS[grand].x.preGet
    def _a(self) -> None:
      log.append('preGet')

    # noinspection PyCompatibility
    @THIS[grand].x.onGet
    def _b(self, value: int) -> None:
      log.append(('onGet', value))

    # noinspection PyCompatibility
    @THIS[grand].x.preSet
    def _c(self, value: int) -> None:
      log.append(('preSet', value))

    # noinspection PyCompatibility
    @THIS[grand].x.onSet
    def _d(self, value: int) -> None:
      log.append(('onSet', value))

    # noinspection PyCompatibility
    @THIS[grand].x.preDelete
    def _e(self) -> None:
      log.append('preDelete')

    # noinspection PyCompatibility
    @THIS[grand].x.onDelete
    def _f(self) -> None:
      log.append('onDelete')

    # noinspection PyCompatibility
    @THIS[grand].x.setName
    def _g(cls, desc: AttriBox) -> None:
      log.append(('setName', cls.__name__, desc.getFieldName()))

  return Child


# noinspection PyCompatibility
def hookedChild(hooked: type, log: list) -> type:
  """
  The 'hookedChild' function returns a subclass of 'hooked' declared
  with the class keyword 'flag=True', which the holder's own
  '__init_subclass__' takes, whose body decorates the inherited 'x'
  through 'THIS[hooked]' with 'onSet', the callback appending the value
  to 'log'.
  """

  class Child(hooked, flag=True):
    """Child hands a keyword to the holder and decorates its 'x'."""

    # noinspection PyCompatibility
    @THIS[hooked].x.onSet
    def _w(self, value: int) -> None:
      log.append(value)

  return Child


# noinspection PyCompatibility
def boxedChild(boxed: type, log: list) -> type:
  """
  The 'boxedChild' function returns a subclass of 'boxed', a worktoy
  holder, whose body decorates the inherited 'x' through 'THIS[boxed]'
  with 'onGet', the callback appending the value to 'log'.
  """

  class Child(boxed):
    """Child decorates the 'x' of a worktoy holder."""

    # noinspection PyCompatibility
    @THIS[boxed].x.onGet
    def _w(self, value: int) -> None:
      log.append(value)

  return Child


# noinspection PyCompatibility
def twoHolders(parent: type, log: list) -> type:
  """
  The 'twoHolders' function returns a subclass of 'parent' whose body
  decorates 'x', which 'parent' inherits, and 'y', which 'parent'
  holds, both through 'THIS[parent]' with 'onGet', each callback
  appending its name and the value to 'log'.
  """

  class Child(parent):
    """Child decorates a descriptor of each of two holders."""

    # noinspection PyCompatibility
    @THIS[parent].x.onGet
    def _a(self, value: int) -> None:
      log.append(('x', value))

    # noinspection PyCompatibility
    @THIS[parent].y.onGet
    def _b(self, value: str) -> None:
      log.append(('y', value))

  return Child
