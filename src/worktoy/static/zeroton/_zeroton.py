"""
Zeroton represents a novel concept similar to the idea of singleton
classes, but without any instantiation at all. The Zeroton object provides
a custom metaclass for these classes.

Zeroton classes should be used as immutable token objects that represent
particular situations. The primary use case at the initial point of
development is that of a placeholder allowing objects to be referenced
before they are created. For example, consider the following class with an
overloaded constructor:

class Foo:
  #  Using overloaded constructor

  @overload(Bar)  # Used when argument is of type 'Bar'
  def __init__(self, bar: Bar) -> None:
    ...

  @overload(THIS)  # Used when argument is also of type 'Foo'
  def __init__(self, other: Self) -> None:
    ...

During the creation of the 'Foo' class,


"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from . import ZeroSpace as ZSpace

from ...waitaminute import IllegalInstantiation, ZerotonCaseException
from ...waitaminute import MissingVariable, TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, TypeAlias, Never

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class Zeroton(type):
  """
  Zeroton is a metaclass that prevents instantiation of the class.
  """

  __class_str__ = None

  @staticmethod
  def _badNewFactory() -> Func:
    """
    Creates '__new__' replacement that prevents instantiation of the class.
    """

    def __new__(cls, *__, **_) -> Never:
      """
      Prevent instantiation of Zeroton class.
      """
      raise IllegalInstantiation(cls)

    if isinstance(__new__, Func):
      return __new__
    raise TypeException('__new__', __new__, Func)

  @staticmethod
  def _badInitFactory() -> Func:
    """
    Creates '__init__' replacement that prevents instantiation of the class.
    """

    def __init__(cls, *__, **_) -> Never:
      """Prevent instantiation of Zeroton class."""
      raise IllegalInstantiation(cls)

    if isinstance(__init__, Func):
      return __init__
    raise TypeException('__init__', __init__, Func)

  @staticmethod
  def _badHashFactory() -> Func:
    """
    Creates '__hash__' replacement that prevents instantiation of the class.
    """

    def __hash__(cls, ) -> Never:
      """
      Prevents the Zeroton class from being used as a hash key.
      """
      raise TypeError('Zeroton classes are not hashable')

    if isinstance(__hash__, Func):
      return __hash__
    raise TypeException('__hash__', __hash__, Func)

  def __str__(cls) -> str:
    """
    Return the string representation of the Zeroton class. Each such
    class must provide a string representation by implementing the
    '__class_str__' method as a classmethod.
    """
    try:
      func = cls.__class_str__
    except Exception as exception:
      raise MissingVariable('__class_str__', classmethod) from exception
    else:
      if isinstance(func, classmethod):
        out = func()
        if isinstance(out, str):
          if TYPE_CHECKING:
            assert isinstance(out, str)
          return out
        raise TypeException('__class_str__', func, str)
      raise TypeException('__class_str__', func, classmethod)
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        return 'pycharm, please!'
      else:
        pass

  def __instancecheck__(cls, obj: Any) -> bool:
    """
    Check if the object is an instance of the Zeroton class.
    """
    name = '__class_instancecheck__'
    if cls is obj:
      return True
    if not hasattr(cls, name):
      return False
    try:
      func = getattr(cls, name)
    except Exception as exception:
      raise MissingVariable(name, classmethod) from exception
    else:
      if isinstance(func, classmethod):
        return True if func(obj) else False
      raise TypeException(name, func, classmethod)
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        return not 'pycharm, please!'
      else:
        pass

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> ZSpace:
    """
    Prepare the class namespace for the Zeroton class.
    """
    if name != name.upper():
      raise ZerotonCaseException(name)
    return ZSpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Bases, space: Space) -> Self:
    """
    Confirms that the 'name' is all upper case and inserts a private
    variable with the name '__<name>__' (lower case) into the class
    namespace.
    """
    if name != name.upper():
      raise ZerotonCaseException(name)
    bases = (object,)
    key = '__%s__' % name.lower()
    space[key] = True
    return type.__new__(mcls, name, bases, space)

  def __init__(cls, *args: Any, **kwargs: Any) -> None:
    """
    Sets '__new__' and '__init__' methods to prevent instantiation of the
    Zeroton class.
    """
    type.__init__(cls, *args, **kwargs)  # no-op
    # As of 3.13, type.__init__ is a no-op but is included here for future
    # changes.
    badNames = ('__new__', '__init__', '__hash__')
    factories = (
        cls._badNewFactory,
        cls._badInitFactory,
        cls._badHashFactory
    )

    for name, factory in zip(badNames, factories):
      value = getattr(cls, name, None)
      if value is None:
        setattr(cls, name, factory)

    setattr(cls, '__new__', cls._badNewFactory())
    setattr(cls, '__init__', cls._badInitFactory())
    setattr(cls, '__hash__', cls._badHashFactory())

  def __call__(cls, *args, **kwargs) -> Never:
    """Prevent instantiation of Zeroton class."""
    if not getattr(cls, '__trust_me_bro__', False):
      raise IllegalInstantiation(cls)
    self = cls.__new__(*args, **kwargs)
    return self

  def __hash__(cls, ) -> Never:
    """
    Prevents the Zeroton class from being used as a hash key.
    """
    raise TypeError('Zeroton classes are not hashable')
