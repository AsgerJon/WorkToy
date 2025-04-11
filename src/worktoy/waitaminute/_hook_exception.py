"""HookException is raised from the AbstractNamespace class to wrap
exceptions raised by __getitem__ hooks. This is necessary to avoid
confusion with the expected KeyError exception in the metacall system."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.mcls import AbstractNamespace
  from worktoy.mcls.hooks import AbstractHook


class HookException(Exception):
  """This custom exception allows get item hooks to interrupt calls to
  __getitem__. Because the metacall system requires the __getitem__ to
  specifically raise a KeyError in certain situations, an exception raised
  by a hook might be confused for the KeyError. Instead,
  the AbstractNamespace class will catch exceptions raised by hooks and
  raise them from this exception:
  For example:

  try:
    hook(self, key, val)
  except Exception as exception:
    raise _HookException(exception) from exception

  """

  __initial_exception__ = None
  __namespace_object__ = None
  __key_str__ = None
  __val_or_error__ = None
  __hook_function__ = None

  def __init__(
      self,
      exception: Exception,
      namespace: AbstractNamespace,
      key: str,
      val: object,
      hook: AbstractHook,
  ) -> None:
    self.__initial_exception__ = exception
    self.__namespace_object__ = namespace
    self.__key_str__ = key
    self.__val_or_error__ = val
    self.__hook_function__ = hook
    Exception.__init__(self, str(exception))
