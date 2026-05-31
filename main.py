"""
Main Tester Script
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING
from types import FunctionType, MethodType, BuiltinFunctionType
from types import ModuleType, MemberDescriptorType
from types import WrapperDescriptorType, MethodWrapperType
from types import MethodDescriptorType, ClassMethodDescriptorType
from types import LambdaType, BuiltinMethodType

from test_overload.test_this_cast_recursion import TestThisCastRecursion
from worktoy.utilities import ExceptionInfo, textFmt

try:
  from pyperclip import copy
except ImportError:

  def copy(_) -> None:
    pass

from profile_tests import profileTests
from worktoy.desc import Field
from yolo_dev import runTests, runTest, yolo

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  Tester: TypeAlias = Callable[[], int]
  MaybeType: TypeAlias = Optional[type]

NotImplementedType = type(NotImplemented)

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
  list.extend(stuff, (yolo,))
  for item in stuff:
    line = str(item)
    if len(line) > 64:
      line = """%s...""" % (line[:61],)
    print("""|  %64s  |""" % line)
  else:
    return 0


def tester01() -> int:
  """
  "They call be Nobody!" "Bro, no we don't, we call you 'None'!"
  """

  class Derp:
    callMeMaybe = None

  derp = Derp()
  with ExceptionInfo(TypeError) as info:
    res = derp.callMeMaybe()
  if info:
    print(info.actualException)
  else:
    print(res)

  return 0


def tester02() -> int:
  """
  testing length
  Returns
  -------

  """
  words = """software. From 1.0 onwards, versions that no longer receive 
  security updates"""
  print(len(textFmt(words)))
  return 0


if __name__ == '__main__':
  # runTest(TestThisCastRecursion)
  yolo(tester02)
  # yolo(runTests, tester00)
