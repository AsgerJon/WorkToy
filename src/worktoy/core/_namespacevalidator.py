"""The nameSpaceValidator function ensures that an object returned from
the __prepare__ method on a metaclass implements the necessary methods and
raises the correct errors:

The namespace object must implement:
  __getitem__, __setitem__ and __contains__

The namespace object must support setting and getting.

If the namespace receives an unrecognized key, it must raise a KeyError.
This one is important, as the resulting unexpected behaviour in no way
suggests a problem with the namespace class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from random import choices, randint
import string
from typing import Optional, TYPE_CHECKING, cast, Union, Self, Type, Callable

from icecream import ic

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


def _randomWord(*args) -> str:
  """Generates a random word of length n"""
  vals = [8, 12]
  for (i, arg) in enumerate(args):
    if isinstance(arg, int):
      vals[i] = arg
  n = randint(8, 12)

  bases = [string.ascii_lowercase,
           string.ascii_uppercase,
           string.digits]
  chars = [char for char in ''.join(bases)]
  return ''.join(choices(chars, k=n))


def _randomWords(*args) -> list[str]:
  """Generates a list of random words"""
  intArgs = [arg for arg in args if isinstance(arg, int)]
  while len(intArgs) < 3:
    intArgs.append(8)
  N, a, b = intArgs[:3]
  return [_randomWord(a, b) for _ in range(N)]


def _collectError(cls: type) -> Optional[Exception]:
  """Collects the exception"""
  return getattr(cls, '__reserved_key_error__', None)


def _collectReservedKeys(cls: type) -> list[str]:
  """Collects the reserved keys."""

  reservedKeys = getattr(cls, '__reserved__', None)

  if reservedKeys is None:
    return []

  if not isinstance(reservedKeys, list):
    if isinstance(reservedKeys, tuple):
      reservedKeys = list(reservedKeys)
    elif isinstance(reservedKeys, dict):
      reservedKeys = [k for k in reservedKeys.keys()]
    else:
      raise TypeError
  return [key for key in reservedKeys if isinstance(key, str)]


def _getSampleKeys(cls: type, *args) -> list[str]:
  """Creates a list of keys that are not reserved by the obj."""
  defVals = [12, 8, 12]
  intArgs = [arg for arg in args if isinstance(arg, int)]
  while len(intArgs) < 3:
    intArgs.append(defVals[len(intArgs)])
  N, a, b = intArgs

  reservedKeys = _collectReservedKeys(cls)
  randKeys = _randomWords(N, a, b)
  out = [arg for arg in randKeys if arg not in reservedKeys]
  while len(out) < N:
    out.append(_randomWord(a, b))
  return out


def _hasAttributes(cls: type) -> Union[Exception, bool]:
  """This method checks if the obj has the necessary attributes. It
  returns a list of the missing attributes. """
  requiredAttributes = ['__getitem__', '__setitem__', '__contains__']
  missingAttributes = []
  for key in requiredAttributes:
    if getattr(cls, key, None) is None:
      missingAttributes.append(key)
  return AttributeError(*missingAttributes) if missingAttributes else []


def _setterTest(obj: object, ) -> Union[Exception, bool]:
  """This method checks that the obj does support item setting. """

  if TYPE_CHECKING:
    obj = cast(dict, obj)

  reservedKeys = _collectReservedKeys(obj.__class__)
  randKeys = _randomWords(12, 8, 12)
  sampleKeys = [arg for arg in randKeys if arg not in reservedKeys]

  for key in sampleKeys:
    try:
      obj.__setitem__(key, 777)
    except TypeError as e:
      raise NotImplementedError from e
    except Exception as e:
      return e

  return True


def _reservedKeyTest(obj: object, cls: type) -> Union[Exception, bool]:
  """If the obj reserves keywords, this method looks for them at
  __reserved__ attribute. If the object provides this list, it should also
  provide the specific exception it intends to raise at
  __reserved_key_error__ attribute. If only the __reserved__ attribute is
  present, this method will just use other keys in the test. If both are
  provided, this method will also check that the proper exception is
  raised."""

  reservedKeys = _collectReservedKeys(cls)
  reservedKeyError = _collectError(cls)

  if not reservedKeys or reservedKeyError is not None:
    return True

  if TYPE_CHECKING:
    obj = cast(dict, obj)

  for key in reservedKeys:
    try:
      obj.__setitem__(key, 777)
    except Exception as e:
      if e is not reservedKeyError:
        return e
  return True


def _getterTest(obj: object, cls: type) -> Union[Exception, bool]:
  """This method checks item getting. Please note that this method
  considers the test passed as long as the obj returns a value for some
  key after a value has been set at that key.

  nameSpace[key] = 69  # setter
  val = nameSpace[key]  # getter
  val >>> 420  #  This method allows this. """

  if TYPE_CHECKING:
    obj = cast(dict, obj)

  sampleKeys = _getSampleKeys(cls, )

  for key in sampleKeys:
    obj.__setitem__(key, randint(0, 2 ** 32 - 1))
    try:
      _ = obj.__getitem__(key)
    except Exception as e:
      return e


def _getterErrorTest(obj: object, cls: type) -> Union[Exception, bool]:
  """This method checks that trying to get an item at a key not present
  raises KeyError. Please note that trying to use a namespace that does
  not raise a KeyError in this circumstance will cause undefined behaviour
  with no clear indication that the problem is with the namespace."""

  if TYPE_CHECKING:
    obj = cast(dict, obj)

  sampleKeys = [k for k in _getSampleKeys(cls, 12, 8, 12) if k not in obj]

  for key in sampleKeys:
    try:
      _ = obj.__getitem__(key)
    except KeyError as e:
      if not isinstance(e, KeyError):
        raise TypeError
  return True


def nameSpaceValidator(cls_: type, errorHandler: object) -> object:
  """Validates the namespace"""
  if TYPE_CHECKING:  # Static type checking is disgusting
    errorHandler = cast(Callable, errorHandler)
  cls = cls_
  if TYPE_CHECKING:
    cls = cast(Type[Self], cls_)
  obj = cls.__new__(cls, None)
  missingAttributes = _hasAttributes(cls)
  if missingAttributes:
    raise errorHandler(cls, missingAttributes, )
  test = _setterTest(obj, )
  if isinstance(test, Exception):
    raise errorHandler(cls, test)
  test = _reservedKeyTest(obj, cls)
  if isinstance(test, Exception):
    raise errorHandler(cls, test)
  test = _getterTest(obj, cls)
  if isinstance(test, Exception):
    raise errorHandler(cls, test)
  test = _getterErrorTest(obj, cls)
  if isinstance(test, Exception):
    raise errorHandler(cls, test)
  return True
