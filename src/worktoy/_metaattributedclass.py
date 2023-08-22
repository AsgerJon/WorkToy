"""WorkToy - MetaAttributedClass
This class is the metaclass used to generate attribute only classes. That
is, classes where each entry in the class body is replaced by the
appropriate attribute class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractMetaType, AttributeNameSpace


class MetaAttributedClass(AbstractMetaType):
  """WorkToy - MetaAttributedClass
  This class is the metaclass used to generate attribute only classes. That
  is, classes where each entry in the class body is replaced by the
  appropriate attribute class."""

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple,
                  **kwargs) -> AttributeNameSpace:
    """The AttributeNameSpace returned by the __prepare__ method will
    arrive in the __new__ with values populated as normal. Then __new__
    should access the 'getKeyAttributes' on it. This will return a new
    dictionary containing attributes instead of basic types. """
    return AttributeNameSpace()

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: AttributeNameSpace,
              **kwargs) -> AbstractMetaType:
    """"""
