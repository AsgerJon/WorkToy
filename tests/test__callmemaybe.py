#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence

import unittest
from typing import Never, NoReturn
from unittest.mock import MagicMock

from icecream import ic

from mainclass import Cunt
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import UnexpectedStateError

ic.configureOutput(includeContext=True)


class TestCallMeMaybe(unittest.TestCase):

  def test_singleton(self):
    cm1 = CallMeMaybe()
    cm2 = CallMeMaybe()
    self.assertIs(cm1, cm2)

  def test_call(self):
    cm = CallMeMaybe()
    self.assertIs(cm(), cm)

  def test_str(self):
    cm = CallMeMaybe()
    self.assertEqual(str(cm), "CallMeMaybe")

  def test_repr(self):
    cm = CallMeMaybe()
    self.assertEqual(repr(cm), "CallMeMaybe")

  def test_instancecheck(self):
    cm = CallMeMaybe()
    self.assertTrue(isinstance(cm, type))

  def test_instancecheck_no_class(self):
    cm = CallMeMaybe
    self.assertFalse(isinstance(None, cm))

  def test_instancecheck_function(self):
    def func():
      pass

    cm = CallMeMaybe
    self.assertTrue(isinstance(func, cm))

  def test_instancecheck_method(self):
    class MyClass:
      def method(self):
        pass

    cm = CallMeMaybe
    self.assertTrue(isinstance(MyClass().method, cm))
