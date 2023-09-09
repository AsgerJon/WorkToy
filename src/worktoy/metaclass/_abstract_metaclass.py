"""WorkToy - MetaClass - AbstractMetaClass
This provides the abstract baseclass for metaclasses."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from icecream import ic

from worktoy.core import Bases
from worktoy.metaclass import MetaMetaClass

ic.configureOutput(includeContext=True)


class AbstractMetaClass(MetaMetaClass):
  """WorkToy - MetaClass - AbstractMetaClass
  This provides the abstract baseclass for metaclasses."""

  @classmethod
  @abstractmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Any:
    """
    The namespace for a newly created class, contains the key-value pairs
    given in the class body. By default, the builtin 'dict' provides the
    datastructure for the namespace. A custom metaclass may provide an
    alternative to this behaviour by reimplementing the __prepare__
    method.

    The default implementation deployed by 'type' and by custom
    metaclasses not implementing __prepare__ is to return an empty
    instance of 'dict'. A custom implementation can achieve enhanced
    functionality by prepopulating the instance of 'dict' or by returning
    an instance of a custom class instead of 'dict'.

    Introducing a custom class in the place of 'dict' provides a powerful
    tool for customizing the class creation process. However, the custom
    class must satisfy the following conditions:

    1.  The object transmitted to the super call in the __new__ method
        must be recognised as belonging to class 'dict' or as a subclass.
    2.  It must implement: __setitem__, __getitem__, __contains__
    3.  IMPORTANT: The __getitem__ implementation must raise a KeyError when
        receiving a key not matching any value. If the custom class does
        not raise a KeyError, HIGHLY UNDEFINED BEHAVIOUR will result.

    Developers implementing a custom class instead of dict for the
    namespace are encouraged to read the above conditions carefully.

    Below is a brief description of the class creation process.
    Parameters
    ----------
    mcls : type
      The metaclass creating the new class.
    cls : type
      The class being created.
    self : object
      Instance created by the newly created class.
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

    The code in the body is executed and each line provides an entry to
    the namespace with the left-hand side of the equal side indicating the
    key and the right-hand side the value. This key value pair is then
    placed in the object returned by the __prepare__ method. The namespace
    now populated with the data obtained from the class body becomes
    available to the __new__ method along with the name of the class and a
    tuple containing its baseclasses. Any keyword arguments set in the
    class constructor are also passed along to the __new__ method. (This
    does not include metaclass=MetaClass keyword argument though).

    Once the __new__ method completes, it returns the new class which is
    then passed to the __init__ function on the metaclass. Here, the new
    class is initialised.

    When the class has been initialised, it is also possible to augment the
    instance creation process. When a call is sent to the class,
    it generally creates a new instance of itself. The __call__ method on
    the metaclass defines this procedure, allowing for customization of
    instance creation as well.

    SUMMARY
    __prepare__
      Creates a namespace object by default a dictionary.
    The code in the class body is run line by line, providing entries into
    the namespace object.
    __new__
      Receives the namespace of the class along with name and bases and
      then returns the newly created class.
    __init__
      Receives the newly created class and initialises it.
    __call__
      Receives that class when an attempt is made to instantiate it."""

  #  NO! @classmethod
  def __new__(mcls, name, bases, nameSpace, **kwargs) -> type:
    """DO NOT place class method decorator on the __new__ method. The
    method is automatically a class method, and placing a redundant
    decorator will cause undefined behaviour.
    The baseclass implementation of __new__ collects arguments in the
    MetaClassParams body and passes them to the super call."""
    return super().__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls, name=None, bases=None, nameSpace=None, **kwargs) -> None:
    """The baseclass implementation uses the MetaClassParams instance to
    collect and pass the arguments to the super call."""
    MetaMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """This method refers to the call method on the class itself, meaning
    instance creation. Below is shown an approximation of the steps
    involved:

      newInstance = newClass(, *args, **kwargs)
      ...
    This line invokes the instance creation in the __call__ method:
      newInstance = NewClass.__new__(NewClass)
      NewClass.__init__(newInstance, *args, **kwargs)
      return newInstance

    Upon completion, the new instance is returned. Please note that this
    is a demonstration. The real implementation may not produce the same
    results."""
    return MetaMetaClass.__call__(cls, *args, **kwargs)
