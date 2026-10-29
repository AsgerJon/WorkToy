"""
TestOwnerLookup subclasses 'DescTest' from the 'tests.test_desc' package
and pins that a descriptor finds its notification callbacks and the
accessors of a 'Field' on the class of the instance with
'type.__getattribute__', so a metaclass reimplementing
'__getattribute__' cannot answer in their place. They used to be read with
'getattr', which runs whatever the metaclass puts in front of the class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, Field

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _impostor(*args, **kwargs) -> str:
  """Stands in for every name the metaclasses below intercept."""
  return 'impostor'


class TestOwnerLookup(DescTest):
  """
  TestOwnerLookup provides tests for callbacks and accessors defined on a
  class whose metaclass reimplements '__getattribute__'.
  """

  def test_notification_callback(self) -> None:
    """An 'onSet' callback runs as the class defines it."""
    calls = []

    class Intercepting(type):
      def __getattribute__(cls, name: str) -> Any:
        if name == '_onLevel':
          return _impostor
        return type.__getattribute__(cls, name)

    class Gauge(metaclass=Intercepting):
      level = AttriBox[int](0)

      @level.onSet
      def _onLevel(self, value: int) -> None:
        calls.append(value)

    gauge = Gauge()
    gauge.level = 3
    self.assertEqual(calls, [3])

  def test_set_name_callback(self) -> None:
    """A 'setName' callback runs as the class defines it."""
    calls = []

    class Intercepting(type):
      def __getattribute__(cls, name: str) -> Any:
        if name == '_named':
          return _impostor
        return type.__getattribute__(cls, name)

    class Gauge(metaclass=Intercepting):
      level = AttriBox[int](0)

      @classmethod
      @level.setName
      def _named(cls, desc: Any) -> None:
        calls.append(desc.getFieldName())

    self.assertEqual(calls, ['level'])

  def test_field_accessors(self) -> None:
    """A 'Field' reads, writes and deletes through the accessors the class
    defines."""

    class Intercepting(type):
      def __getattribute__(cls, name: str) -> Any:
        if name in ('_getValue', '_setValue', '_deleteValue'):
          return _impostor
        return type.__getattribute__(cls, name)

    class Holder(metaclass=Intercepting):
      value = Field()
      _stored = 0

      @value.GET
      def _getValue(self) -> int:
        return self._stored

      @value.SET
      def _setValue(self, newValue: int) -> None:
        self._stored = newValue

      @value.DELETE
      def _deleteValue(self) -> None:
        self._stored = -1

    holder = Holder()
    holder.value = 7
    self.assertEqual(holder.value, 7)
    del holder.value
    self.assertEqual(holder.value, -1)
