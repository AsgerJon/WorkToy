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

from worktoy.utilities.combinatorics import Arrangements

try:
  from pyperclip import copy
except ImportError:

  def copy(text: str) -> None:
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
  Peaking at recursion thing
  """

  arrangements = Arrangements('Tom', 'Dick', 'Harry')

  try:
    peekHashable = arrangements.isHashable(_recursion=True)
  except RecursionError:
    peekHashable = None

  print(peekHashable)

  return 0


if __name__ == '__main__':
  yolo(runTests, tester00)
