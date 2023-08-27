"""WorkToy - Symbolic - AbstractSym
This class provides the functions used by the Symbolic classes. These are
methods generally shared by classes by virtue of being Symbolic."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.core import StringAware


class AbstractSym(StringAware):
  """WorkToy - Symbolic - AbstractSym
  This class provides the functions used by the Symbolic classes. These are
  methods generally shared by classes by virtue of being Symbolic."""

  @classmethod
  @abstractmethod
  def getClassName(cls) -> str:
    """Getter-function for the class name."""

  @abstractmethod
  def getInstanceName(self) -> str:
    """Getter-function for the instance name."""

  def __str__(self) -> str:
    return '%s - %s' % (self.__class__.__name__, self.__name__)

  def __repr__(self) -> str:
    return '%s.%s' % (self.__class__.__name__, self.__name__)

  def __eq__(self, other: AbstractSym) -> bool:
    return True if self is other else False

  def __ne__(self, other: AbstractSym) -> bool:
    return True if self is not other else False
