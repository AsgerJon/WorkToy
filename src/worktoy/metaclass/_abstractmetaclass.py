"""WorkToy - MetaClass - AbstractMetaClass
This provides the abstract baseclass for metaclasses."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.metaclass import MetaMetaClass


class AbstractMetaClass(MetaMetaClass):
  """WorkToy - MetaClass - AbstractMetaClass
  This provides the abstract baseclass for metaclasses."""

  @classmethod
  @abstractmethod
  def __prepare__(mcls, name: str, bases: tuple[type], **kwargs) -> dict:
    """Sub-metaclasses should implement the prepare method to customise
    how to metaclass receives the class body. If the default behaviour is
    sufficient, this method should return an instance of dict.
    Alternatively, an instance of a custom class may be used under the
    following conditions:

    1.  It must implement: __setitem__, __getitem__, __contains__
    2.  The __getitem__ implementation must raise a KeyError when
        receiving a key not matching any value. If the custom class does
        not raise a KeyError, highly undefined behaviour will result.
    3.  The object transmitted to the super call in the __new__ method
        must be recognised as belonging to class 'dict' or a subclass.

    IMPORTANT: Developers implementing a custom class instead of dict for
    the namespace are encouraged to read the above conditions carefully.

    Below is a brief description of the class creation process, beginning
    with definitions:
      - Class body
      - NameSpace
      - Bases
    Parameters
    ----------
    mcls : type
        The metaclass, not the class being created, but the metaclass
        creating it.
    :cls:  The class being created.
    :self: Instance created by the newly created class.
    ----------

    The class body is the code creating the class. For example,

    class NewClass(metaclass=MetaClass):
    # Start of class body
      _classVariable = None

      @classmethod
      def getClassVariable(cls) -> object:
        return cls._classVariable

      def __init__(self, *args, **kwargs) -> None:
        self._instanceVariable = math.cos(pi/6)

      def instanceMethod(self) -> object:
        self
    # End of class body



    """

  #  NO! @classmethod
  def __new__(mcls, *args, **kwargs) -> type:
    """DO NOT place class method decorator on the __new__ method. The
    method is automatically a class method, and placing a redundant
    decorator will cause undefined behaviour.

    The baseclass implementation of __new__ collects arguments in the
    MetaClassParams body and passes them to the super call.

    """
    mcls.params.setAllArgs(*args, **kwargs)
    name = mcls.params.name
    bases = mcls.params.bases
    nameSpace = mcls.params.nameSpace
    return type.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls, *args, **kwargs) -> None:
    """The baseclass implementation uses the MetaClassParams instance to
    collect and pass the arguments to the super call."""
    cls.params.setAllArgs(*args, **kwargs)
    name = cls.params.name
    bases = cls.params.bases
    nameSpace = cls.params.nameSpace
    type.__init__(cls, name, bases, nameSpace, **kwargs)
