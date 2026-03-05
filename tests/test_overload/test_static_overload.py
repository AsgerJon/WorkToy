"""
TestStaticOverload tests that the overload system correctly dispatches
'staticmethod' decorated methods.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Callable, Never


class Foo(BaseObject):
  """
  This method implements both regular and static overloads.
  """


class TestStaticOverload(OverloadTest):
  """
  TestStaticOverload tests that the overload system correctly dispatches
  'staticmethod' decorated methods.
  """
