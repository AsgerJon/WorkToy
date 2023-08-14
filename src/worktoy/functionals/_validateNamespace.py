"""The nameSpaceValidator function takes any object as argument and
validates that the object can be used as the mapping object returned by
the __prepare__ method in a custom metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import MutableMapping as Map


def _isValidNamespace(obj: Map) -> int:
  """Check if the given object can be used as a namespace in a
  metaclass."""

  # Check for presence of methods
  requiredMethods = ['__getitem__', '__setitem__', '__contains__']
  if not all(hasattr(obj, method) for method in requiredMethods):
    return 1

  # Test functionality of methods
  try:
    testKey, testValue = "testKey", "testValue"

    # Test __setitem__
    obj[testKey] = testValue

    # Test __getitem__
    try:
      retrievedValue = obj[testKey]
      if retrievedValue != testValue:
        return 2
    except KeyError:
      # If KeyError is raised during retrieval, return False
      return 3

    # Test __contains__
    if testKey not in obj:
      return 4

    # Test for KeyError on unsupported key
    counter = 69420
    baseUnsupportedKey = lambda x: 'LMAO%d' % x
    while baseUnsupportedKey(counter) in obj:
      counter += 1
    _ = obj[baseUnsupportedKey(counter)]  # This should raise a KeyError

  except Exception as e:
    # This is expected for the unsupported key test
    if isinstance(e, KeyError):
      return 0
    return 5

  return 6


def validateNamespace(obj: Map) -> bool:
  """This function is the public interface. It calls _isValidNameSpace on
  the given object receiving an exitcode. If the exitcode is 0 the object
  is validated. Otherwise, the exitcode describes why the validation check
  failed."""

  exitcode = _isValidNamespace(obj)
  if not exitcode:
    return True
  from worktoy.waitaminute import InvalidNameSpaceError
  raise InvalidNameSpaceError(exitcode, obj)
