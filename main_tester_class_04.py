"""
Testing what happens to the namespace when weird lines without equal sign
occur.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from time import sleep


class Space(dict):
  """A simple dictionary-like class for testing purposes."""

  def __setitem__(self, key: str, value: object) -> None:
    """Set an item in the dictionary."""
    print(50 * '_')
    print("""Namespace setitem""")
    print("""Key: '%s'""" % repr(key))
    valueStr = str(value)
    if len(valueStr) > 50:
      valueStr = value[:47] + '...'
    print("""Value: '%s'""" % valueStr)
    print("""Type: '%s'""" % type(value).__qualname__)
    print("""End of namespace setitem""")
    print(50 * '¨')
    super().__setitem__(key, value)

  def __getitem__(self, key: str) -> object:
    """Get an item from the dictionary."""
    print(50 * '_')
    print("""Namespace getitem""")
    print("""Key: '%s'""" % repr(key))
    sleep(0.01)
    value = None
    error = None
    valueStr = ''
    try:
      value = super().__getitem__(key)
    except KeyError as keyError:
      valueSTr = str(keyError) or type(keyError).__qualname__
      error = keyError
    else:
      valueStr = str(value)
    sleep(0.01)
    if len(valueStr) > 50:
      valueStr = valueStr[:47] + '...'
    print("""Value: '%s'""" % valueStr)

    sleep(0.01)
    if error is None:
      print("""End of namespace getitem\n%s""" % ('-' * 50))
      return value
    e = type(error).__qualname__
    print("""Error: '%s' for name: %s""" % (e, key))
    print("""End of namespace getitem""")
    print(50 * '¨')
    sleep(0.01)
    raise error


class Meta(type):
  """A simple metaclass for testing purposes."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> Space:
    """Prepare the namespace for the class."""
    return Space()


class Bar:

  def __matmul__(self, *_) -> object:
    return self


class Foo(metaclass=Meta):
  """A simple class using the custom metaclass."""

  print(""" --- About to put a comment in the namespace:""")
  #  This is a comment in the namespace

  print(""" --- About to put a string in the namespace:""")
  'This is a string in the namespace'

  print(""" --- About to put a Bar instance with its @ matmul:""")
  Bar() @ Bar()  # NOQA

  print(""" --- About to put a Bar instance without its @ matmul:""")
  Bar()

  print(""" --- About to put a list in the namespace:""")
  [1, 2, 3]

  print(""" --- About to put a dictionary in the namespace:""")
  {'key': 'value'}

  print(""" --- About to put a tuple in the namespace:""")
  (1, 2, 3)

  print(""" --- About to put a set in the namespace:""")
  {1, 2, 3}

  print(""" --- About to put a None in the namespace:""")
  None

  print(""" --- About to put a lambda in the namespace:""")
  lambda x: x + 1
