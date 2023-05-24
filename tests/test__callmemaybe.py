#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
import typing
from typing import NoReturn
from unittest import TestCase, skip

from worktoy.core import CallMeMaybe


class HasCall:
  """This class implements __call__"""

  def __call__(self) -> NoReturn:
    """Implementation of call"""

  def __str__(self) -> str:
    """String Representation"""
    return 'call me anytime....'


class NoCall:
  """This class does not implement __call__"""

  def __str__(self) -> str:
    """String Representation"""
    return 'can call this....'


class TestCallMeMaybe(TestCase):
  """Testing CallMeMaybe
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def getCallables(self) -> list:
    """Getter-function for callables."""

  def setUp(self) -> NoReturn:
    """Sets up each test"""
    self.doCall = HasCall()
    self.noCall = NoCall()

  def testBuiltinFunctions(self) -> NoReturn:
    """Testing proper recognition of callable builtins"""
    self.assertIsInstance(print, CallMeMaybe)
    self.assertIsInstance(callable, CallMeMaybe)
    self.assertIsInstance(enumerate, CallMeMaybe)
    self.assertIsInstance(len, CallMeMaybe)

  def testCustomClass(self) -> NoReturn:
    """Testing two custom classes, one with __call__ implemented and one
    without."""
    self.assertIsInstance(self.doCall, CallMeMaybe)
    self.assertNotIsInstance(self.noCall, CallMeMaybe)

  def testCustomClass2(self) -> NoReturn:
    """Testing two custom classes, one with __call__ implemented and one
    without."""
    self.assertIsInstance(self.doCall, typing.Callable)
    self.assertNotIsInstance(self.noCall, typing.Callable)
