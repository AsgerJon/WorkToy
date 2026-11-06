"""
TestClassBodyTemplate tests 'ClassBodyTemplate' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import ClassBodyTemplate
from worktoy.utilities._class_body_template import _SomeClass
from . import UtilitiesTest


class TestClassBodyTemplate(UtilitiesTest):
  """
  'ClassBodyTemplate' is the string of section banners the author pastes
  into a new class file, and '_SomeClass' the same banners in an empty
  class. The tests pin that the string carries every banner the library
  uses, in the order the files use them, and that the reference class
  is empty apart from its docstring.
  """

  banners = (
    'STATIC METHODS',
    'NAMESPACE',
    'GETTERS',
    'SETTERS',
    'NOTIFIERS',
    'Python API',
    'CONSTRUCTORS',
    'DOMAIN SPECIFIC',
    'OPTIONAL METHODS',
    'REQUIRED METHODS',
    'PARENT METHODS',
    'PUBLIC METHODS',
  )

  def test_is_string(self) -> None:
    self.assertIsInstance(ClassBodyTemplate, str)

  def test_banners_in_order(self) -> None:
    positions = [ClassBodyTemplate.index(banner) for banner in self.banners]
    self.assertEqual(positions, sorted(positions))

  def test_variable_groups(self) -> None:
    groups = ('Class', 'Fallback', 'Private', 'Public', 'Virtual')
    for group in groups:
      with self.subTest(group=group):
        self.assertIn('#  %s Variables' % group, ClassBodyTemplate)

  def test_reference_class_is_empty(self) -> None:
    names = [n for n in vars(_SomeClass) if not n.startswith('__')]
    self.assertEqual(names, [])
    self.assertIn('section banners', _SomeClass.__doc__)
