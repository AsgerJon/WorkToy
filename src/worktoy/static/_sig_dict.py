"""SigDict provides a dictionary subclass using TypeSig objects as keys."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import TypeSig
from worktoy.text import typeMsg


class SigDict(dict):
  """SigDict provides a dictionary subclass using TypeSig objects as keys.

  The SigDict class is a dictionary subclass that uses TypeSig objects as
  keys. It is used to store dispatch functions and their associated
  signatures. The SigDict class provides methods for adding, removing, and
  retrieving dispatch functions based on their signatures.
  """

  __inner_dict__ = None

  def _createInnerDict(self, ) -> None:
    """Creator-function for the inner dictionary."""
    self.__inner_dict__ = dict()

  def _validateInnerDict(self, ) -> None:
    """Validator-function for the inner dictionary."""
    if self.__inner_dict__ is None:
      raise RuntimeError("""The inner dictionary is not initialized!""")
    if not isinstance(self.__inner_dict__, dict):
      raise TypeError(typeMsg('__inner_dict__', self.__inner_dict__, dict))
    for key, val in self.__inner_dict__.items():
      if not isinstance(key, TypeSig):
        raise TypeError(typeMsg('key', key, TypeSig))

  def _getInnerDict(self, **kwargs) -> dict:
    """Getter-function for the inner dictionary."""
    if self.__inner_dict__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createInnerDict()
      return self._getInnerDict(_recursion=True)
    return self.__inner_dict__

  def __getitem__(self, *args, **kwargs) -> object:
    """Get the value associated with the key."""
    if not kwargs.get('_root', False):
      if isinstance(args[0], tuple):
        return self.__getitem__(*args[0], _root=True)
    if isinstance(args[0], TypeSig):
      return self._getInnerDict()[args[0]]
