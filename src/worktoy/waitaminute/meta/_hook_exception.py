"""
HookException is raised from the AbstractNamespace class to wrap
exceptions raised by __getitem__ hooks. This is necessary to avoid
confusion with the expected KeyError exception in the metacall system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from ...mcls import AbstractNamespace
  from ...mcls.space_hooks import AbstractSpaceHook


class HookException(Exception):
  """
  HookException wraps any exception raised by a namespace hook so it cannot
  be mistaken for the 'KeyError' that the metacall system uses as a control
  signal during '__getitem__'. 'AbstractNamespace' catches a hook exception
  and re-raises it from this one:

      try:
        hook(self, key, val)
      except Exception as exception:
        raise HookException(exception, ...) from exception

  Attributes
  ----------
  initialException : Exception
    The original exception raised by the hook.
  namespaceObject : AbstractNamespace
    The namespace whose hook raised.
  itemKey : str
    The key being accessed when the hook raised.
  errorValue : object
    The value passed to the hook.
  hookFunction : AbstractSpaceHook
    The hook that raised.
  """

  __slots__ = (
    'initialException',
    'namespaceObject',
    'itemKey',
    'errorValue',
    'hookFunction',
  )

  def __init__(
      self,
      exception: Exception,
      namespace: AbstractNamespace,
      key: str,
      val: object,
      hook: AbstractSpaceHook,
  ) -> None:
    self.initialException = exception
    self.namespaceObject = namespace
    self.itemKey = key
    self.errorValue = val
    self.hookFunction = hook
    Exception.__init__(self, )

  def __str__(self) -> str:
    spec = """HookException raised from %s! Key: '%s', Value: '%s', 
    Hook: '%s'! Initial exception: %s"""
    cls = type(self).__name__
    info = spec % (
      self.namespaceObject, self.itemKey, self.errorValue,
      self.hookFunction, self.initialException,
    )
    return textFmt(info)

  __repr__ = __str__
