"""
TestSubclassCheck checks that classes derived from the 'AbstractMetaclass'
can customize the behaviour of the 'issubclass' method when testing if
another object should be regarded as a subclass of the class. A numeric
class could for example implement the classmethod
'__class_subclass_check__' such as to consider float and int objects as
subclasses of itself.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import MCLSTest
from worktoy.mcls import AbstractMetaclass

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Nummer(metaclass=AbstractMetaclass):
  """
  'Nummer' is a numeric class that considers float and int objects as
  subclasses of itself.
  """

  @classmethod
  def __class_subclasscheck__(cls, subcls: type) -> bool:
    """
    Custom subclass check for the Nummer class.
    """
    if subcls is cls:
      return True
    if subcls is int or subcls is float:
      return True
    for base in subcls.__mro__:
      if base is cls:
        return True
    return False


class TestSubclassCheck(MCLSTest):
  """
  TestSubclassCheck checks that classes derived from the 'AbstractMetaclass'
  can customize the behaviour of the 'issubclass' method when testing if
  another object should be regarded as a subclass of the class.
  """

  def assertIsSubclass(self, subclass: type, cls: Any) -> None:
    """
    Asserts that the given class is a subclass of the specified subclass.
    """
    self.assertTrue(issubclass(subclass, cls))

  def assertIsNotSubclass(self, subclass: type, cls: Any) -> None:
    """
    Asserts that the given class is not a subclass of the specified subclass.
    """
    self.assertFalse(issubclass(subclass, cls))

  def test_subclass_check(self) -> None:
    """
    Tests that the custom subclass check works as expected.
    """
    self.assertIsSubclass(int, Nummer)
    self.assertIsSubclass(float, Nummer)

  def test_non_strict_self_sub(self) -> None:
    """issubclass(a, a) should always return True."""
    self.assertIsSubclass(Nummer, Nummer)

  def test_non_subclass(self) -> None:
    self.assertIsNotSubclass(str, Nummer)

  def test_deep_subclass(self) -> None:
    """
    Tests that a subclass of a subclass is still considered a subclass.
    """

    class En(Nummer):
      pass

    class To(En):
      pass

    class Tre(To):
      pass

    self.assertIsSubclass(Tre, Nummer)
