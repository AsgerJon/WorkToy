"""
TestBasicMeta tests some basic functionalities of the AbstractMetaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass, BaseMeta
from worktoy.waitaminute import QuestionableSyntax

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class TestBasicMeta(TestCase):
  """
  TestBasicMeta tests some basic functionalities of the AbstractMetaclass.
  """

  def test_good_class(self) -> None:
    """
    Test that the metaclass is set correctly.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with AbstractMetaclass as its metaclass.
      """

      def __getitem__(self, item: Any) -> Any:
        """
        Get an item from the class.
        """

      def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set an item in the class.
        """

      def __set_name__(self, name: str, owner: type) -> None:
        """
        Set the name of the class.
        """

  def test_bad_class(self) -> None:
    """
    Test that the metaclass is set correctly.
    """

    with self.assertRaises(QuestionableSyntax):
      class Foo(metaclass=AbstractMetaclass):
        """
        Foo is a class with AbstractMetaclass as its metaclass.
        """

        def __get_item__(self, item: Any) -> Any:
          """
          Get an item from the class.
          """

        def __set_item__(self, key: Any, value: Any) -> None:
          """
          Set an item in the class.
          """
