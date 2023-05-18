"""Unit tests for the textBetween function."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn
from unittest import TestCase

from loremify import lorem

from worktoy import textBetween


class TextBetweenTestCase(TestCase):
  """Unit tests for the textBetween function."""

  def setUp(self) -> NoReturn:
    """Sets up the classes"""
    self.sample = """This is a <b>test</b> for bold fonts! <p>and this is 
    a paragraph</p>. This should not found. <b>bla</b>___"""

  def testSimple(self) -> NoReturn:
    """Testing simple case"""
    prediction = ['test', 'bla']
    reality = textBetween(self.sample, '<b>', '</b>')
    self.assertEqual(prediction, reality)
