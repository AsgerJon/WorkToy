"""
RefusedObjectInClassBody holds the refusals that belong with
'design.promises.core.promise_object_in_class_body'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class RefusedObjectInClassBody(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Writing an 'Object' of a class body through an instance raises
  'ReadOnlyError' and deleting it raises 'ProtectedError', both
  'AttributeError's. A plain base listed after an 'Object' class is
  initialized without arguments, so one requiring some refuses with its own
  'TypeError'. Source: the 'Object' docstring and the docstrings of its three
  access methods and '__init__', and the 1.1.0 changelog entry "A base listed
  after an Object class is initialized".
  """

  def test_shared_and_read_only_1(self) -> None:
    class Setting(Object):
      pass

    class Config:
      theme = Setting('dark')

    config, theme = Config(), vars(Config)['theme']
    with self.assertRaises(Exception) as refused:
      config.theme = 'light'
    self.assertIsInstance(refused.exception, ReadOnlyError)

  def test_shared_and_read_only_2(self) -> None:
    class Setting(Object):
      pass

    class Config:
      theme = Setting('dark')

    config, theme = Config(), vars(Config)['theme']
    with self.assertRaises(Exception) as refused:
      del config.theme
    self.assertIsInstance(refused.exception, ProtectedError)

  def test_base_after_object_gets_no_arguments(self) -> None:
    class Needy:
      def __init__(self, x) -> None:
        self.x = x

    class Job(Object, Needy):
      pass

    with self.assertRaises(Exception) as refused:
      Job(1)
    self.assertIsInstance(refused.exception, TypeError)
