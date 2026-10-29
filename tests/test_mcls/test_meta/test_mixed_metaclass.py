"""
TestMixedMetaclass pins that 'AbstractMetaclass' hands over with
'super()', so a metaclass mixed in beside 'BaseMeta' takes part: its
'__new__' and '__init__' run as the class is built, and its own
'__call__', '__instancecheck__', '__subclasscheck__', '__str__',
'__repr__', '__setattr__' and '__delattr__' run where the class declares
no hook. 'AbstractMetaclass' used to call 'MetaType' by name, which
passed over every one of them.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import MetaType
from worktoy.mcls import BaseMeta

from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

records = []


class Recording(MetaType):
  """Recording notes every method it takes part in, then hands over."""

  def __new__(mcls, name: str, bases: tuple, space: dict, **kw) -> Any:
    records.append('__new__')
    return super().__new__(mcls, name, bases, space, **kw)

  def __init__(cls, name: str, bases: tuple, space: Any, **kw) -> None:
    records.append('__init__')
    super().__init__(name, bases, space, **kw)

  def __call__(cls, *args, **kwargs) -> Any:
    records.append('__call__')
    return super().__call__(*args, **kwargs)

  def __instancecheck__(cls, obj: Any) -> bool:
    records.append('__instancecheck__')
    return super().__instancecheck__(obj)

  def __subclasscheck__(cls, subclass: type) -> bool:
    records.append('__subclasscheck__')
    return super().__subclasscheck__(subclass)

  def __str__(cls) -> str:
    records.append('__str__')
    return super().__str__()

  def __repr__(cls) -> str:
    records.append('__repr__')
    return super().__repr__()

  def __setattr__(cls, name: str, value: Any) -> None:
    records.append('__setattr__')
    super().__setattr__(name, value)

  def __delattr__(cls, name: str) -> None:
    records.append('__delattr__')
    super().__delattr__(name)


class Both(BaseMeta, Recording):
  """Both mixes 'Recording' in beside 'BaseMeta'."""


class TestMixedMetaclass(MCLSTest):
  """
  TestMixedMetaclass provides tests for a metaclass mixed in beside
  'BaseMeta'.
  """

  def test_resolution_order(self) -> None:
    """The mixed-in metaclass comes right after 'AbstractMetaclass'."""
    names = [meta.__name__ for meta in Both.__mro__]
    self.assertEqual(names[:5], [
      'Both', 'BaseMeta', 'AbstractMetaclass', 'Recording', 'MetaType',
    ])

  def test_construction(self) -> None:
    """The mixed-in '__new__' and '__init__' run as the class is built."""
    del records[:]

    class Thing(metaclass=Both):
      pass

    self.assertEqual(records, ['__new__', '__init__'])

  def test_defaults(self) -> None:
    """Where the class declares no hook, the mixed-in defaults run."""

    class Thing(metaclass=Both):
      pass

    del records[:]
    thing = Thing()
    self.assertFalse(isinstance(5, Thing))
    self.assertFalse(issubclass(int, Thing))
    self.assertEqual(str(Thing), 'Thing[metaclass=Both]')
    self.assertEqual(repr(Thing), 'Thing[metaclass=Both]')
    Thing.extra = 1
    del Thing.extra
    expected = [
      '__call__', '__instancecheck__', '__subclasscheck__', '__str__',
      '__repr__', '__setattr__', '__delattr__',
    ]
    self.assertEqual(records, expected)
    self.assertIs(type(thing), Thing)

  def test_hook_comes_first(self) -> None:
    """A class hook still takes the operation ahead of the mixed-in
    default."""

    class Thing(metaclass=Both):
      @classmethod
      def __class_str__(cls) -> str:
        return 'hooked'

    del records[:]
    self.assertEqual(str(Thing), 'hooked')
    self.assertEqual(records, [])
