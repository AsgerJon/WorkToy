#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence

import unittest
from typing import Union, TypeAlias, NoReturn
from unittest import TestCase

from worktoy.core import unStupid

Numerical: TypeAlias = Union[int, float, complex]


class TestUnStupid(TestCase):
  def test_extract_union_types(self) -> NoReturn:
    # Define a Union type
    MyUnion = Union[int, str, bool]

    # Extract the types from the Union
    types = unStupid(MyUnion)

    # Check if the extracted types match the expected types
    expected_types = (int, str, bool)
    self.assertEqual(types, expected_types)

  def testNumerical(self) -> NoReturn:
    """Testing the TypeAlias"""
    self.assertIn(int, unStupid(Numerical))
    self.assertIn(float, unStupid(Numerical))
    self.assertIn(complex, unStupid(Numerical))
