"""Testing Pathify"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import os
from typing import NoReturn
from unittest import TestCase

from worktoy.dio import Pathify


@Pathify()
class TargetClass:
  """This class gets decorated"""

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __str__(self) -> str:
    """String representation"""
    parentDir = os.path.dirname(self.pathName)
    msg = """My path is %s and my env is %s. My parent dir is %s"""
    return msg % (self.pathName, self.envName, parentDir)


class TestPathify(TestCase):
  """Testing Pathify
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def setUp(self) -> NoReturn:
    """Sets up the tests"""
    self.target = TargetClass()

  def testDecoration(self) -> NoReturn:
    """Testing if the fields have been applied to the TargetClass"""
    try:
      print(self.target)
      self.assertTrue(True)
    except AttributeError as e:
      print('lol fail: \n%s' % e)
      self.assertTrue(False)

  def testParentDir(self) -> NoReturn:
    """Testing if the __pos__ method was updated"""
    print(self.target)
    prevParent = os.path.dirname(self.target.pathName)
    parent = +self.target
    print(self.target)
    self.assertEqual(prevParent, parent.pathName)
