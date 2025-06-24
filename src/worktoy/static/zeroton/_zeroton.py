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

from typing import TYPE_CHECKING

from ...waitaminute import IllegalInstantiation, ZerotonCaseException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, TypeAlias, Never

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class Zeroton(type):
  """
  Zeroton is a metaclass that prevents instantiation of the class.
  """

  def __str__(cls) -> str:
    """
    Return the string representation of the Zeroton class. Each such
    class must provide a string representation by implementing the
    '__class_str__' method as a classmethod.
    """
    return getattr(cls, '__class_str__')()

  def __repr__(cls) -> str:
    """
    Return the string representation of the Zeroton class.
    """
    return """<Zeroton: %s>""" % cls.__name__

  def __instancecheck__(cls, obj: Any) -> bool:
    """
    Check if the object is an instance of the Zeroton class.
    """
    return getattr(cls, '__class_instancecheck__', lambda _: False)(obj)

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    """
    Prepare the class namespace for the Zeroton class.
    """
    if name != name.upper():
      raise ZerotonCaseException(name)
    return dict()

  def __new__(mcls, name: str, bases: Bases, space: Space) -> Self:
    """
    Confirms that the 'name' is all upper case and inserts a private
    variable with the name '__<name>__' (lower case) into the class
    namespace.
    """
    bases = (object,)
    key = '__%s__' % name.lower()
    space[key] = True
    return type.__new__(mcls, name, bases, space)

  def __init__(cls, *args: Any, **kwargs: Any) -> None:
    """
    Sets '__new__' and '__init__' methods to prevent instantiation of the
    Zeroton class.
    """

    def throw() -> Never:
      """Raise IllegalInstantiation exception."""
      raise IllegalInstantiation(cls)

    setattr(cls, '__new__', lambda *_: throw())
    setattr(cls, '__init__', lambda *_: throw())

  def __hash__(cls, ) -> Never:
    """
    Prevents the Zeroton class from being used as a hash key.
    """
    raise TypeError('Zeroton classes are not hashable')
