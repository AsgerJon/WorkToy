"""
TestMoreSpace does some more testing of the AbstractNamespace class. This
is because the 'unittest' module is not fit for purpose.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import BaseMeta, AbstractNamespace
from worktoy.utilities import stringList

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = AbstractNamespace


class HookedMeta(BaseMeta):
  """Test metaclass for testing the AbstractNamespace class."""

  def __new__(mcls, name: str, bases: Bases, space: Space, **kw) -> Self:
    """The __new__ method is invoked to create the class."""
    strSpace = str(space)
    reprSpace = repr(space)
    space['__str_space__'] = strSpace
    space['__repr_space__'] = reprSpace
    return BaseMeta.__new__(mcls, name, bases, space, **kw)


class TrustedClass(trustMeBro=True, metaclass=HookedMeta):
  """
  TrustedClass is a class that is used to test the AbstractNamespace class.
  It is a simple class that has a metaclass that adds some hooks to the
  namespace.
  """


class SusClass(metaclass=HookedMeta):  # No trustMeBro=True
  """
  SusClass is a class that is used to test the AbstractNamespace class.
  It is a simple class that has a metaclass that adds some hooks to the
  namespace.
  """


class TestMoreSpace(TestCase):
  """
  TestMoreSpace does some more testing of the AbstractNamespace class.
  """

  @classmethod
  def tearDownClass(cls):
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_str_repr(self) -> None:
    """
    Tests that the string representation of the AbstractNamespace class
    is correct.
    """

  def test_ad_hoc(self) -> None:
    """
    Tests that the AbstractNamespace class can be used as an ad-hoc
    namespace.
    """

    trustedNames = stringList("""HookedMeta, TrustedClass""")
    susNames = stringList("""HookedMeta, SusClass, """)
    for trustedName in trustedNames:
      self.assertIn(trustedName, TrustedClass.__str_space__)
      self.assertIn(trustedName, TrustedClass.__repr_space__)

    for susName in susNames:
      self.assertIn(susName, SusClass.__str_space__)
      self.assertIn(susName, SusClass.__repr_space__)

    self.assertIn('trustMeBro', TrustedClass.__repr_space__)
    self.assertNotIn('trustMeBro', SusClass.__repr_space__)
