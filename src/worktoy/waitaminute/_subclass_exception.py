"""SubclassException is a custom exception class raised to indicate that a
class was expected to be a subclass of another class, but was not. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations


class SubclassException(TypeError):
  """SubclassException is a custom exception class raised to indicate that a
  class was expected to be a subclass of another class, but was not. """

  __expected_parent__ = None
  __sub_cls__ = None

  def _getSubclsMRO(self, ) -> list[type]:
    """Return the MRO of the subclass. """
    return [cls for cls in self.__sub_cls__.__mro__]

  def __init__(self, expectedParent: type, subcls: type) -> None:
    """Initialize the exception with the expected and actual parent
    classes. """

    self.__expected_parent__ = expectedParent
    self.__sub_cls__ = subcls
    header = """Expected class '%s' to be a subclass of parent: '%s',  
    but does not appear in the MRO of the subclass:<br>%s"""
    body = '<tab><br>'.join([cls.__name__ for cls in self._getSubclsMRO()])
    msg = header % (subcls.__name__, expectedParent.__name__, body)
    TypeError.__init__(self, msg)
