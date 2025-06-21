"""
AbstractDescriptor provides the base class for descriptors in the
'worktoy.attr' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import random as rand

from ..parse import maybe
from ..static import AbstractObject
from ..text import monoSpace
from ..waitaminute import MissingVariable

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any, Iterator, Callable
  from .accessor_hooks import AbstractDescriptorHook as Hook


class AbstractDescriptor(AbstractObject):
  """
  'AbstractDescriptor' inherits descriptor protocol implementation from
  'AbstractObject' and enhances it with a hook system surrounding each
  accessor method. These hooks are class specific and thus set with
  classmethod 'addAccessorHook'. The intended use is for hook classes to
  register themselves during '__set_name__'.

  The control flow dispatches hooks in order determined by their priority
  attribute from low to high. Tie-breakers are intentionally given fuzzy
  ordering to avoid undefined deterministic behaviour concealing errors.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
