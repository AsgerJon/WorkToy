"""Documentation - maybe
The objective of the 'maybe' function is to implement the null-coalescence
behaviour in a None-aware way. It returns the first non-None argument
passed to it, or None if all arguments are None.

Inputs:
The function takes in any number of arguments of any type.

Flow:
The function iterates through all the arguments passed to it and checks if
each argument is not None. If it finds a non-None argument, it immediately
returns that argument. If it iterates through all the arguments and finds
that all of them are None, it returns None.

Outputs:
The function returns either the first non-None argument passed to it or
None if all arguments are None.

Additional aspects:
The function is None-aware, meaning it can handle None values as
arguments. The function is also licensed under the MIT Licence and was
created by Asger Jon Vistisen in 2023.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from worktoy.worktype import CallMeMaybe


def maybe(*args) -> object:
  """The None-aware 'maybe' implements the null-coalescence behaviour.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  for arg in args:
    if arg is not None:
      return arg


def onlyIf(func: CallMeMaybe, *args) -> list[object, ...]:
  """Returns a list of the positional arguments that satisfy the given
  function """
  return [arg for arg in args if func(arg)]


def maybeFirstIf(func: CallMeMaybe, *args, ) -> object:
  """Returns the first positional argument """
  return onlyIf(func, *args)[0]


def maybeAllIf(func: CallMeMaybe, *args, ) -> list[object]:
  """Returns the first positional argument """
  return onlyIf(func, *args)


def maybeType(type_: type, *args) -> object:
  """Getter-function for the first arg in the positional arguments that
  has the given type"""
  func = lambda item: True if isinstance(item, type_) else False
  return maybeFirstIf(func, *args)


def maybeTypes(type_: type, *args) -> list[object]:
  """Getter-function for each arg in the positional arguments that has the
  given type"""
  func = lambda item: True if isinstance(item, type_) else False
  return maybeAllIf(func, *args)


def empty(*args) -> bool:
  """Returns True unless one of the positional arguments (if any) is
  different from None. If no positional arguments are present this method
  returns True also"""
  func = lambda x: True if x is None else False
  return all(maybeAllIf(func, (*args, None)))


def some(*args) -> bool:
  """Returns True if at least one of the positional arguments is different
  from None. If no positional argument is present, this function returns
  False. """
  func = lambda x: False if x is None else True
  return any(maybeAllIf(func, (*args, None)))


def plenty(*args) -> bool:
  """Returns True if every positional argument is different from None.
  Please note that plenty also returns True if no positional arguments are
  found. Thus: empty() == plenty(), but some() is False."""
