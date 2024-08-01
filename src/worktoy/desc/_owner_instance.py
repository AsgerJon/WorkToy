"""Owner is a Zeroton object indicating the owner of the descriptor
instance.  """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any, Never

from worktoy.meta import ZerotonMetaclass, BaseMetaclass
from worktoy.text import typeMsg


class _Field:
  """Primitive descriptor implementation"""

  __field_owner__ = None
  __field_name__ = None
  __getter_function__ = None
  __setter_function__ = None
  __deleter_function__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Called when the descriptor is assigned to a class attribute"""
    self.__field_owner__ = owner
    self.__field_name__ = name

  def __init__(self, *__, **_) -> None:
    pass

  def GET(self, callMeMaybe: Callable) -> Callable:
    """Decorator defining the getter function"""
    self.__getter_function__ = callMeMaybe
    return callMeMaybe

  def SET(self, callMeMaybe: Callable) -> Callable:
    """Decorator defining the setter function"""
    self.__setter_function__ = callMeMaybe
    return callMeMaybe

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """Decorator defining the deleter function"""
    self.__deleter_function__ = callMeMaybe
    return callMeMaybe

  def __get__(self, instance: object, owner: type) -> Any:
    """Getter-function for descriptor protocol"""
    if instance is None:
      return self
    if self.__getter_function__ is None:
      e = """The getter function has not been set!"""
      raise AttributeError(e)
    return self.__getter_function__(instance)

  def __set__(self, instance: object, value: object) -> None:
    """Setter-function for descriptor protocol"""
    if self.__setter_function__ is None:
      e = """The setter function has not been set!"""
      raise AttributeError(e)
    self.__setter_function__(instance, value)

  def __delete__(self, instance: object) -> None:
    """Deleter-function for descriptor protocol"""
    if self.__deleter_function__ is None:
      e = """This descriptor does not implement deleter functionality!"""
      raise TypeError(e)
    self.__deleter_function__(instance)


class WaitForIt(metaclass=BaseMetaclass):
  """Provides a dedicated class for wrapped callables created by SCOPE and
  TEST. This allows AttriBox to recognize that wrapped callables should
  run before finally being passed to the instance creation object"""

  __zeroton_argument__ = None  # THIS or SCOPE
  __replacement_argument__ = None
  __wrapped_callable__ = None

  zeroton = _Field()
  replacement = _Field()

  @zeroton.GET
  def __get_zeroton__(self) -> ZerotonMetaclass:
    """Getter-function for the zeroton argument attribute"""
    if self.__zeroton_argument__ is None:
      e = """The 'zeroton' attribute has not been set!"""
      raise AttributeError(e)
    if isinstance(self.__zeroton_argument__, ZerotonMetaclass):
      return self.__zeroton_argument__
    e = typeMsg('zeroton', self.__zeroton_argument__, ZerotonMetaclass)
    raise TypeError(e)

  @zeroton.SET
  def __set_zeroton__(self, zeroton: ZerotonMetaclass) -> None:
    """Setter-function for the zeroton argument attribute"""
    if self.__zeroton_argument__ is not None:
      e = """The 'zeroton' attribute has already been set!"""
      raise AttributeError(e)
    if not isinstance(zeroton, ZerotonMetaclass):
      e = typeMsg('zeroton', zeroton, ZerotonMetaclass)
      raise TypeError(e)
    self.__zeroton_argument__ = zeroton

  @replacement.GET
  def __get_replacement__(self, ) -> Any:
    """Getter-function for the replacement argument attribute"""
    if self.__replacement_argument__ is None:
      e = """The 'replacement' attribute has not been set!"""
      raise AttributeError(e)
    return self.__replacement_argument__

  @replacement.SET
  def __set_replacement__(self, replacement: Any) -> None:
    """Setter-function for the replacement argument attribute"""
    self.__replacement_argument__ = replacement

  @replacement.DELETE
  @zeroton.DELETE
  def _illegalDeleter(self, *_) -> Never:
    """Illegal accessor function"""
    e = """Attempted to delete protected attribute"""
    raise AttributeError(e)

  def __init__(self,
               zeroton: ZerotonMetaclass,
               callMeMaybe: Callable) -> None:
    self.__zeroton_argument__ = zeroton
    self.__wrapped_callable__ = callMeMaybe

  def __call__(self, *args, **kwargs) -> Any:
    """Calls the wrapped callable with SCOPE as the first argument
    followed by given positional and keyword arguments. """
    if not callable(self.__wrapped_callable__):
      e = typeMsg('wrapped callable', self.__wrapped_callable__, Callable)
      raise TypeError(e)
    wrap = self.__wrapped_callable__
    if self.__zeroton_argument__ is None:
      return wrap(*args, **kwargs)
    return wrap(self.replacement, *args, **kwargs)


class _MetaTHIS(ZerotonMetaclass):
  """Special metaclass for the 'THIS' object. """

  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    return False

  def __rshift__(cls, callMeMaybe: Callable) -> WaitForIt:
    """Returns a wrapper that calls the given function with the zeroton as
    the first argument. """
    if not callable(callMeMaybe):
      return NotImplemented
    return WaitForIt(cls, callMeMaybe)

  def __rlshift__(cls, callMeMaybe: Callable) -> WaitForIt:
    """Returns a wrapper that calls the given function with the zeroton as
    the last argument. """
    return cls >> callMeMaybe


class _MetaSELF(_MetaTHIS):
  """This metaclass makes the SELF object consider the 'THIS' object as an
  instance of itself."""

  @classmethod
  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    return False


class SELF(metaclass=_MetaSELF):
  """SELF is a Zeroton object indicating the descriptor instance itself."""


class _MetaBOX(_MetaTHIS):
  """This metaclass creates the zeroton object representing the descriptor
  class itself. """

  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    return True if instance is SELF else False


class BOX(metaclass=_MetaBOX):
  """BOX is a Zeroton object indicating the descriptor class itself."""


class THIS(metaclass=_MetaTHIS):
  """Instance is a Zeroton object indicating the instance owning the
  descriptor instance.  """


class _MetaSCOPE(_MetaTHIS):
  """This metaclass makes the SCOPE object consider the 'THIS' object as
  an instance of itself."""

  @classmethod
  def __instancecheck__(cls, instance: object) -> bool:
    """The __instancecheck__ method is called when the 'isinstance' function
    is called."""
    return True if instance is THIS else False


class SCOPE(metaclass=_MetaSCOPE):
  """SCOPE is a Zeroton object indicating the class owning the descriptor
  instance.  """
