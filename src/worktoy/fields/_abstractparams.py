"""WorkToy - Core - AbstractParams
Provides a body of argument parameters. This is practical for common,
but complicated arguments. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.core import DefaultClass
from worktoy.fields import AbstractDescriptor


class Parameter(AbstractDescriptor):
  """Extracts the bases."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    types = []
    self.keyNames = []
    for arg in args:
      if isinstance(arg, type):
        types.append(arg)
      if isinstance(arg, str):
        self.keyNames.append(arg)
    self.argTypes = (*types,)

  def explicitGetter(self,
                     obj: DefaultClass,
                     cls: DefaultClass) -> object:
    args, kwargs = obj.getArgs(), obj.getKwargs()
    kwAny = self.maybeKeys(*self.keyNames, **kwargs)
    kwargValues = [arg for arg in kwAny if isinstance(arg, self.argTypes)]
    ArgValues = [arg for arg in args if isinstance(arg, self.argTypes)]
    return self.maybe(*kwargValues, *ArgValues)

  def explicitSetter(self, *_) -> Never:
    """Read only"""
    raise TypeError

  def explicitDeleter(self, *_) -> Never:
    """Read only"""
    raise TypeError


class AbstractParams(AbstractDescriptor):
  """WorkToy - Core - Params
  Provides a body of argument parameters. This is practical for common,
  but complicated arguments. """

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
