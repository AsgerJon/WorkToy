"""
Main Tester Script
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any
from types import FunctionType, MethodType, BuiltinFunctionType
from types import ModuleType, MemberDescriptorType
from types import WrapperDescriptorType, MethodWrapperType
from types import MethodDescriptorType, ClassMethodDescriptorType
from types import LambdaType, BuiltinMethodType

from pyperclip import copy

from profile_tests import profileTests
from tests.test_mcls.test_hooks.test_flex_call_hook import TestFlexCallHook
from tests.test_overload.test_overload_flex import TestOverloadFlex
from worktoy.desc import Field
from worktoy.utilities import ExceptionInfo, textFmt, wordWrap
from yolo_dev import yolo, runTests, runTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  Tester: TypeAlias = Callable[[], int]
  MaybeType: TypeAlias = Optional[type]

Func = (
  FunctionType,
  MethodType,
  BuiltinFunctionType,
  ModuleType,
  MemberDescriptorType,
  WrapperDescriptorType,
  MethodWrapperType,
  MethodDescriptorType,
  ClassMethodDescriptorType,
  LambdaType,
  BuiltinMethodType,
)

Names = (
  'FunctionType',
  'MethodType',
  'BuiltinFunctionType',
  'ModuleType',
  'MemberDescriptorType',
  'WrapperDescriptorType',
  'MethodWrapperType',
  'MethodDescriptorType',
  'ClassMethodDescriptorType',
  'LambdaType',
  'BuiltinMethodType',
)


def tester00() -> int:
  """
  Hello World!
  """
  stuff = [os, sys, 'Hello world!', profileTests, runTest, runTests, copy]
  for item in stuff:
    line = str(item)
    if len(line) > 64:
      line = """%s...""" % (line[:61],)
    print("""|  %64s  |""" % line)
  else:
    return 0
  return 1


def tester01() -> int:
  """
  Testing operator order
  """

  class Foo:

    def __rmatmul__(self, other):
      print("""from left @""")
      return self

    def __matmul__(self, other):
      print("""to the right @""")
      return self

  with ExceptionInfo() as info:
    res = 69 @ Foo() @ 420
  if info:
    print(info)
  else:
    print(res)
  return 0


def tester02() -> int:
  """
  Testing __set_name__ edges
  """

  class Desc:
    def __set_name__(self, owner, name):
      print("""Desc.__set_name__(%s, %s)""" % (owner.__name__, name))

    def __get__(self, instance, owner):
      return self

  class Breh(Desc):
    __set_name__ = """Trololololo"""
    __set_name__ = None
    __set_name__ = lambda: None
    __set_name__ = print

  class Foo:
    bar = Desc()
    breh = Breh()

  foo = Foo()
  print(foo.bar)
  return 0


def tester03() -> int:
  """
  Testing 'classmethod' type
  """

  class Space(dict):
    __expect_class_method__: bool = False
    __expect_static_method__: bool = False
    __info_reports__: list[str] = []

    def __getitem__(self, key: str) -> Any:
      try:
        value = dict.__getitem__(self, key)
      except KeyError as keyError:
        if 'classmethod' in str(keyError):
          self.__expect_class_method__ = True
          self.__expect_static_method__ = False
        elif 'staticmethod' in str(keyError):
          self.__expect_class_method__ = False
          self.__expect_static_method__ = True
        else:
          self.__expect_class_method__ = False
          self.__expect_static_method__ = False
        raise keyError
      else:
        return value

    def report(self, key: str, value: Callable, ) -> None:
      lines = []
      if self.__expect_static_method__:

        lines.append("""While expecting a '@staticmethod':""")
      elif self.__expect_class_method__:
        lines.append("""While expecting a '@classmethod':""")
      elif callable(value):
        lines.append(
          """While not expecting a '@classmethod' or '@staticmethod':""")
      else:
        return
      infoSpec = """<tab>key: '%s': type: '%s'"""
      info = infoSpec % (key, type(value).__name__)
      lines.append(info)
      infoSpec = """<tab>isinstance(value, FunctionType): %s"""
      flag = 'True' if isinstance(value, FunctionType) else 'False'
      info = infoSpec % flag
      lines.append(info)
      infoSpec = """<tab><tab>Retrieving value again: dict.__getitem__:"""
      lines.append(infoSpec)
      setValue = dict.__getitem__(self, key)
      infoSpec = """<tab><tab>type: '%s'"""
      info = infoSpec % (type(setValue).__name__,)
      lines.append(info)
      infoSpec = """<tab><tab>isinstance(value, FunctionType): %s"""
      flag = 'True' if isinstance(setValue, FunctionType) else 'False'
      info = infoSpec % flag
      lines.append(info)
      linesFmt = [textFmt(line, tabToken='breh') for line in lines]
      n = max(len(line) for line in linesFmt)
      if n < 64:
        linesWrapped = [*linesFmt, ]
      else:
        linesWrapped = [wordWrap(64, line) for line in linesFmt]
        n = 64
      linesJoined = str.join('<br>', linesWrapped)
      self.__info_reports__.append('_' * n)
      self.__info_reports__.append(textFmt(linesJoined))
      self.__info_reports__.append('¨' * n)

    def __setitem__(self, key: str, value: Any) -> None:
      dict.__setitem__(self, key, value)
      self.report(key, value)
      self.__expect_class_method__ = False
      self.__expect_static_method__ = False

  class Meta(type):
    @classmethod
    def __prepare__(mcls, *args, **kwargs) -> Space:
      return Space()

    def __new__(mcls, name: str, bases: tuple, space: Space, ) -> type:
      cls = super().__new__(mcls, name, bases, {**space, })
      print(str.join(os.linesep, space.__info_reports__))
      copy(str.join(os.linesep, space.__info_reports__))
      return cls

  class Foo(metaclass=Meta):
    @classmethod
    def eggs(cls) -> None: pass

    @staticmethod
    def ham() -> None: pass

    def instanceMethod(self, ) -> None: pass

  return 0


if __name__ == '__main__':
  # yolo(tester03)
  # runTest(TestOverloadFlex)
  yolo(runTests, tester00)
