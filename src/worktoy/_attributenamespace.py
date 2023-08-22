"""WorkToy - AttributeNameSpace
This class supports a namespace that attempts to replace all values with
relevant attributes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractNameSpace, IntAttribute
from worktoy import FloatAttribute, StrAttribute, ListAttribute
from worktoy import DictAttribute, CallMeMaybe, MetaAttribute


class AttributeNameSpace(AbstractNameSpace):
  """WorkToy - AttributeNameSpace
  This class supports a namespace that attempts to replace all values with
  relevant attributes."""

  _implementedAttributes = [
    IntAttribute,
    FloatAttribute,
    StrAttribute,
    ListAttribute,
    DictAttribute,
    CallMeMaybe,
  ]

  @classmethod
  def _getAttributeMethods(cls) -> list[MetaAttribute]:
    """Getter-function for the list of supported Attribute Classes"""
    return cls._implementedAttributes

  @classmethod
  def _recognizeAttribute(cls, key: str, val: object) -> MetaAttribute:
    """Finds the attribute class that matches the value in the namespace."""
    for attribute in cls._getAttributeMethods():
      if isinstance(val, attribute):
        return attribute

  def __init__(self, *args, **kwargs) -> None:
    AbstractNameSpace.__init__(self, *args, **kwargs)

  def _explicitGetter(self, key: str) -> object:
    """Explicit Getter"""

  def _explicitSetter(self, key: str, val: object) -> None:
    """Explicit Setter"""

  def _explicitDeleter(self, key: str) -> None:
    """Explicit Deleter"""

  def _collectAttributes(self) -> None:
    """Analyzes the contents of the namespace and creates a dictionary
    containing key to attribute pairs. A name space may implement the
    __prepare__ method to return this method. Then the metaclass should
    attempt to use the key to attribute dictionary. """

  def getKeyAttributes(self, ) -> dict[str, MetaAttribute]:
    """Creates and returns the dictionary containing key to attribute."""
    out = {}
    for key in self:
      attribute = self._recognizeAttribute(key, self._contents[key])
      out |= {key: self.maybe(attribute, self._explicitGetter(key))}

    return out
