"""
HookException wraps an exception raised by a namespace hook, so it is not
mistaken for the 'KeyError' by which a namespace tells the interpreter
that the class body never bound a name.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...mcls import AbstractNamespace
  from ...mcls.space_hooks import AbstractSpaceHook


class HookException(WorkToyException, Exception):
  """
  HookException wraps any exception raised by a namespace hook so it cannot
  be mistaken for the 'KeyError' that the interpreter reads as a control
  signal during '__getitem__': the class body never bound the name, which
  is then looked for among the global names. 'AbstractNamespace' catches
  an exception raised by the 'getItemPhase' of a hook and raises this one
  in its place, which keeps the original at 'initialException' and as its
  context:

      try:
        hook.getItemPhase(key, val)
      except Exception as exception:
        raise HookException(exception, self, key, val, hook)

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
    spec = """HookException raised from %s! Key: '%s', Value: %s, 
    Hook: '%s'! Initial exception: %s"""
    info = spec % (
      self.namespaceObject, self.itemKey, self._reprOf(self.errorValue),
      self.hookFunction, self._reprOf(self.initialException),
    )
    return textFmt(info)

  __repr__ = __str__
