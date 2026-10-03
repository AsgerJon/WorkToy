"""
TestKeeValueTypeDeclared subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that the 'valueType' of an enumeration is the type its
members were declared with, 'T' in 'Kee[T]'. It used to be the type of the
value of the first member, and every other value had to be an instance of
that, so three enumerations that build without complaint broke every
lookup reaching the value step, even one that should simply miss: values
of different subclasses of 'T', mixed values under 'Kee[object]', and a
'bool' first among 'int' values. 'KeeBox' reads the same type.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest


class Animal:
  """Animal is the declared value type of 'Pets'."""


class Dog(Animal):
  """Dog is a subclass of 'Animal', the value of the first member."""


class Pets(KeeNum):
  """Pets holds values of 'Animal' and of its subclass 'Dog'."""

  DOG = Kee[Animal](Dog())
  GENERIC = Kee[Animal](Animal())


class Mixed(KeeNum):
  """Mixed holds values of different types under 'Kee[object]'."""

  ONE = Kee[object](1)
  DEUX = Kee[object]('deux')


class Bits(KeeNum):
  """Bits holds a 'bool' first among its 'int' values."""

  ON = Kee[int](True)
  TWO = Kee[int](2)


class Kennel(BaseObject):
  """Kennel holds a 'KeeBox' of 'Pets'."""

  pet = KeeBox[Pets]()


class TestKeeValueTypeDeclared(KeeTest):
  """
  TestKeeValueTypeDeclared provides tests for the 'valueType' of an
  enumeration whose values are not all of one exact type.
  """

  def test_value_type_is_declared(self) -> None:
    """'valueType' is the declared type, not the type of the first
    value."""
    self.assertIs(Pets.valueType, Animal)
    self.assertIs(Mixed.valueType, object)
    self.assertIs(Bits.valueType, int)

  def test_subclass_values_resolve(self) -> None:
    """A value of the declared type resolves when the first value is of a
    subclass."""
    self.assertIs(Pets(Pets.GENERIC.value), Pets.GENERIC)
    self.assertIs(Pets(Pets.DOG.value), Pets.DOG)

  def test_subclass_miss(self) -> None:
    """A value matching no member misses with 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      Pets(Animal())

  def test_mixed_values_resolve(self) -> None:
    """Values of different types under 'Kee[object]' each resolve."""
    self.assertIs(Mixed(1), Mixed.ONE)
    self.assertIs(Mixed('deux'), Mixed.DEUX)

  def test_bool_first_resolves(self) -> None:
    """An 'int' value resolves when the first value is a 'bool'."""
    self.assertIs(Bits(2), Bits.TWO)

  def test_kee_box_subclass_value(self) -> None:
    """A 'KeeBox' resolves a value of the declared type."""
    kennel = Kennel()
    kennel.pet = Pets.GENERIC.value
    self.assertIs(kennel.pet, Pets.GENERIC)

  def test_bool_refused_as_int_value(self) -> None:
    """'Bits' is an 'int' enumeration, so as for any such enumeration a
    'bool' never resolves by value, while the 'int' equal to it does,
    and the 'bool' member is still found by name and by index."""
    with self.assertRaises(KeeResolveError):
      Bits(True)
    self.assertIs(Bits(1), Bits.ON)
    self.assertIs(Bits('on'), Bits.ON)
    self.assertIs(Bits[0], Bits.ON)
