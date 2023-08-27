"""WorkToy - Core - AbstractTask
This class contains precise control over specific tasks, their status and
their conclusion. Changes in the status trigger signals to listeners."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from abc import abstractmethod

from worktoy.core import StringAware, FLAG, Function, AbstractDescriptor
from worktoy.core import LIST

if TYPE_CHECKING:
  LIST = Iterable


class AbstractTask(StringAware):
  """WorkToy - Core - Task
  This class contains precise control over specific tasks, their status and
  their conclusion. Changes in the status trigger signals to listeners."""

  __not_started__ = FLAG[True,]
  __ready_to_start__ = FLAG[False,]
  __in_progress__ = FLAG[False,]
  __completed_with_errors__ = FLAG[False,]
  __successfully_completed__ = FLAG[False,]
  __listener_functions__ = LIST[()]
  __exception__ = AbstractDescriptor[None, Exception]

  def addListener(self, listener: Function, ) -> None:
    """Adds a listener."""
    self.__listener_functions__.append(listener)

  def notify(self, ) -> bool:
    """Calls each listener sending self."""
    for listener in self.__listener_functions__:
      listener(self)
    return True

  def run(self, *args, **kwargs) -> object:
    """This method causes the job to begin"""
    if not self.__ready_to_start__:
      raise TypeError
    self.__ready_to_start__ = False
    self.__not_started__ = False
    self.__in_progress__ = True
    if self.notify():
      try:
        self.job(*args, **kwargs)
        self.__successfully_completed__ = True
      except Exception as e:
        self.__completed_with_errors__ = True
        self.__exception__ = e
      self.__in_progress__ = False
      return self.notify()

  def __bool__(self, ) -> bool:
    """If a job is completed successfully, this returns True. Otherwise,
    False."""
    return True if self.__successfully_completed__ else False

  @abstractmethod
  def job(self, *args, **kwargs) -> object:
    """This abstract method defines the code to be run. Subclasses must
    implement this method."""
