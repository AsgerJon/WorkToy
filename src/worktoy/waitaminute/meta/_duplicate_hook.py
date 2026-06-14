"""
DuplicateHook is raised when a hook is registered at a name that already
holds a different hook.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt


class DuplicateHook(Exception):
  """
  DuplicateHook is raised when a hook is registered on a namespace at a
  name that already holds a different hook. Re-registering the same hook
  object is a no-op; only a genuine collision raises.

  Attributes
  ----------
  owner : type
    The namespace class the hook was being added to.
  name : str
    The field name both hooks claim.
  existingHook : object
    The hook already registered under that name.
  newHook : object
    The hook whose registration was rejected.
  """

  __slots__ = ('owner', 'name', 'existingHook', 'newHook')

  def __init__(self, *args, ) -> None:
    _owner, _name, _oldHook, _newHook = [*args, None, None, None, None][:4]
    self.owner = _owner
    self.name = _name
    self.existingHook = _oldHook
    self.newHook = _newHook
    Exception.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The class '%s' already has a hook registered 
    at name: '%s'! The existing hook is '%s', and the new hook is '%s'."""
    ownerName = self.owner.__name__
    oldHook = str(self.existingHook)
    newHook = str(self.newHook)
    info = infoSpec % (ownerName, self.name, oldHook, newHook)
    return textFmt(info)

  __repr__ = __str__
