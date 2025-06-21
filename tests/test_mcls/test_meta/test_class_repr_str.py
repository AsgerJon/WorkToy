"""
TestClassReprStr tests the __class_repr__ and __class_str__ hooks
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import AbstractObject
from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class VerboseClass(metaclass=AbstractMetaclass):
  """
  VerboseClass defines __class_str__ and __class_repr__ for testing.
  """

  @classmethod
  def __class_str__(cls) -> str:
    """
    Custom str for the class object.
    """
    return 'this-is-the-str'

  @classmethod
  def __class_repr__(cls) -> str:
    """
    Custom repr for the class object.
    """
    return '<VerboseClass|repr>'


class SilentClass:
  """
  SilentClass does not override str or repr hooks.
  """


class TestClassStrRepr(TestCase):
  """
  TestClassStrRepr checks the class-level string and repr hooks.
  """

  def testClassStrHook(self) -> None:
    """
    Tests that __class_str__ is used in str(class).
    """
    self.assertEqual(str(VerboseClass), 'this-is-the-str')

  def testClassReprHook(self) -> None:
    """
    Tests that __class_repr__ is used in repr(class).
    """
    self.assertEqual(repr(VerboseClass), '<VerboseClass|repr>')

  def testDefaultStr(self) -> None:
    """
    Tests fallback to type.__str__ if no __class_str__.
    """
    out = str(SilentClass)
    self.assertTrue(out.startswith("<class '"))
    self.assertIn('SilentClass', out)

  def testDefaultRepr(self) -> None:
    """
    Tests fallback to type.__repr__ if no __class_repr__.
    """
    out = repr(SilentClass)
    self.assertTrue(out.startswith("<class '"))
    self.assertIn('SilentClass', out)
