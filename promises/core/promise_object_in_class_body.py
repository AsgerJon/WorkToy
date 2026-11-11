"""
PromiseObjectInClassBody promises how a plain 'Object' behaves in a
class body, from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class PromiseObjectInClassBody(TestCase):
  """
  An 'Object' that defines none of the three access methods, placed in a
  class body, is a class variable shared by every instance: reading it
  through an instance gives the object itself, writing raises
  'ReadOnlyError' and deleting raises 'ProtectedError', both
  'AttributeError's. A class listing a plain base after an 'Object'
  class still has that base's '__init__' run, as 'threading.Thread'
  needs, though without arguments, so a base requiring some refuses with
  its own 'TypeError'. Every 'Object' has 'directory', the folder of the file defining
  its class. Source: the 'Object' docstring and the docstrings of its
  three access methods and '__init__', and the 1.1.0 changelog entry "A
  base listed after an Object class is initialized".
  """

  def test_shared_and_read_only(self) -> None:
    class Setting(Object):
      pass

    class Config:
      theme = Setting('dark')

    config, theme = Config(), vars(Config)['theme']
    self.assertIs(config.theme, theme)
    self.assertIs(Config().theme, theme)
    with self.assertRaises(ReadOnlyError) as context:
      config.theme = 'light'
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, config)
    self.assertIs(e.desc, theme)
    self.assertEqual(e.newVal, 'light')
    with self.assertRaises(ProtectedError) as context:
      del config.theme
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, config)
    self.assertIs(e.desc, theme)
    #  'oldVal' holds the value only "if known".
    self.assertIn(e.oldVal, (None, theme))

  def test_base_after_object_initialized(self) -> None:
    class Ready:
      def __init__(self) -> None:
        self.ready = True

    class Job(Object, Ready):
      pass

    self.assertTrue(Job().ready)

  def test_base_after_object_gets_no_arguments(self) -> None:
    class Needy:
      def __init__(self, x) -> None:
        self.x = x

    class Job(Object, Needy):
      pass

    with self.assertRaises(TypeError):
      Job(1)

  def test_directory(self) -> None:
    class Plain(Object):
      pass

    here = os.path.dirname(os.path.abspath(__file__))
    self.assertEqual(Plain().directory, here)
