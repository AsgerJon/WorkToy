"""
TestAliasMethodKinds subclasses 'DescTest' and pins that an 'Alias' of a
staticmethod or a classmethod behaves as the method it names. The alias
used to copy what reading the name from the class returned, after the
descriptor protocol had applied: a staticmethod came back as a plain
function, which then bound as a method and received the instance, and a
classmethod came back bound to the class declaring the alias, so a
subclass read it bound to the wrong class. An alias declared before the
name it stands for exists forwards each access instead, and its
staticmethod broke in the same way.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Alias
from worktoy.mcls import BaseObject

from . import DescTest


class Parent(BaseObject):
  """Parent holds the staticmethod and the classmethod the aliases name."""

  @staticmethod
  def helper(x: int) -> int:
    return x * 2

  @classmethod
  def who(cls) -> str:
    return cls.__name__


class Child(Parent):
  """Child aliases the methods of 'Parent'."""

  h = Alias('helper')
  w = Alias('who')


class GrandChild(Child):
  """GrandChild inherits the aliases."""


class Deferred(BaseObject):
  """Deferred declares aliases of names it does not define itself."""

  h = Alias('helper')
  w = Alias('who')


class Late(Deferred):
  """Late defines the names the aliases of 'Deferred' stand for."""

  @staticmethod
  def helper(x: int) -> int:
    return x * 3

  @classmethod
  def who(cls) -> str:
    return cls.__name__


class Later(Late):
  """Later inherits everything from 'Late'."""


class TestAliasMethodKinds(DescTest):
  """
  TestAliasMethodKinds provides tests for an 'Alias' of a staticmethod or
  a classmethod.
  """

  def test_static_through_instance(self) -> None:
    """An alias of a staticmethod read from an instance receives no
    instance."""
    self.assertEqual(Child().h(3), 6)
    self.assertEqual(GrandChild().h(4), 8)

  def test_static_through_class(self) -> None:
    """An alias of a staticmethod read from the class is the plain
    function."""
    self.assertEqual(Child.h(3), 6)

  def test_classmethod_binds_reading_class(self) -> None:
    """An alias of a classmethod binds to the class it is read from."""
    self.assertEqual(Child.w(), 'Child')
    self.assertEqual(GrandChild.w(), 'GrandChild')
    self.assertEqual(GrandChild().w(), 'GrandChild')

  def test_deferred_static(self) -> None:
    """A forwarding alias of a staticmethod receives no instance."""
    self.assertEqual(Late().h(3), 9)
    self.assertEqual(Later.h(2), 6)

  def test_deferred_classmethod(self) -> None:
    """A forwarding alias of a classmethod binds to the class it is read
    from."""
    self.assertEqual(Late.w(), 'Late')
    self.assertEqual(Later().w(), 'Later')
