"""
NameHook filters named used in the namespace system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...waitaminute import QuestionableSyntax

from . import AbstractHook

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias

  NearMiss: TypeAlias = tuple[str, str]


class NameHook(AbstractHook):
  """
  NameHook intercepts names added to the namespace and filters out
  "near-miss" identifiers that resemble critical Python dunder methods.
  These mistakes often go unnoticed, leading to subtle bugs or broken
  protocol support.

  This hook raises a QuestionableSyntax exception when such names are
  detected during assignment in the namespace.

  ## Purpose

  Many magic methods in Python have specific names that must be spelled
  exactly. If a user misspells one by inserting or omitting underscores,
  the name is silently ignored by Python and treated as an ordinary
  attribute — sometimes shadowing a builtin or behaving unexpectedly.

  ## Near-miss Examples
  ___________________________________________________________________________
  | Intended Name  | Mistyped Name | Notes                                 |
  |----------------|---------------|---------------------------------------|
  | `__set_name__` | `__setname__` | Misses descriptor registration        |
  | `__getitem__`  | `__get_item__`| Breaks item access in dict-like APIs  |
  | `__setitem__`  | `__set_item__`| Same as above                         |
  | `__delitem__`  | `__del_item__`| Silent failure of delete protocol     |
  | `__delete__`   | `__del__`     | High risk: __del__ ties to GC hooks   |
  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
  These errors can be especially difficult to diagnose, as they usually
  do not raise any errors directly — instead, they silently fail to
  participate in expected behaviors or override builtin methods.

  ## Usage
  To use NameHook, simply declare it in your namespace class:

  class Space(AbstractNamespace):  # Must inherit from AbstractNamespace
    #  Custom namespace class inheriting from AbstractNamespace
    nameHook = NameHook()  # Register the hook
"""

  @classmethod
  def _getNearMisses(cls) -> list[NearMiss]:
    """
    Get the near-miss names.
    """
    return [
        ('__set_name__', '__setname__'),  # NOQA, miss-spelled name
        ('__getitem__', '__get_item__'),
        ('__setitem__', '__set_item__'),
        ('__delitem__', '__del_item__'),
        ('__delete__', '__del__'),
    ]

  @classmethod
  def _validateName(cls, name: str) -> bool:
    """
    Compares the name to list of potential near-miss names. If the name
    is a near-miss, a QuestionableSyntax exception is raised.
    """
    nearMisses = cls._getNearMisses()
    for nearMiss in nearMisses:
      if name == nearMiss[1]:
        raise QuestionableSyntax(*nearMiss, )
    return False

  def setItemHook(self, key: str, value: Any, oldValue: Any) -> bool:
    """
    Hook for setItem. This is called before the __setitem__ method of
    the namespace object is called. The default implementation does nothing
    and returns False.
    """
    return self._validateName(key)
