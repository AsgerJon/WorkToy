"""OverloadList is a subclass providing additional logic for invoking the
overloaded functions. Each instance should represent a list of functions
point to the same name. The class is callable on arguments that are then
passed on to the functions in it."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any

from worktoy import maybeType, searchKeys, maybe, CallMeMaybe, WorkMeta
from worktoy.sharperexceptions import ReadOnlyError


class OverloadList(list, WorkMeta):
  """Overloading procedure"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__()
    nameKwarg = searchKeys('name', 'title') @ str >> kwargs
    nameArg = maybeType(str, *args)
    nameDefault = None
    self._name = maybe(nameKwarg, nameArg, nameDefault)

  def __call__(self, *args, **kwargs) -> Any:
    """This overloading procedure operates under the following
    assumptions:
    There is an underlying function taking an unchanging number of
    parameters of known types and default values. Some combination of
    values or some default values may invoke errors, but those errors will
    never be regarded as argument errors. Every parameter answer to a
    particular keyword, such that all parameters might be invoked
    exclusively with keyword parameters. Likewise, every parameter must
    have a default value. Finally, this overloading procedure does not
    guarrantee that the result combination of arguments are appropriate.
    It is then left to the function itself to handle such cases and to
    provide relevant error messages.

    This leads to the following steps:
    1. Fill as many parameters with keyword arguments as possible.
    2. For each function, determine which arguments are covered by keyword
    arguments.
    3. For each function, collect positional arguments based on ordering
    and on types. Each function may only use each argument once.
    4. For each function, fill remaining parameters with default values.
    5. Whichever function requires the least default valued parameters are
    regarded as the best.

    In a future update, support will be added for weighted functions,
    such that more efficient functions are chosen over less efficient ones.
    """

  def _bestMatch(self, *args, **kwargs) -> CallMeMaybe:
    """Returns the best match between the functions"""

  def _getName(self) -> str:
    """Getter-function for the name"""
    return self._name

  def _setName(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('name')

  def _delName(self, ) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('name')

  name = property(_getName, _setName, _delName)
