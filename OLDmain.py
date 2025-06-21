"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2023-2025 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from worktoy.core import Some
from worktoy.parse import maybe
from worktoy.static import PreClass
from worktoy.text import monoSpace
from worktoy.waitaminute import CascadeException
from yolo import yolo, runTests

sys.path.append('./src')
sys.path.append('./src/worktoy')

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


def tester00() -> int:
  """Hello World!"""
  stuff = ['hello world!', os, sys, frozenset]
  for item in stuff:
    print(item)
  return 0


def tester01() -> int:
  """
  Testing the PreClass
  """
  preClass = PreClass(69420, 'Foo', type)
  print('hash(preClass):', hash(preClass))
  print('preClass.__name__', preClass.__name__)
  print('preClass.__class__', preClass.__class__)
  print('type(preClass):', type(preClass))
  return 0


def tester02() -> int:
  """
  Testing module stuff
  """
  return 0


def tester03() -> int:
  """
  Testing better metaclass error message
  """
  exceptions = []

  try:
    raise ValueError
  except ValueError as valueError:
    exceptions.append(valueError)
  try:
    raise TypeError
  except TypeError as typeError:
    exceptions.append(typeError)
  try:
    raise AttributeError
  except AttributeError as attributeError:
    exceptions.append(attributeError)
  try:
    raise KeyError
  except KeyError as keyError:
    exceptions.append(keyError)
  try:
    raise CascadeException(*exceptions, )
  except CascadeException as cascadeException:
    print('__str__')
    print(cascadeException)
    print('__repr__')
    print(repr(cascadeException))
  return 0


def tester04() -> int:
  """
  Testing monoSpace
  """
  # Point3D = EZData('Point3D', x=69, y=420, z=1337)
  try:
    print(annotations)
  except NameError as nameError:
    print('annotations not here cause: %s' % str(nameError))
  else:
    print("""Here be annotations: '%s'""" % str(annotations))
  finally:
    pass
  return 0


def tester05() -> int:
  """
  LOL
  """
  print(Some)
  print(isinstance('urmom', Some))
  print(isinstance(None, Some))
  return 0


def tester06() -> int:
  """
  Testing the Foo class
  """

  try:

    class MetaFoo(type):
      pass

    class MetaBar(type):
      pass

    class Foo(metaclass=MetaFoo):
      pass

    class Bar(Foo, metaclass=MetaBar):
      pass  # raises
  except Exception as exception:
    print(exception)
    return 1
  else:
    return 0
  finally:
    print('Finally block executed')


class Num:
  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    print("""Before returning 69:""")
    print(getattr(instance, '__test_number__', 'breh'))
    try:
      return 69
    finally:
      print("""After returning 69:""")
      print(getattr(instance, '__test_number__', 'breh'))


def tester07() -> int:
  """
  Testing the metaclass space thing
  """
  from main_tester_class_04 import Foo
  print("""The tester just ensures the Foo class is imported""")
  print(Foo())
  return 0


def tester08() -> int:
  """
  Testing the 'Some' sentinel
  """

  print(Some)
  print('isinstance("Hello", Some)', end='  ')  # Should be True
  print(isinstance("Hello", Some))
  print('isinstance(None, Some)', end='  ')  # Should be False
  print(isinstance(None, Some))
  print('issubclass(Some, object)', end='  ')  # Should be True
  print(issubclass(Some, object))
  print('issubclass(type(None), Some)', end='  ')  # Should be False
  print(issubclass(type(None), Some))
  print('issubclass(None, Some)', end='  ')  # Error or False lol
  try:
    print(issubclass(None, Some))
  except TypeError as typeError:
    print('lol: %s' % str(typeError))
  print('isinstance(None, object)', end='  ')  # Should be True
  print(isinstance(None, object))
  print('issubclass(type(None), object)', end='  ')  # Should be True
  print(issubclass(type(None), object))
  return 0


def tester09() -> int:
  """
  Testing the exportSomeStuff function
  """
  f = lambda n, c=1: f(n - 1, c * n) if n else c
  g = lambda n: n * g(n - 1) if n else 1

  print("""Factorial test:""")
  for i in range(10):
    print("""%d: %5d""" % (i, f(i)))
  return 0


def tester10() -> int:
  """
  Testing the 'runTests' function
  """
  try:
    print(hash(dict()))
  except Exception as exception:
    print("""Exception raised: %s""" % str(exception))
    print(type(exception).__name__)
  return 0


def tester11() -> int:
  """
  Testing the 'runTests' function
  """
  try:
    for urmom in 69:
      print(urmom)
  except Exception as exception:
    print(exception)
    return 0


def tester12() -> int:
  """
  Testing the 'runTests' function
  """
  sluts = lambda: None
  try:
    if 'urmom' in sluts:
      print('breh')
  except Exception as exception:
    print(exception)
    print(type(exception).__name__)
  return 0


def tester13() -> int:
  """
  Testing the len error message
  """
  try:
    print(len(lambda: None))
  except Exception as exception:
    print(exception)
    print(type(exception).__name__)
  return 0


def tester14() -> int:
  """
  Testing missing attribute on type
  """
  try:
    print(getattr(type, 'urmom'))
  except Exception as exception:
    print(exception)
    print(type(exception).__name__)
  try:
    print(getattr(69, 'urmom'))
  except Exception as exception:
    print(exception)
    print(type(exception).__name__)
  return 0


def tester15() -> int:
  """
  Testing the __getitem__ on unsupported class
  """
  try:
    _ = type['urmom']
  except Exception as exception:
    print(exception)
  return 0


def tester16() -> int:
  """
  Testing accessing a non-existent attribute
  """
  try:
    print(getattr(69, 'urmom'))
  except Exception as exception:
    print(exception)
    print(type(exception).__name__)
  return 0


