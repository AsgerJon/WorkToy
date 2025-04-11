"""FastDispatch leverages strict typing to provide performant dispatching
of calls to overloaded functions. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe
from worktoy.static import TypeSig
from worktoy.text import typeMsg
from worktoy.waitaminute import MissingVariable, VariableNotNone, \
  SigKeyError, DispatchException


class FastDispatch:
  """FastDispatch leverages strict typing to provide performant dispatching
  of calls to overloaded functions. """

  __sig_funcs__ = None
  __frozen_sig_funcs__ = None

  def _createSigFuncs(self, ) -> None:
    """Create the signature functions. """
    if self.__sig_funcs__ is not None:
      raise VariableNotNone('__sig_funcs__')
    self.__sig_funcs__ = dict()

  def _validateSigFuncs(self, ) -> None:
    """Validate the signature functions. """
    if self.__sig_funcs__ is None:
      raise MissingVariable('__sig_funcs__', dict)
    if not isinstance(self.__sig_funcs__, dict):
      e = typeMsg('__sig_funcs__', self.__sig_funcs__, dict)
      raise TypeError(e)
    for sig, func in self.__sig_funcs__.items():
      if not isinstance(sig, TypeSig):
        e = typeMsg('sig', sig, TypeSig)
        raise TypeError(e)
      if not callable(func):
        from worktoy.mcls import CallMeMaybe
        e = typeMsg('func', func, CallMeMaybe)
        raise TypeError(e)

  def _getSigFuncs(self, **kwargs) -> dict:
    """Get the signature functions for the dispatch. """
    if self.__frozen_sig_funcs__ is not None:
      e = """The dispatch is already frozen!"""
      raise RuntimeError(e)
    try:
      self._validateSigFuncs()
    except MissingVariable:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createSigFuncs()
      return self._getSigFuncs(_recursion=True)
    return self.__sig_funcs__

  def _setSigFunc(self, sig: TypeSig, func: callable) -> None:
    """Set the signature functions for the dispatch. """
    if not isinstance(sig, TypeSig):
      e = typeMsg('sig', sig, TypeSig)
      raise TypeError(e)
    if not callable(func):
      from worktoy.mcls import CallMeMaybe
      e = typeMsg('func', func, CallMeMaybe)
      raise TypeError(e)
    existing = self._getSigFuncs()
    if sig in existing:
      raise SigKeyError(sig, func)
    self.__sig_funcs__ = {**existing, sig: func}

  def _freezeSigFuncs(self, ) -> None:
    """Freeze the signature functions. """
    if self.__frozen_sig_funcs__ is not None:
      raise VariableNotNone('__frozen_sig_funcs__')
    sigFuncs = self._getSigFuncs()
    self.__frozen_sig_funcs__ = dict()
    for sig, func in sigFuncs.items():
      self.__frozen_sig_funcs__[hash(sig)] = func

  def __call__(self, *args, **kwargs) -> object:
    """Call the function with the given arguments. """
    if self.__frozen_sig_funcs__ is None:
      raise MissingVariable('__frozen_sig_funcs__', dict)
    if not isinstance(self.__frozen_sig_funcs__, dict):
      e = typeMsg('__frozen_sig_funcs__', self.__frozen_sig_funcs__, dict)
      raise TypeError(e)
    argHash = hash((*[type(arg) for arg in args],))
    for key, func in self.__frozen_sig_funcs__.items():
      if argHash == key:
        return func(*args, **kwargs)
    raise DispatchException(self, *args)
