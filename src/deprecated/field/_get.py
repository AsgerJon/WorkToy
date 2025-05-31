"""
GET provides the decorator used by 'worktoy.attr.field.Field' to designate
the getter method in the class body.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ...parse import maybe
from ...static import AbstractObject
from ...static.zeroton import THIS, OWNER, DESC
from ...waitaminute import MissingVariable, TypeException
from ...waitaminute import SubclassException
from ...waitaminute import ReadOnlyError, ProtectedError

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, TypeAlias, Never


class GET(AbstractObject):
  """Creates a deferred function that is called when the __get__ is first
  called. """
 