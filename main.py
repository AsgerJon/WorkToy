"""
Main Tester Script
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING
from types import FunctionType, \
  MethodType, \
  BuiltinFunctionType

from types import ModuleType, MemberDescriptorType
from types import WrapperDescriptorType, MethodWrapperType
from types import MethodDescriptorType, ClassMethodDescriptorType
from types import LambdaType, BuiltinMethodType

from worktoy.utilities import typeCast
from worktoy.utilities.combinatorics import Arrangements
from worktoy.waitaminute import TypeException

try:
  from pyperclip import copy
except ImportError:

  def copy(text: str) -> None:
    pass

from profile_tests import profileTests
from worktoy.desc import Field
from yolo_dev import runTests, runTest, yolo

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Callable, Self, Any

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
  Peaking at recursion thing
  """

  arrangements = Arrangements('Tom', 'Dick', 'Harry')

  try:
    peekHashable = arrangements.isHashable(_recursion=True)
  except RecursionError:
    peekHashable = None

  print(peekHashable)

  return 0


def tester02() -> int:
  """
  Testing __slots__
  """

  class Complex:
    """
    Complex number implementation
    """
    if TYPE_CHECKING:  # pragma: no cover
      REAL: float
      IMAG: float
      MaybeSelf = Union[NotImplementedType, Self]

    @classmethod
    def _getFallbackReal(cls) -> float:
      return 0.

    @classmethod
    def _getFallbackImag(cls) -> float:
      return 0.

    @classmethod
    def _truthyFloat(cls, value: float) -> bool:
      return True if abs(value) > sys.float_info.epsilon else False

    __slots__ = ('REAL', 'IMAG')

    def __init__(self, *args) -> None:
      if not args:
        self.REAL = self._getFallbackReal()
        self.IMAG = self._getFallbackImag()
      if len(args) == 1:
        arg = args[0]
        if isinstance(arg, str):
          try:
            arg = complex(arg)
          except ValueError as valueError:
            try:
              arg = float(arg)
            except ValueError:
              e = TypeException('arg', arg, (int, float, complex))
              raise e from valueError
        elif isinstance(arg, (int, float, complex)):
          arg = args[0] + 0j
          self.REAL = arg.real
          self.IMAG = arg.imag
        else:
          raise TypeException('arg', arg, (int, float, complex))
      if len(args) == 2:
        floatArgs = (*(typeCast(float, arg) for arg in args),)
        self.REAL, self.IMAG, *_ = (*floatArgs, None, None)
      if len(args) > 2:
        infoSpec = """Expected at most 2 arguments, got %d!"""
        raise ValueError('args', args, infoSpec % len(args))

    @classmethod
    def _resolveOther(cls, other: Any) -> Optional[Complex]:
      if isinstance(other, cls):
        return other
      if isinstance(other, (tuple, list)):
        try:
          resolved = cls(*other)
        except (TypeError, ValueError):
          return NotImplemented
        else:
          return resolved
      try:
        resolved = cls(other)
      except (TypeError, ValueError):
        return NotImplemented
      else:
        return resolved

    def __invert__(self) -> Complex:  # Conjugate
      cls = type(self)
      # noinspection PyTypeChecker
      return cls(self.REAL, -self.IMAG)

    def __complex__(self, ) -> complex:
      return self.REAL + self.IMAG * 1j

    def __mul__(self, other: Complex) -> MaybeSelf:
      cls = type(self)
      if isinstance(other, cls):
        # noinspection PyTypeChecker
        return cls(complex(self) * complex(other))
      return NotImplemented

    def __abs__(self, ) -> float:
      return (self * (~self)).REAL ** 0.5

    def __bool__(self, ) -> bool:
      return True if self._truthyFloat(abs(self)) else False

    def __sub__(self, other: Complex) -> MaybeSelf:
      raise NotImplementedError

    def __str__(self, ) -> str:
      if not self:
        return '0'
      if not self._truthyFloat(self.REAL):
        if self.IMAG < 0:
          infoSpec = """-%r J"""
        else:
          infoSpec = """%r J"""
        return infoSpec % abs(self.IMAG)
      if not self._truthyFloat(self.IMAG):
        if self.REAL < 0:
          infoSpec = """-%r"""
        else:
          infoSpec = """%r"""
        return infoSpec % abs(self.REAL)
      infoSpec = """%s%r %s %r J"""
      realSign = '-' if self.REAL < 0 else ''
      imagSign = '-' if self.IMAG < 0 else '+'
      return infoSpec % (realSign, abs(self.REAL), imagSign, abs(self.IMAG))

    def __repr__(self, ) -> str:
      infoSpec = """%s(%r, %r)"""
      return infoSpec % (type(self).__name__, self.REAL, self.IMAG)

  z0 = Complex()
  z1 = Complex(69 + 420j)
  z2 = Complex(1337, 80085.)

  print(z0.REAL)
  try:
    attr = getattr(Complex, 'REAL')
  except AttributeError as attributeError:
    infoSpec = """Caught '%s': %s!"""
    info = infoSpec % (type(attributeError).__name__, attributeError)
    print(info)
  else:
    print(attr)
    print(type(attr))
    print(attr.__objclass__)
    print(attr.__get__)
  return 0


def tester03() -> int:
  """
  Testing member_descriptor trolling
  """
  return 0


heyClaude = """claude --resume ea45daf8-2917-45da-b0c4-f5ca02b77161"""


def firstInts(n: int) -> int:
  if n < 0:
    raise ValueError
  if n:
    return n + firstInts(n - 1)
  return 0


def tester04() -> int:
  """
  Testing recursion peaking
  """
  res = firstInts(10)
  print("""First 10 ints: %d""" % res)
  return 0


if __name__ == '__main__':
  # yolo(tester04)
  yolo(runTests, tester00)
