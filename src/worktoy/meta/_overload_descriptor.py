"""Overload provides a class for overloading methods in a class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint

from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg
from worktoy.meta import Dispatcher, TypeSig, OverloadException

try:
  from typing import Any, Callable, TYPE_CHECKING
except ImportError:
  Any = object
  Callable = object
  TYPE_CHECKING = False

if TYPE_CHECKING:
  FuncList = list[tuple[TypeSig, Callable]]
else:
  FuncList = object


class Overload:
  """Overload provides a class for overloading methods in a class."""

  __function_name__ = None
  __function_owner__ = None
  __deferred_funcs__ = None
  __func_list__ = None
  __dispatcher_instance__ = None
  __class_method__ = None
  __static_method__ = None
  __instance_id__ = None

  def __init__(self, functionType: type = None) -> None:
    self.__instance_id__ = randint(0, 255)
    self.__static_method__ = False
    self.__class_method__ = False
    self.__func_list__ = []
    if functionType is not None:
      if functionType is staticmethod:
        self.__static_method__ = True
        self.__class_method__ = False
      elif functionType is classmethod:
        self.__static_method__ = False
        self.__class_method__ = True
      else:
        e = """Received invalid function type: '%s'! Only 'staticmethod'
        and 'classmethod' are allowed!"""
        raise TypeError(monoSpace(e % functionType))

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field. When this
    method is called the owner is created, so it is safe for the overload
    instance to create the Dispatcher instance. """
    clsName = '%sOverload' % name
    setattr(owner, clsName, self)
    self._setFunctionOwner(owner)
    self._setFunctionName(name)
    self.__dispatcher_instance__ = Dispatcher(self, self.getFuncList(), )

  def _setFunctionOwner(self, owner: type) -> None:
    """Setter-function for the function owner."""
    if self.__function_owner__ is not None:
      e = """The function owner of the '%s' instance is already set!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if not isinstance(owner, type):
      e = typeMsg('owner', owner, type)
      raise TypeError(e)
    self.__function_owner__ = owner
    self._compileFuncList()

  def _getFunctionOwner(self) -> type:
    """Getter-function for the function owner."""
    if self.__function_owner__ is None:
      e = """The function owner of the '%s' instance is accessed before 
      '__set_name__' has been called!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if isinstance(self.__function_owner__, type):
      return self.__function_owner__
    e = typeMsg('self.__function_owner__', self.__function_owner__, type)
    raise TypeError(e)

  def _setFunctionName(self, name: str, ) -> None:
    """Setter-function for the function name"""
    if self.__function_name__ is not None:
      e = """The function name of the '%s' instance is already set!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if not isinstance(name, str):
      e = typeMsg('name', name, str)
      raise TypeError(e)
    self.__function_name__ = name

  def _getFunctionName(self, ) -> str:
    """Getter-function for the function name"""
    if self.__function_name__ is None:
      e = """The function name of the '%s' instance is accessed before 
      '__set_name__' has been called!"""
      raise OverloadException(monoSpace(e % self.__class__.__name__))
    if isinstance(self.__function_name__, str):
      return self.__function_name__
    e = typeMsg('self.__function_name__', self.__function_name__, str)
    raise TypeError

  def __get__(self, instance: object, owner: type) -> Any:
    """Getter-function"""
    if instance is None:
      return self._classGetter(owner)
    return self._instanceGetter(instance)

  def _classGetter(self, owner: type) -> Any:
    """Getter-function for the class."""
    if self.__class_method__:
      self.__dispatcher_instance__.setBound(owner)
      return self.__dispatcher_instance__
    return self

  def _instanceGetter(self, instance: object) -> Any:
    """Getter-function for the instance. This returns the dispatcher. """
    self.__dispatcher_instance__.setBound(instance)
    return self.__dispatcher_instance__

  def getFuncList(self) -> FuncList:
    """Getter-function for the function dictionary."""
    return maybe(self.__func_list__, [])

  def overload(self, *types) -> Callable:
    """The overload function returns a callable that decorates a function
    with the signature. """

    def decorator(callMeMaybe: Callable) -> Callable:
      """The decorator function that adds the function to the function
      dictionary."""
      if isinstance(callMeMaybe, staticmethod):
        if not self.__static_method__:
          e = """The 'Overload' instance is not a static method!"""
          raise TypeError(e)
      if isinstance(callMeMaybe, classmethod):
        if not self.__class_method__:
          e = """The 'Overload' instance is not a class method!"""
          raise TypeError(e)
      existing = maybe(self.__deferred_funcs__, [])
      self.__deferred_funcs__ = [*existing, ((*types,), callMeMaybe)]
      return callMeMaybe

    return decorator

  def _compileFuncList(self, ) -> None:
    """Creates TypeSig instances for the function list. Please note that
    this method is meant to be invoked only after the owning class has
    been created. This permits the use of 'THIS' in overloaded functions.
    This allows overloading functions to instances of the same class. For
    example:

    from typing import Self
    from worktoy.meta import overload, THIS
    from worktoy.desc import AttriBox, THIS


    class Complex(BaseObject):
      #  Class representation of complex numbers
      RE = AttriBox[float]()
      IM = AttriBox[float]()

      #  Constructors omitted for brevity

      @overload(complex)
      def __add__(self, other: complex) -> Self:
        cls = self.__class__
        return cls(self.RE + other.real, self.IM + other.imag)

      @overload(float, float)
      def __add__(self, re_: float, im: float) -> Self:
        cls = self.__class__
        return cls(self.RE + re_, self.IM + im)

      @overload(THIS)  # When other is an instance of the same class
      def __add__(self, other: Self) -> Self:
        cls = self.__class__
        return cls(self.RE + other.RE, self.IM + other.IM)

      #  Implementations for the remaining mathematical operations are
      #  left as an exercise for the try-hard reader. """
    for (types, callMeMaybe) in self.__deferred_funcs__:
      finalTypes = []
      for type_ in types:
        if getattr(type_, '__THIS_ZEROTON__', None) is None:
          finalTypes.append(type_)
          continue
        finalTypes.append(self._getFunctionOwner())
      key = TypeSig(*finalTypes, )
      self.__func_list__.append((key, callMeMaybe))
