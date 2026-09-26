"""
TestKeeNumClassInit subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that a 'KeeNum' class takes part in the class-creation
protocol of 'AbstractMetaclass' like any other worktoy class: its
'__class_init__' hook runs once the class is complete, and each base
hears of the new subclass through '__subclasshook__'. 'KeeMeta.__init__'
builds the members of the enumeration, and the hook runs after that, so
it sees the finished members.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee, KeeSpace

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestKeeNumClassInit(KeeTest):
  """
  TestKeeNumClassInit provides tests for the '__class_init__' and
  '__subclasshook__' hooks on 'KeeNum' classes.
  """

  def test_class_init_sees_members(self) -> None:
    """
    The '__class_init__' of a 'KeeNum' class runs once, after the members
    exist, so the hook can read them.
    """
    calls = []

    class Hooked(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)

      @classmethod
      def __class_init__(cls, name: str, bases: Any, space: Any,
                         **kwargs) -> None:
        calls.append((cls, [member.name for member in cls]))

    self.assertEqual(calls, [(Hooked, ['A', 'B'])])

  def test_class_init_arguments(self) -> None:
    """
    The hook receives the class name, the bases, the namespace, and the
    keyword arguments of the class statement.
    """
    received = []

    class Hooked(KeeNum, flavour='plain'):
      A = Kee[int](1)

      @classmethod
      def __class_init__(cls, name: str, bases: Any, space: Any,
                         **kwargs) -> None:
        received.append((name, bases, space, kwargs))

    (name, bases, space, kwargs), = received
    self.assertEqual(name, 'Hooked')
    self.assertEqual(bases, (KeeNum,))
    self.assertIsInstance(space, KeeSpace)
    self.assertEqual(kwargs, {'flavour': 'plain'})
    self.assertEqual(len(Hooked), 1)

  def test_inherited_class_init(self) -> None:
    """
    A subclass inherits the hook, which runs again for the subclass and
    sees the inherited members followed by the new ones.
    """
    calls = []

    class Hooked(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __class_init__(cls, name: str, bases: Any, space: Any,
                         **kwargs) -> None:
        calls.append((cls, [member.name for member in cls]))

    class Child(Hooked):
      B = Kee[int](2)

    self.assertEqual(calls, [(Hooked, ['A']), (Child, ['A', 'B'])])

  def test_base_hears_of_subclass(self) -> None:
    """
    Each base of a new 'KeeNum' class is handed the new class through
    its '__subclasshook__', as 'AbstractMetaclass' does for every class
    it builds.
    """
    notes = []

    class Parent(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __subclasshook__(cls, subclass: type) -> None:
        notes.append((cls, subclass))

    class Child(Parent):
      B = Kee[int](2)

    self.assertEqual(notes, [(Parent, Child)])
