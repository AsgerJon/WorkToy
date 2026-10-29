"""
TestAliasForwarding subclasses 'DescTest' and pins what an 'Alias' is: a
second name for a descriptor on the same class or a base of it. Through
an instance, the alias forwards every read, write and deletion to the
descriptor the real name holds on the class of that instance, looked up
afresh at each access, so a subclass that redeclares the field is served
by its own box, whichever name is read first. Through the class, the alias
is itself.

As the class is created the alias is held to what it stands for: a name
no class holds is refused with 'DanglingAlias', a name holding a plain
value with 'NotADescriptor', and a 'staticmethod' or 'classmethod', which
the class does not read as itself, with 'NotAliasable'. A plain function
may be aliased. The first two refusals come again from an access should
the name be removed or replaced on the class afterwards.

The alias used to swap itself for the target object as its class was
created, so a subclass redeclaring the field kept reaching the parent's
box through the alias and the first name read decided what both names
held afterwards.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Alias
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import NotADescriptor, NotAliasable
from worktoy.waitaminute.desc import DanglingAlias

from . import DescTest


class Geometry(BaseObject):
  """Geometry exposes 'width' under the second name 'w'."""

  width = AttriBox[list]([240])
  w = Alias('width')

  def method(self) -> str:
    return 'bound to %s' % type(self).__name__

  f = Alias('method')


class Parent(BaseObject):
  """Parent holds the field the alias stands for."""

  value = AttriBox[int](0)


class Child(Parent):
  """Child aliases the inherited field."""

  v = Alias('value')


class GrandChild(Child):
  """GrandChild redeclares the field under the alias."""

  value = AttriBox[int](9)


class TestAliasForwarding(DescTest):
  """
  TestAliasForwarding provides tests for 'Alias' forwarding each access
  to the descriptor the real name holds.
  """

  def test_instance_reads_the_same_object(self) -> None:
    """Through an instance both names give one object."""
    geometry = Geometry()
    self.assertEqual(geometry.w, [240])
    self.assertIs(geometry.w, geometry.width)

  def test_class_access_is_the_alias(self) -> None:
    """Through the class the alias is itself, not the box."""
    self.assertIs(Geometry.w, Geometry.__dict__['w'])
    self.assertIsInstance(Geometry.w, Alias)
    self.assertIsNot(Geometry.w, Geometry.width)

  def test_write_and_delete_through_either_name(self) -> None:
    """A write or a deletion through either name reaches the one field."""
    geometry = Geometry()
    geometry.w = [1]
    self.assertEqual(geometry.width, [1])
    geometry.width = [2]
    self.assertEqual(geometry.w, [2])
    del geometry.w
    with self.assertRaises(MissingVariable):
      _ = geometry.width

  def test_redeclared_field_whichever_name_is_read_first(self) -> None:
    """A subclass redeclaring the field is served by its own box through
    the alias, in either read order."""
    first = GrandChild()
    self.assertEqual((first.v, first.value), (9, 9))
    second = GrandChild()
    self.assertEqual((second.value, second.v), (9, 9))
    self.assertEqual(Child().v, 0)

  def test_plain_function_binds(self) -> None:
    """A plain function is read by the class as itself, so it may be
    aliased, and binds to the instance."""
    self.assertEqual(Geometry().f(), 'bound to Geometry')

    class Sub(Geometry):
      pass

    self.assertEqual(Sub().f(), 'bound to Sub')

  def test_rebinding_descriptor_refused(self) -> None:
    """An alias of a staticmethod or a classmethod is refused as the
    class is created, naming the real name and both kinds."""
    for kind in (staticmethod, classmethod):
      with self.subTest(kind=kind.__name__):
        with self.assertRaises((NotAliasable, RuntimeError)) as context:
          class Bad(BaseObject):
            helper = kind(lambda *args: None)
            h = Alias('helper')
        exception = self._unwrapSetName(context.exception, NotAliasable)
        self.assertIsInstance(exception, NotAliasable)
        self.assertIn('helper', str(exception))
        self.assertIn(kind.__name__, str(exception))

  def test_dangling_alias_refused(self) -> None:
    """An alias of a name no class holds is refused as the class is
    created, naming the alias and the real name."""
    with self.assertRaises((DanglingAlias, RuntimeError)) as context:
      class Dangling(BaseObject):
        m = Alias('missing')
    exception = self._unwrapSetName(context.exception, DanglingAlias)
    self.assertIsInstance(exception, DanglingAlias)
    self.assertIn('missing', str(exception))
    self.assertIn('Dangling.m', str(exception))

  def test_plain_value_refused(self) -> None:
    """An alias of a plain value is refused as the class is created,
    naming the real name and the value."""
    with self.assertRaises((NotADescriptor, RuntimeError)) as context:
      class Plain(BaseObject):
        plain = 5
        p = Alias('plain')
    exception = self._unwrapSetName(context.exception, NotADescriptor)
    self.assertIsInstance(exception, NotADescriptor)
    self.assertIn('plain', str(exception))

  def test_forwarding_proxy_refused(self) -> None:
    """This method tests that a value whose class forwards '__get__'
    through '__getattr__' passing as a descriptor does not happen: Python
    reads '__get__' off the type, so the alias is refused with
    'NotADescriptor' as the class is created."""

    class Proxy:
      def __init__(self, target: object) -> None:
        self._target = target

      def __getattr__(self, name: str) -> object:
        return getattr(self._target, name)

    def greet(self) -> str:
      return 'hi'  # pragma: no cover

    with self.assertRaises((NotADescriptor, RuntimeError)) as context:
      class Holder(BaseObject):
        value = Proxy(greet)
        v = Alias('value')
    exception = self._unwrapSetName(context.exception, NotADescriptor)
    self.assertIsInstance(exception, NotADescriptor)
    self.assertIn('value', str(exception))

  def test_target_removed_or_replaced_afterwards(self) -> None:
    """A name removed from the class after creation makes an access raise
    'DanglingAlias'; one replaced by a plain value, 'NotADescriptor'."""

    class Owner(BaseObject):
      width = AttriBox[int](1)
      w = Alias('width')

    owner = Owner()
    self.assertEqual(owner.w, 1)
    Owner.width = 5
    with self.assertRaises(NotADescriptor):
      _ = owner.w
    del Owner.width
    with self.assertRaises(DanglingAlias):
      _ = owner.w
    with self.assertRaises(DanglingAlias):
      owner.w = 2
