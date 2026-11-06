"""
TestReservedNames tests 'ReservedNames' from 'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls.space_hooks import ReservedNames, ReservedNamespaceHook
from . import MclsTest


class TestReservedNames(MclsTest):
  """
  'ReservedNames' lists the names Python sets in a class namespace or
  gives a class, for the hook guarding them. The tests pin the two
  routes of the descriptor, the names it lists, and that none of the
  names a body usually binds is among them.
  """

  def test_through_class_gives_descriptor(self) -> None:
    desc = ReservedNamespaceHook.__dict__['reservedNames']
    self.assertIsInstance(desc, ReservedNames)
    self.assertIs(ReservedNamespaceHook.reservedNames, desc)

  def test_through_instance_gives_names(self) -> None:
    names = ReservedNamespaceHook().reservedNames
    self.assertIsInstance(names, tuple)
    self.assertEqual(len(names), 14)
    self.assertEqual(len(set(names)), 14)
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(name.startswith('__'))
        self.assertTrue(name.endswith('__'))

  def test_interpreter_names_listed(self) -> None:
    names = ReservedNamespaceHook().reservedNames
    expected = (
      '__dict__', '__weakref__', '__module__', '__annotations__',
      '__match_args__', '__doc__', '__name__', '__qualname__',
      '__firstlineno__', '__static_attributes__', '__classcell__',
      '__classdictcell__', '__orig_bases__', '__type_params__',
    )
    self.assertEqual(names, expected)

  def test_body_names_not_listed(self) -> None:
    names = ReservedNamespaceHook().reservedNames
    for name in ('__init__', '__slots__', '__class_len__', '__del__'):
      with self.subTest(name=name):
        self.assertNotIn(name, names)

  def test_random_words_not_listed(self) -> None:
    names = ReservedNamespaceHook().reservedNames
    self.randomWord.size = 8
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertNotIn(word, names)
        self.assertNotIn('__%s__' % word, names)
