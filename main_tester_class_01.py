"""
breh
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import Any, Iterator, Self, Never


class Space(dict):
  hist = []

  def __getitem__(self, key: str, ) -> Any:
    value = None
    try:
      value = dict.__getitem__(self, key)
    except KeyError as keyError:
      value = keyError
      raise keyError
    except TypeError as typeError:
      raise KeyError(key)
    else:
      pass
    finally:
      self.hist.append(('__getitem__', key, value, None))
    return value

  def __setitem__(self, key: str, value: Any) -> None:

    try:
      oldValue = dict.get(self, key)
    except Exception as exception:
      oldValue = exception
    else:
      pass
    finally:
      dict.__setitem__(self, key, value)
      self.hist.append(('__setitem__', key, oldValue, value))

  def __delitem__(self, key: str, ) -> None:
    oldValue = None
    try:
      oldValue = dict.get(self, key)
    except Exception as exception:
      oldValue = exception
    finally:
      dict.__delitem__(self, key)
      self.hist.append(('__delitem__', key, oldValue, None))

  def __iter__(self, ) -> Iterator[tuple]:
    yield from self.hist


class Meta(type):

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> Space:
    return Space()

  # def __new__(mcls, name, bases, space, **kwargs) -> type:
  #   return type.__new__(mcls, name, bases, space, **kwargs)


Foo = None
try:
  class Foo(metaclass=Meta):
    """This is a test class."""
    pass
except Exception as exception:
  print(exception)
else:
  pass
finally:
  if Foo is None:
    Foo = lambda *_: None
