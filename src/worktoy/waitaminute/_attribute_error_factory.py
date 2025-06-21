"""
The 'attributeErrorFactory' instantiates 'AttributeError' with a message
that matches the built-in message if a given object does not have a given
attribute. This allows simulating the absense of an attribute. For example:

class Bar:  # secret descriptor!

  __fallback_value__ = 'lol'
  __field_name__ = None
  __field_owner__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> object:
    if instance is None:
      return self
    if hasattr(owner, '__trust_me_bro__'):
      pvtName = '__%s__' % self.__field_name__
      fallback = self.__fallback_value__
      return getattr(instance, pvtName, fallback)
    raise attributeErrorFactory(owner, self.__field_name__)


class Foo:
  __trust_me_bro__ = True
  bar = Bar()


class Sus:
  bar = Bar()


if __name__ == '__main__':
  foo = Foo()
  print(foo.bar)  # This will return the fallback value 'lol'
  sus = Sus()
  print(sus.bar)  # Raises AttributeError


The above attribute error will have the following message:
AttributeError: 'Sus' object has no attribute 'bar'
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class Breh(ValueError):
  """
  Breh is a custom exception that is raised when an attribute error is
  encountered, but the attribute error message does not match the built-in
  message.
  """

  posArgs = _Attribute()

  def __init__(self, *args: Any) -> None:
    self.posArgs = args
    ValueError.__init__(self, )

  def __str__(self) -> str:
    """
    Return a string representation of the Breh exception.
    """
    infoSpec = """Unable to resolve arguments: \n%s"""
    argStr = '<br><tab>'.join([str(arg) for arg in self.posArgs])
    info = infoSpec % argStr
    return monoSpace(info)

  __repr__ = __str__


def attributeErrorFactory(*args) -> AttributeError:
  """
  Factory function that creates an AttributeError with a message that
  matches the built-in message if a given object does not have a given
  attribute.
  """
  ownerName, fieldName = None, None
  for arg in args:
    if isinstance(arg, type) and ownerName is None:
      ownerName = arg.__name__
      continue
    if isinstance(arg, str):
      if ownerName is None:
        ownerName = arg
        continue
      if fieldName is None:
        fieldName = arg
        continue
  else:
    if ownerName is None or fieldName is None:
      raise Breh(*args)
  infoSpec = """AttributeError: '%s' object has no attribute '%s'"""
  info = infoSpec % (ownerName, fieldName)
  return AttributeError(info)  # type: ignore[return-value]
