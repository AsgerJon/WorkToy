"""The Dispatch class dispatches a function call to the appropriate
function based on the type of the first argument. """
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
  from typing import Any, Callable

from worktoy.text import typeMsg
from worktoy.waitaminute import MissingVariable, VariableNotNone, SigMismatch
from worktoy.waitaminute import DispatchException

from worktoy.static import OverloadedFunction as OverFunc


class _Name:
  """Private descriptor allowing attribute access to the name of the
  wrapped function. """

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the name of the function."""
    if instance is None:
      return self
    name = getattr(instance, '__func_name__', None)
    if name is None:
      info = """'__func_name__' attribute is not set!"""
      raise RuntimeError(info)
    if isinstance(name, str):
      return name
    e = typeMsg('__func_name__', name, str)
    raise TypeError(e)


class _HasFallback:
  """Private descriptor indicating the presence of a fallback function. """

  __attr_name__ = '__fallback_func__'

  def _getAttrName(self, ) -> str:
    """Getter-function for the attribute name."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: object) -> Any:
    """Get the state of the fallback flag."""
    if instance is None:
      return self
    attrName = self._getAttrName()
    state = getattr(instance, attrName, None)
    return False if state is None else True


class _HasFlex:
  """Private descriptor indicating the presence of a fallback function. """

  __attr_name__ = '__flex_funcs__'

  def _getAttrName(self, ) -> str:
    """Getter-function for the attribute name."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: object) -> Any:
    """Get the state of the fallback flag."""
    if instance is None:
      return self
    attrName = self._getAttrName()
    flexFuncs = getattr(instance, attrName, )
    if flexFuncs is None:
      return False
    if isinstance(flexFuncs, dict):
      return True if flexFuncs else False
    e = typeMsg('__flex_funcs__', flexFuncs, dict)
    raise TypeError(e)


class Dispatch:
  """The Dispatch class dispatches a function call to the appropriate
  function based on the type of the first argument. """

  __func_name__ = None
  __sig_funcs__ = None
  __flex_funcs__ = None
  __fallback_func__ = None

  __field_owner__ = None  # The base class that owns this dispatch
  __field_name__ = None  # Should be same as function name

  __bound_instance__ = None

  hasFallback = _HasFallback()
  hasFlex = _HasFlex()
  __name__ = _Name()

  def __set_name__(self, owner: type, name: str) -> None:
    """Invoked when the owning class is created. """
    funcName = self.__name__
    if funcName != name:
      e = """Dispatch name '%s' does not match function name '%s'!"""
      raise RuntimeError(e % (funcName, name))
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the bound instance."""
    if instance is not None:
      self.__bound_instance__ = instance
    return self

  def __init__(self, *args) -> None:
    """Initialize the Dispatch object."""
    overFuncs = []
    for arg in args:
      if isinstance(arg, OverFunc):
        overFuncs.append(arg)
        continue
      e = typeMsg('overFunc', arg, OverFunc)
      raise TypeError(e)
    sigFuncs = {}
    flexFuncs = {}
    funcName = None
    for overFunc in overFuncs:
      func = overFunc.getFunc()
      if funcName is None:
        funcName = overFunc.__name__
      else:
        if funcName != overFunc.__name__:
          e = """Functions with different names found in same dispatch:
          '%s' != '%s'!""" % (funcName, overFunc.__name__)
          raise RuntimeError(e)
      if overFunc.isFallback:
        if self.__fallback_func__ is not None:
          raise VariableNotNone('__fallback_func__')
        self.__fallback_func__ = func
      else:
        for sig in overFunc.getTypeSigs():
          if overFunc.allowFlex:
            flexFuncs[sig] = func
          sigFuncs[sig] = func
    self.__sig_funcs__ = sigFuncs
    self.__flex_funcs__ = flexFuncs
    self.__func_name__ = funcName

  def _boundFast(self, *args, **kwargs) -> Any:
    """Attempts to fast call the function. """
    instance = self.__bound_instance__
    for sig, func in self.__sig_funcs__.items():
      try:
        return func(instance, *sig.fast(*args), **kwargs)
      except SigMismatch:
        continue
    raise DispatchException(self, *args, )

  def _freeFast(self, *args, **kwargs) -> Any:
    """Attempts to fast call the function. """
    for sig, func in self.__sig_funcs__.items():
      try:
        return func(*sig.fast(*args), **kwargs)
      except SigMismatch:
        continue

  def _boundCast(self, *args, **kwargs) -> Any:
    """Attempts to cast call the function. """
    instance = self.__bound_instance__
    for sig, func in self.__sig_funcs__.items():
      try:
        return func(instance, *sig.cast(*args), **kwargs)
      except SigMismatch:
        continue
    raise DispatchException(self, *args, )

  def _freeCast(self, *args, **kwargs) -> Any:
    """Attempts to cast call the function. """
    for sig, func in self.__sig_funcs__.items():
      try:
        return func(*sig.cast(*args), **kwargs)
      except SigMismatch:
        continue

  def _boundFlex(self, *args, **kwargs) -> Any:
    """Attempts to flex call the function. """
    instance = self.__bound_instance__
    for sig, func in self.__flex_funcs__.items():
      try:
        return func(instance, *sig.flex(*args), **kwargs)
      except SigMismatch:
        continue
      except TypeError as typeError:
        if 'required positional' in str(typeError):
          continue
    raise DispatchException(self, *args, )

  def _freeFlex(self, *args, **kwargs) -> Any:
    """Attempts to flex call the function. """
    for sig, func in self.__flex_funcs__.items():
      try:
        return func(*sig.flex(*args), **kwargs)
      except SigMismatch:
        continue
      except TypeError as typeError:
        if 'required positional' in str(typeError):
          continue
    raise DispatchException(self, *args, )

  def _boundBack(self, *args, **kwargs) -> Any:
    """Calls fallback function with bound instance. """
    if self.__fallback_func__ is None:
      raise MissingVariable('__fallback_func__', Callable)
    instance = self.__bound_instance__
    if instance is None:
      raise VariableNotNone('__bound_instance__')
    if not callable(self.__fallback_func__):
      e = typeMsg('__fallback_func__', self.__fallback_func__, Callable)
      raise TypeError(e)
    try:
      return self.__fallback_func__(instance, *args, **kwargs)
    except Exception as exception:
      raise DispatchException(self, *args) from exception

  def _freeBack(self, *args, **kwargs) -> Any:
    """Calls fallback function without bound instance. """
    if self.__fallback_func__ is None:
      raise MissingVariable('__fallback_func__', Callable)
    if not callable(self.__fallback_func__):
      e = typeMsg('__fallback_func__', self.__fallback_func__, Callable)
      raise TypeError(e)
    try:
      return self.__fallback_func__(*args, **kwargs)
    except Exception as exception:
      raise DispatchException(self, *args) from exception

  def __call__(self, *args, **kwargs) -> Any:
    """Calls the function with the given arguments."""
    if self.__bound_instance__ is None:
      try:
        return self._freeFast(*args, **kwargs)
      except DispatchException:
        try:
          return self._freeCast(*args, **kwargs)
        except DispatchException:
          try:
            return self._freeFlex(*args, **kwargs)
          except DispatchException as dispatchException:
            if self.__fallback_func__ is None:
              raise dispatchException
            try:
              return self._freeBack(*args, **kwargs)
            except Exception as exception:
              raise DispatchException(self, *args) from exception
    try:
      return self._boundFast(*args, **kwargs)
    except DispatchException:
      try:
        return self._boundCast(*args, **kwargs)
      except DispatchException:
        try:
          return self._boundFlex(*args, **kwargs)
        except DispatchException as dispatchException:
          if self.__fallback_func__ is None:
            raise dispatchException
          try:
            return self._boundBack(*args, **kwargs)
          except Exception as exception:
            raise DispatchException(self, *args) from exception
