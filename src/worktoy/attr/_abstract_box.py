"""
AbstractBox provides a descriptor with lazy instantiation of a particular
class instantiating only when 'AbstractBox.__get__' receives an instance
(not 'None'). This conserves resources and streamlines object creation.

Qt applications such as developed by Pyside6, require the
'QCoreApplication' to be running before any 'QObject' may be instantiated.
Since Pyside6 is effectively a C++ library, failure to adhere to this
requirement leads to segmentation related errors occurring separate from
the Python interpreter. In other words, it leads to highly undefined
behaviour. By using 'AbstractBox' descriptors when developing in Pyside6,
this design patterns becomes much easier to implement and maintain as the
descriptor itself defers instantiation.

AbstractBox descriptor implements only 'get' functionality, which
looks for an instance of the wrapped class at the private name of
the descriptor in the namespace of the current instance. If no such is
found, it creates one and recursively calls the instance get again. This
attempt passes positional and keyword arguments received by the descriptor
constructor and passes them on to the wrapped class constructor.

The 'set' functionality may be implemented in multiple different ways,
unlike the 'get' functionality which AbstractBox does provide. For 'set'
and 'delete' functionality, AbstractBox leaves it to subclasses to change
the default behaviour of simply raising 'ReadOnlyError' or
'ProtectedError' respectively.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static.zeroton import DELETED
from ..waitaminute import MissingVariable, TypeException, \
  attributeErrorFactory
from . import Field

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias

  Types: TypeAlias = tuple[type, ...]


class AbstractBox(Field):
  """AttriBox provides a descriptor with lazy instantiation of the
  underlying object. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __wrapped__ = None  # __get__ returns an instance of this class

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getWrappedClass(self) -> type:
    """
    Getter-function for the wrapped class.
    """
    if self.__wrapped__ is None:
      raise MissingVariable('__wrapped__', type)
    if isinstance(self.__wrapped__, type):
      return self.__wrapped__
    name, value = '__wrapped__', self.__wrapped__
    raise TypeException(name, value, type)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setWrappedClass(self, wrapped: type) -> None:
    """
    Setter-function for the wrapped class.
    """
    if self.__wrapped__ is not None:
      raise MissingVariable('__wrapped__', type)
    if not isinstance(wrapped, type):
      name, value = '__wrapped__', wrapped
      raise TypeException(name, value, type)
    self.__wrapped__ = wrapped
    return

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createdWrappedObject(self, ) -> Any:  # of __wrapped__ type
    """
    Creator-function for the object of __wrapped__ type.
    """
    args = self._getPositionalArgs()
    kwargs = self._getKeywordArgs()
    wrapCls = self.getWrappedClass()
    return wrapCls(*args, **kwargs)

  def __instance_get__(self, **kwargs) -> Any:
    """
    Instance getter-function retrieves a wrapped object already at the
    current instance. If no wrapped object is found, an attempt is made to
    create and set one after which __'instance_get__' is called again,
    but with the '_recursion' keyword argument set to 'True'. If again, no
    wrapped object is found, the function raises a plain RecursionError.
    """
    pvtName = self._getPrivateName()
    out = getattr(self.instance, pvtName, None)
    if out is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      out = self._createdWrappedObject()
      setattr(self.instance, pvtName, out)
      return self.__instance_get__(_recursion=True, )
    if out is DELETED:
      raise attributeErrorFactory(self.owner, self.__field_name__)

    wrapped = self.getWrappedClass()
    if isinstance(out, wrapped):
      return out
    name, value = pvtName, out
    raise TypeException(name, value, wrapped)
