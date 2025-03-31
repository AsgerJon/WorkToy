"""AbstractField provides an abstract base class for implementations of
the descriptor protocol that rely on the owning instances to provide the
accessor methods. These methods are identified by keys. One unique key
points to one unique getter method. As for setter and deleter methods,
multiple keys can be assigned to one field. This allows the owning class
to provide multiple setter and deleter methods for one field.

The following methods are provided for specifying keys to accessor methods:
  - setGetterKey: Assigns the getter key. Exactly one getter key should be
    assigned to each field.
  - appendSetterKey: Appends a setter key. Multiple setter keys or none at
    all may be assigned to one field.
  - appendDeleterKey: Appends a deleter key. Multiple deleter keys or none
    at all may be assigned to one field.

Please note that the above methods expects the key string pointing to the
accessor method as input. Thus, they cannot be used as decorators. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import maybe
from worktoy.text import typeMsg
from depr.meta import BaseMetaclass


class AbstractField(metaclass=BaseMetaclass):
  """AbstractField provides an abstract base class for implementations of
  the descriptor protocol that rely on the owning instances to provide the
  accessor methods. This is in contrast to implementations where the
  descriptor classes provide the accessor methods themselves. """

  #  Field name and first owner
  __field_name__ = None
  __base_owner__ = None
  #  Accessor method keys
  __getter_key__ = None
  __setter_keys__ = None
  __deleter_keys__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """This method sets the name of the descriptor. """
    self.__field_name__ = name
    self.__base_owner__ = owner

  def _getGetterKey(self, ) -> str:
    """This method returns the getter key. """
    if self.__getter_key__ is None:
      e = """The getter key has not been assigned!"""
      raise AttributeError(e)
    if isinstance(self.__getter_key__, str):
      return self.__getter_key__
    e = typeMsg('__getter_key__', self.__getter_key__, str)
    raise TypeError(e)

  def _getSetterKeys(self, ) -> list[str]:
    """This method returns the setter keys. """
    return maybe(self.__setter_keys__, [])

  def _getDeleterKeys(self, ) -> list[str]:
    """This method returns the deleter keys. """
    return maybe(self.__deleter_keys__, [])

  def setGetterKey(self, setterKey: str) -> None:
    """This method sets the getter key. """
    if self.__getter_key__ is not None:
      e = """The getter key has already been assigned!"""
      raise AttributeError(e)
    if not isinstance(setterKey, str):
      e = typeMsg('setterKey', setterKey, str)
      raise TypeError(e)
    self.__getter_key__ = setterKey

  def appendSetterKey(self, setterKey: str) -> None:
    """This method appends a setter key. """
    existing = self._getSetterKeys()
    self.__setter_keys__ = [*existing, setterKey]

  def appendDeleterKey(self, deleterKey: str) -> None:
    """This method appends a deleter key. """
    existing = self._getDeleterKeys()
    self.__deleter_keys__ = [*existing, deleterKey]

  def getFieldName(self) -> str:
    """This method returns the field name. """
    if self.__field_name__ is None:
      e = """The field name has not been set!"""
      raise AttributeError(e)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Why are we still here?"""

  def __init_subclass__(cls, **kwargs) -> None:
    """Just to suffer?"""
