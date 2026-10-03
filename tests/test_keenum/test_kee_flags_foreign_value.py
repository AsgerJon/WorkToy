"""
TestKeeFlagsForeignValue subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins how a 'KeeFlags' class resolves an identifier that is
neither a member, a name, an index nor a collection of names. Such an
identifier is looked up by value, and a value compares only with member
values of its own type. Comparing it with every member value instead
hands the decision to its own '__eq__' whenever the member value cannot
decide: 'unittest.mock.ANY' then equals the first member and resolves to
'NULL', and an 'RGB', which reads the channels of the other operand,
raises 'AttributeError' from the lookup and from 'in' alike. An identifier
matching no member raises 'KeeResolveError', which 'in' reports as absent.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest.mock import ANY

from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest
from .examples import FileAccess, FlagsExample, RGB


class TestKeeFlagsForeignValue(KeeTest):
  """
  TestKeeFlagsForeignValue provides tests for the lookup by value of
  'KeeFlags' classes, with identifiers of types foreign to the values of
  the members.
  """

  def test_equal_to_anything_does_not_resolve(self) -> None:
    """
    Calling or subscripting a flags class with 'unittest.mock.ANY' raises
    'KeeResolveError', whether the member values are the default indices
    or the 'bytes' of 'FileAccess'.
    """
    for cls in (FlagsExample, FileAccess):
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(KeeResolveError):
          cls(ANY)
        with self.assertRaises(KeeResolveError):
          _ = cls[ANY]

  def test_equal_to_anything_is_not_member(self) -> None:
    """
    'unittest.mock.ANY' is not in a flags class.
    """
    for cls in (FlagsExample, FileAccess):
      with self.subTest(cls=cls.__name__):
        self.assertNotIn(ANY, cls)

  def test_foreign_value_does_not_resolve(self) -> None:
    """
    An 'RGB' matches no member, so resolving it raises 'KeeResolveError'
    and it is not in the class, although its '__eq__' raises when asked
    about a member value.
    """
    for cls in (FlagsExample, FileAccess):
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(KeeResolveError):
          cls(RGB(1, 2, 3))
        self.assertNotIn(RGB(1, 2, 3), cls)

  def test_other_number_type_does_not_resolve(self) -> None:
    """
    A value compares only with member values of its own type, as a
    'KeeNum' looks up only instances of its value type: '3.0' does not
    find the member of 'FlagsExample' whose value is the index '3'.
    """
    with self.assertRaises(KeeResolveError):
      FlagsExample(3.0)
    self.assertNotIn(3.0, FlagsExample)

  def test_member_is_not_its_value(self) -> None:
    """
    A member is not equal to its own value: its '__eq__' declines anything
    that is not a member of a flags class.
    """
    for cls in (FlagsExample, FileAccess):
      for member in cls:
        with self.subTest(member=str(member)):
          self.assertNotEqual(member, member.value)

  def test_value_resolves(self) -> None:
    """
    A value of the type the member values have resolves to the member
    holding it, and one matching no member raises 'KeeResolveError'.
    """
    for member in FileAccess:
      with self.subTest(member=member.name):
        self.assertIs(FileAccess(member.value), member)
    with self.assertRaises(KeeResolveError):
      FileAccess(b'\xff')

  def test_value_of_subclass_resolves(self) -> None:
    """
    A value of a subclass of the type the member values have counts as a
    value of that type, as it does for a 'KeeNum', so a 'bytes' subclass
    finds the member of 'FileAccess' holding an equal value.
    """

    class Bits(bytes):
      pass

    for member in FileAccess:
      with self.subTest(member=member.name):
        self.assertIs(FileAccess(Bits(member.value)), member)
