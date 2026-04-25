"""
Main Tester Script
"""
#  AGPL-3.0 license
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

from pyperclip import copy

from profile_tests import profileTests
from tests.test_utilities.test_perm_indexed import TestPermIndexed
from worktoy.desc import Field
from worktoy.utilities import perm, permTraced
from worktoy.utilities._perm import _intPerm
from yolo_dev import yolo, runTests, runTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  Tester: TypeAlias = Callable[[], int]

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
  stuff = [os, sys, 'Hello world!', profileTests, runTest, runTests]
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
  Testing the worktoy.utilities.perm function
  """
  types_ = int, str, float
  perms = perm(*types_)
  seen = []
  d = 0
  for perm_ in perms:
    print("""%s""" % (str(perm_),))
    if perm_ in seen:
      print("""Duplicate: %s""" % (perm_,))
      d += 1
    seen.append(perm_)
  else:
    if not d:
      print("""No duplicates!""")
  return 0


def tester02() -> int:
  """
  Verifying the reworked permutation generator
  """
  for item in permTraced('tom', 'dick', 'harry'):
    print(item)
  for item in permTraced(int, int, float):
    print(item)
  return 0


def tester03() -> int:
  """
  Testing the _intPerm method.
  """

  lines = []

  for n in [3, 4, 5]:
    for line in _intPerm(n):
      lines.append(str(line))

  copy(str.join('\n', lines))

  return 0


if __name__ == '__main__':
  # yolo(tester03)
  # runTest(TestPermIndexed)
  yolo(runTests, tester00)
