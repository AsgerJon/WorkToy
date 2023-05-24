"""The typeGuardFunction compares function annotations against the
expected types"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import builtins
from typing import TypeAlias, Union, Any

from worktoy.core import CallMeMaybe, maybeTypes, searchKeys, empty, maybe

from worktoy.stringtools import stringList
from worktoy.waitaminute import typeGuard, n00bError, TypeGuardError

Ann: TypeAlias = tuple[Union[list[str], list[type]], type]


class TypeGuardFunction:
  """The typeGuardFunction compares function annotations against the
  expected types
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  @staticmethod
  def _isBuiltIn(func: CallMeMaybe) -> bool:
    """Checks if a function is builtin"""
    if not isinstance(func, type(abs)):
      return False
    if not getattr(func, '__module__', None) == builtins.__name__:
      return False
    return True

  @staticmethod
  def _removeFirst(data: list, item: Any) -> list:
    """Returns the list with the first encountered instance equal to item
    removed. """
    out = []
    taken = False
    for entry in data:
      if item != entry or taken:
        out.append(item)
      else:
        taken = True
    return out

  @staticmethod
  def _parseAnnotations(*args, **kwargs) -> list[type]:
    """Parses the arguments to obtain the expectation of the annotations"""
    returnKeys = stringList('return, return_, ')
    returnKwarg = searchKeys(*returnKeys) @ type >> kwargs
    types = maybeTypes(type, *args)
    for (key, val) in kwargs.items():
      if isinstance(val, type) and key not in returnKeys:
        types.append(val)
    returnArg = [*types, None]
    if empty(returnKwarg, returnArg):
      raise ValueError('Unable to parse required return type from '
                       'arguments!')
    return_ = maybe(returnKwarg, returnArg)
    posArgs = [type_ for type_ in types if type_ is not return_]
    return [*posArgs, return_]

  @staticmethod
  def _validateAnnotations(annotations_: dict[str, str]) -> dict:
    """Validates the annotations given and parses them to the same format as
    the function parsing the expected annotations"""
    return_ = None
    posTypes = {}
    for (key, val) in annotations_.items():
      if key in ['return', 'return_'] and return_ is None:
        return_ = val
      posTypes |= {key: val}
    if return_ is None:
      raise n00bError('No return hint found in annotations!')
    return posTypes

  @classmethod
  def _compareReturn(cls, annotations_: dict, *args, **kwargs) -> dict:
    """Compares the return values"""
    expect = cls._parseAnnotations(*args, **kwargs)
    actuality = cls._validateAnnotations(annotations_)
    expected = expect[-1].__name__
    actual = actuality['return']
    if actual not in ['Any', expected]:
      return dict(expected=expected, actual=actual)
    return {}

  @classmethod
  def _compareAnnotations(cls, annotations_: dict, *args, **kwargs) -> list:
    """Compares the annotations to the given arguments"""
    expect = cls._parseAnnotations(*args, **kwargs)[:-1]
    actuality = cls._validateAnnotations(annotations_)
    actual, actualTypes = {}, []
    for (k, v) in actuality.items():
      if k != 'return':
        actual |= {k: v}
        actualTypes.append(v)
    unsupported = []
    for entry in expect:
      if entry in actualTypes:
        actualTypes = cls._removeFirst(actualTypes, entry)
      elif 'Any' in actualTypes:
        actualTypes = cls._removeFirst(actualTypes, 'Any')
      else:
        unsupported.append(entry)
    return unsupported

  @classmethod
  def typeGuardFunction(cls, function: CallMeMaybe, *args,
                        **kwargs) -> CallMeMaybe:
    """Returns the function again, if its annotations matches what is given
    in the keyword arguments. Please note that function pass as long as they
    do not contradict the keyword arguments. Functions may take arguments
    not mentioned in the keyword arguments. But if a keyword argument is
    present, the function must annotate the key to the given value."""
    try:
      typeGuard(function, CallMeMaybe)
      if cls._isBuiltIn(function):
        return function
      annotations_ = getattr(function, '__annotations__', None)
      if not annotations_:
        raise n00bError('No annotations at all found in given function!')
      returnCompare = cls._compareReturn(annotations_, *args, **kwargs)
      posCompare = cls._compareAnnotations(annotations_, *args, **kwargs)
      if returnCompare or posCompare:
        raise TypeGuardError(
          *posCompare, return_=returnCompare, function_=function)
    except Exception as e:
      print('Given function encountered the following error:')
      raise e
