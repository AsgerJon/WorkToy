"""WorkToy - Core - MonitorTask
This subclass of AbstractTask monitors other functions and can be applied
specifically to classes and to exact methods. For example, to wrap the
__init__ method on OtherClass:

  @MonitorTask('__init__')
  class OtherClass:
    ### Augmented class ###
    def __init__(self, *args, **kwargs):
      ...

  otherInstance = OtherClass()
  ...
When the other instance is called the following happens, assuming standard
behaviour:
  1. The __new__ method on OtherClass is called
  2. Provided a new instance of OtherClass were returned by __new__,
  the __init__ method is called.
  3. The new instance is assigned to the name.
  4. (Optional) If the new instance is created in a class body,
  the __set_name__ method is called.
By decorating OtherClass with the MonitorTask('__init__'), the __init__
method is now wrapped by the job method in a newly created instance of
MonitorTask. Thus permitting:

  OtherClass.__init__.addListener(postInit)

The postInit method is now able to enrich the behaviour both before and
after the __init__ method.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import AbstractTask, Function, CLASS, STR, FLAG

if TYPE_CHECKING:
  STR = str


class MonitorTask(AbstractTask):
  """This subclass of AbstractTask monitors other functions and can be
  applied specifically to classes and to exact methods."""

  __class_ready__ = FLAG[False,]
  __monitored_class__ = CLASS[()]
  __method_name__ = STR[()]

  def __call__(self, *args, **kwargs) -> object:
    """The call method implements the typical behaviour that depends on
    the state. The first call sets the class or function of this instance.
    Subsequent calls invoke the underlying function or class as specified.
    """
    if not self.__class_ready__:
      self.__monitored_class__ = args[0]

  def _setClass(self, cls: type) -> None:
    """Setter-function for the underlying class"""
    self.__monitored_class__ = cls

  def _invokeFunction(self, *args, **kwargs) -> None:
    """Invokes the underlying function."""

    func = getattr(self.__monitored_class__, self.__method_name__, None)
    return func(*args, **kwargs)
