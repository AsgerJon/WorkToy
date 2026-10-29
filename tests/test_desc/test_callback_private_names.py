"""
TestCallbackPrivateNames subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a private callback or accessor, one whose name
starts with two underscores, is recorded under the name the class body
stores it at, '_Account__audit' for '__audit' in 'Account', and is found
at access. It used to be recorded as written, so the class was created
and the first access failed with 'AttributeError', or, on an owner with
'__getattr__', read that method's answer in place of the field. Like any
private name it is not overridden by a subclass, and a private function
whose qualified name names no class is refused with 'NamelessCallback'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable

from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import NamelessCallback

from . import DescTest


class Account(BaseObject):
  """Account audits its balance in a private callback."""

  balance = AttriBox[int](0)

  @balance.onSet
  def __audit(self, value: int) -> None:
    self.__dict__.setdefault('audited', []).append(value)


class Audited(Account):
  """Audited defines its own '__audit', which mangles to its own name."""

  def __audit(self, value: int) -> None:
    self.__dict__.setdefault('subAudited', []).append(value)


class Lenient(BaseObject):
  """Lenient answers unknown names in '__getattr__'."""

  balance = AttriBox[int](0)

  @balance.onGet
  def __seen(self, value: int) -> None:
    self.__dict__['seen'] = value

  def __getattr__(self, name: str) -> Any:
    return 'fallback for %s' % name


class Temperature(BaseObject):
  """Temperature reads its field through a private accessor."""

  celsius = Field()

  @celsius.GET
  def __getCelsius(self) -> int:
    return 21


class Outer:
  """Outer holds a nested class with a private callback."""

  class Inner(BaseObject):
    """Inner notes its value in a private callback."""

    value = AttriBox[int](0)

    @value.onSet
    def __note(self, value: int) -> None:
      self.__dict__['noted'] = value


def makeLocalClass() -> type:
  """Builds a class with a private callback inside a function."""

  class Local(BaseObject):
    """Local notes its value in a private callback."""

    value = AttriBox[int](0)

    @value.onSet
    def __note(self, value: int) -> None:
      self.__dict__['noted'] = value

  return Local


def makePrivateFunction() -> Callable:
  """Builds a private function outside any class body."""

  def __helper(self: Any, value: int) -> None:
    pass

  return __helper


class TestCallbackPrivateNames(DescTest):
  """
  TestCallbackPrivateNames provides tests for callbacks and accessors
  written with private names.
  """

  def test_on_set_private(self) -> None:
    """A private 'onSet' callback is recorded mangled and runs."""
    box = Account.__dict__['balance']
    self.assertEqual(box._getOnSetKeys(), ('_Account__audit',))
    account = Account()
    account.balance = 5
    self.assertEqual(account.balance, 5)
    self.assertEqual(account.audited, [5])

  def test_owner_getattr_not_consulted(self) -> None:
    """On an owner defining '__getattr__', the field reads its value and
    the private callback runs, where the miss used to fall through to
    '__getattr__'."""
    lenient = Lenient()
    self.assertEqual(lenient.balance, 0)
    self.assertEqual(lenient.seen, 0)

  def test_accessor_private(self) -> None:
    """A private 'Field' accessor is recorded mangled and read."""
    self.assertEqual(Temperature().celsius, 21)

  def test_private_not_overridden(self) -> None:
    """A subclass's own '__audit' mangles to its own name and does not
    replace the base's callback, as with any private name."""
    audited = Audited()
    audited.balance = 3
    self.assertEqual(audited.audited, [3])
    self.assertNotIn('subAudited', audited.__dict__)

  def test_nested_class(self) -> None:
    """A nested class mangles with its own name."""
    inner = Outer.Inner()
    inner.value = 4
    self.assertEqual(inner.noted, 4)

  def test_class_made_in_function(self) -> None:
    """A class made inside a function mangles with its own name."""
    local = makeLocalClass()()
    local.value = 6
    self.assertEqual(local.noted, 6)

  def test_set_name_private(self) -> None:
    """A private 'setName' classmethod callback runs."""
    names = []

    class Named(BaseObject):
      value = AttriBox[int](0)

      @classmethod
      @value.setName
      def __named(cls, desc: AttriBox) -> None:
        names.append(desc.getFieldName())

    self.assertEqual(names, ['value'])

  def test_no_class_refused(self) -> None:
    """A private function whose qualified name names no class could
    never be found, and is refused with 'NamelessCallback'."""
    with self.assertRaises(NamelessCallback):
      AttriBox[int](0).onSet(makePrivateFunction())
