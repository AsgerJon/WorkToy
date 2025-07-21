"""
OverloadTest provides a common base test case for all test classes in the
overload test module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from tests import BaseTest

from typing import TYPE_CHECKING

from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Type, TypeAlias, Any, Iterator, Tuple

  IntSample: TypeAlias = Iterator[tuple[int, ...]]


class OverloadTest(BaseTest):
  """
  OverloadTest provides a common base test case for all test classes in the
  overload test module.
  """
