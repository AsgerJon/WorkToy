"""Test of GuardClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from unittest import TestCase

import unittest
from worktoy.worktoyclass import WorkToyClass


class TestDefaultClass(unittest.TestCase):

  def setUp(self):
    self.default = WorkToyClass()

  def test_monoSpace_with_default_newline(self):
    text = 'Hello   World'
    result = self.default.monoSpace(text)
    self.assertEqual(result, 'Hello World')

  def test_monoSpace_with_custom_newline(self):
    text = 'Hello<br>World'
    result = self.default.monoSpace(text, '<br>')
    self.assertEqual(result, 'Hello\nWorld')

  def test_stringList_with_default_separator(self):
    result = self.default.stringList("""one, two, three, four""")
    self.assertEqual(result, ['one', 'two', 'three', 'four'])

  def test_stringList_with_custom_separator(self):
    result = self.default.stringList('one | two | three | four',
                                     separator=' | ')
    self.assertEqual(result, ['one', 'two', 'three', 'four'])

  def test_justify(self):
    text = self.default.monoSpace("""This is a long text that needs to be 
      justified to fit within a certain character limit.""")
    text = self.default.monoSpace(text)
    result = self.default.justify(text, 50)
    expect = self.default.monoSpace("""This is a long text that needs to 
      be justified<br>to fit within a certain character limit.""")
    self.assertEqual(result, expect)

  def test_extractBetween(self):
    text = 'a(b(c)d)e'
    result = self.default.extractBetween(text, '(', ')')
    self.assertEqual(result, ['b(c'])

  def test_trimWhitespace(self):
    text = '  Some text with leading and trailing spaces   '
    result = self.default.trimWhitespace(text)
    self.assertEqual(result, 'Some text with leading and trailing spaces')

  def test_typeName_with_type(self):
    result = self.default.typeName(str)
    self.assertEqual(result, 'str')


if __name__ == '__main__':
  unittest.main()