def tester17() -> int:
  """
  Testing the 'runTests' function
  """

  class No:
    pass

  args = '69', 420, .1337, 80085j, (54077, 8008135),
  classes = [int, float, complex, type, dict, No]
  info = 'pycharm, please!'

  print('TESTING ONE ARGUMENT AT A TIME')
  for cls in classes:
    for arg in args:
      info = None
      try:
        _ = cls(arg)
      except Exception as exception:
        infoSpec = """ --- %s(%s) <br>%s! %s"""
        clsName = cls.__name__
        argStr = monoSpace(str(arg))
        eType = type(exception).__name__
        eStr = monoSpace(str(exception))
        info = monoSpace(infoSpec % (clsName, argStr, eType, eStr))
      else:
        infoSpec = """ --- %s(%s) <br><tab>no exception!"""
        clsName = cls.__name__
        argStr = monoSpace(str(arg))
        info = monoSpace(infoSpec % (clsName, argStr))
      finally:
        n = max(len(i) for i in info.split('\n'))
        print(n * '_')
        print(info)
        print(n * '¨')
  print('TESTING ALL ARGUMENTS AT ONCE')
  for cls in classes:
    info = None
    try:
      _ = cls(*args)
    except Exception as exception:
      infoSpec = """ --- %s(%s) <br>%s! %s"""
      clsName = cls.__name__
      argsStr = monoSpace(str(args))
      eType = type(exception).__name__
      eStr = monoSpace(str(exception))
      info = monoSpace(infoSpec % (clsName, argsStr, eType, eStr))
    else:
      infoSpec = """ --- %s(%s) <br><tab>no exception!"""
      clsName = cls.__name__
      argsStr = monoSpace(str(args))
      info = monoSpace(infoSpec % (clsName, argsStr))
    finally:
      n = max(len(i) for i in info.split('\n'))
      print(n * '_')
      print(info)
      print(n * '¨')
  print('TESTING TWO ARGUMENTS AT A TIME')
  permutations = [(i, j) for i in args for j in args if i is not j]
  for cls in classes:
    for arg1, arg2 in permutations:
      info = None
      try:
        _ = cls(arg1, arg2)
      except Exception as exception:
        infoSpec = """ --- %s(%s, %s) <br>%s! %s"""
        clsName = cls.__name__
        arg1Str = monoSpace(str(arg1))
        arg2Str = monoSpace(str(arg2))
        eType = type(exception).__name__
        eStr = monoSpace(str(exception))
        info = monoSpace(infoSpec % (clsName, arg1Str, arg2Str, eType, eStr))
      else:
        infoSpec = """ --- %s(%s, %s) <br><tab>no exception!"""
        clsName = cls.__name__
        arg1Str = monoSpace(str(arg1))
        arg2Str = monoSpace(str(arg2))
        info = monoSpace(infoSpec % (clsName, arg1Str, arg2Str))
      finally:
        n = max(len(i) for i in info.split('\n'))
        print(n * '_')
        print(info)
        print(n * '¨')
  return 0


def tester18() -> int:
  """
  Testing some mro stuff
  """

  class UrMom:
    pass

  class UrDad:
    pass

  class TheMilkMan:
    pass

  class TheMailMan:
    pass

  class TheTennisCoach:
    pass

  class U(UrMom, TheMilkMan, TheMailMan, TheTennisCoach):
    pass

  for item in U.__mro__:
    print(item)

  return 0


def tester19() -> int:
  """
  Testing the TypeSig example
  """
  from examples import typeSigExample
  testArgs = [
      (69, 420),
      (0.1337, 0.80085),
      ('1337', '80085'),
      ('lmao',),
  ]
  for testArg in testArgs:
    res = typeSigExample(*testArg)
    infoSpec = """Testing typeSigExample with arguments (%s)"""
    info = infoSpec % (str(testArg),)
    print('_' * 50)
    print(info)
    if res:
      print("""Error!""")
      print('¨' * 50)
      return res
    print('¨' * 50)
  return 0


def tester20() -> int:
  """
  Testing environment variables
  """
  envVar = os.environ.get('RUNNING_TESTS', 'not set')
  print('RUNNING_TESTS:', envVar)
  return 0


def tester21() -> int:
  """
  Testing the 'id' function
  """
  id69 = id(69)
  infoSpec = """The id of '69' is: '%s' of type: '%s'"""
  info = infoSpec % (id69, type(id69).__name__)
  print(info)
  return 0


def tester22() -> int:
  """
  Testing __get__ and stuff
  """
  try:
    print('object.__get__', object.__get__)
  except Exception as exception:
    print('object.__get__ raised an exception: %s' % str(exception))

  try:
    print('type.__get__', type.__get__)
  except Exception as exception:
    print('type.__get__ raised an exception: %s' % str(exception))

  return 0


class GrandMa(type):
  def __getattribute__(cls, key: str) -> Any:
    try:
      return type.__getattribute__(cls, key)
    finally:
      infoSpec = """That's nice dear! (key: '%s')"""
      print(infoSpec % key)


class UrMom(metaclass=GrandMa):

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    print("""Parent.__get__ called""")
    try:
      return 69
    finally:
      print("""Parent.__get__ finished""")


class Child(UrMom):
  def __getattribute__(self, key: str, ) -> Any:
    try:
      return object.__getattribute__(self, key)
    finally:
      infoSpec = """Child.__getattribute__ called with key: '%s'"""
      print(infoSpec % key)


class Troll(metaclass=GrandMa):
  breh = Child()


if __name__ == '__main__':
  yolo(runTests, tester20)
