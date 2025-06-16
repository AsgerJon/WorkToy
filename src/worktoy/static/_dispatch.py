"""The Dispatch class dispatches a function call to the appropriate
function based on the type of the first argument. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

from . import AbstractObject
from ..static import TypeSig
from ..text import typeMsg, monoSpace
from ..waitaminute import HashMismatch, CastMismatch, ResolveException, \
  VariableNotNone, TypeException, CascadeException
from ..waitaminute import DispatchException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable, TypeAlias, Never

  Types: TypeAlias = tuple[type, ...]
  Hashes: TypeAlias = list[int]
  HashMap: TypeAlias = dict[int, Callable]
  TypesMap: TypeAlias = dict[Types, Callable]
  CastMap: TypeAlias = dict[Types, Callable]
  CallMap: TypeAlias = dict[TypeSig, Callable]


class Dispatch(AbstractObject):
  """The Dispatch class dispatches a function call to the appropriate
  function based on the type of the first argument. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __call_map__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getTypeSigs(self) -> list[TypeSig]:
    """Get the type signatures."""
    return [*self.__call_map__.keys(), ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, callMap: CallMap) -> None:
    self.__call_map__ = callMap

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """Set the name of the function."""
    AbstractObject.__set_name__(self, owner, name, **kwargs)

    for sig, call in self.__call_map__.items():
      if not isinstance(sig, TypeSig):
        raise TypeError(typeMsg('sig', sig, TypeSig))
      if not callable(call):
        from worktoy.mcls import FunctionType
        raise TypeError(typeMsg('call', call, FunctionType))
      TypeSig.replaceTHIS(sig, owner)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _fastCall(self, *args: Any, **kwargs: Any) -> Any:
    """Fast call the function."""
    for sig, call in self.__call_map__.items():
      try:
        posArgs = sig.fast(*args)
      except HashMismatch:
        continue
      except TypeError as typeError:
        if 'required positional argument' in str(typeError):
          continue
        raise typeError
      except IndexError:
        continue
      except KeyError:
        continue
      except Exception as exception:
        print("""Unhandled exception in _fastCall: %s""" % str(exception))
        raise SystemExit
      if self.instance is not None:
        return call(self.instance, *posArgs, **kwargs)
      return call(*posArgs, **kwargs)
    raise DispatchException(self, *args)

  def _flexCall(self, *args: Any, **kwargs: Any) -> Any:
    """Flex call the function."""
    exceptions = []
    for sig, call in self.__call_map__.items():
      try:
        posArgs = sig.flex(*args)
      except Exception as exception:
        exceptions.append(exception)
        continue
      else:
        return self._fastCall(*posArgs, **kwargs)
    try:
      raise CascadeException(*exceptions)
    except CascadeException as cascadeException:
      raise DispatchException(self, *args) from cascadeException

  def _resolveArgs(self, *args) -> tuple:
    """Resolves tuples, lists and strings. """
    posArgs = []
    anyResolved = False
    for arg in args:
      if isinstance(arg, tuple):
        posArgs = [*posArgs, *arg]
        anyResolved = True
      elif isinstance(arg, list):
        posArgs = [*posArgs, *arg]
        anyResolved = True
      elif isinstance(arg, tuple):
        posArgs = [*posArgs, *arg]
        anyResolved = True
      elif isinstance(arg, str):
        evalArg = None
        try:
          evalArg = eval(arg)
        except NameError as nameError:
          evalArg = nameError
          posArgs = [*posArgs, arg]
        else:
          posArgs = [*posArgs, evalArg]
          anyResolved = True
        finally:
          pass
      else:
        posArgs.append(arg)
    if anyResolved:
      return (*posArgs,)
    raise ResolveException(self, args)

  def __call__(self, *args: Any, **kwargs: Any) -> Any:
    """Call the function."""
    try:
      return self._fastCall(*args, **kwargs)
    except DispatchException as fastException:
      pass
    try:
      return self._flexCall(*args, **kwargs)
    except DispatchException as flexException:
      pass
    try:
      posArgs = self._resolveArgs(*args)
    except ResolveException as resolveException:
      raise DispatchException(self, *args) from resolveException
    while True:
      try:
        posArgs = self._resolveArgs(*posArgs)
      except ResolveException:
        break
    return self.__call__(*posArgs, **kwargs)

  def __str__(self, ) -> str:
    """Get the string representation of the function."""
    sigStr = [str(sig) for sig in self.getTypeSigs()]
    info = """%s object supporting type signatures: \n%s"""
    sigLines = '<br><tab>'.join(sigStr)
    return monoSpace(info % (self.__field_name__, sigLines))

  def __repr__(self, ) -> str:
    """Get the string representation of the function."""
    return object.__repr__(self)
