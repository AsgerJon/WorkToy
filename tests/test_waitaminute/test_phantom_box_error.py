"""
TestPhantomBoxError tests the custom exception class 'PhantomBoxError'
from the 'worktoy.waitaminute.desc' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import List

from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import PhantomBoxError
from . import WaitAMinuteTest


class Parametrized:
  """
  Parametrized stands in for a parametrized generic that is also a
  'type'.

  Python 3.9 and 3.10 answer 'True' to 'isinstance(list[int], type)',
  and the builtin generic forwards '__name__' to its origin, so asking
  it for a name quietly answers 'list' and loses the argument. From 3.11
  the isinstance answer became 'False' and the two spellings stopped
  diverging, which leaves the real case untestable on a current
  interpreter. This class reproduces the shape directly: it is a genuine
  class carrying an '__origin__', so it exercises the discriminator on
  every version the library supports rather than on two of them.
  """

  __origin__ = list


class TestPhantomBoxError(WaitAMinuteTest):
  """
  TestPhantomBoxError tests the custom exception class 'PhantomBoxError'
  from the 'worktoy.waitaminute.desc' package.
  """

  def test_render_plain_type(self) -> None:
    """
    Testing that a plain class renders as its bare name, which is the
    spelling the declaration used.
    """
    self.assertEqual(PhantomBoxError._renderArg(int), 'int')
    self.assertEqual(PhantomBoxError._renderArg(float), 'float')

  def test_render_alias_keeps_argument(self) -> None:
    """
    Testing that a parametrized generic renders with its argument
    intact, rather than collapsing to the origin.
    """
    rendered = PhantomBoxError._renderArg(List[int])
    self.assertIn('int', rendered)
    self.assertNotEqual(rendered, 'List')
    self.assertNotEqual(rendered, 'list')

  def test_origin_outranks_isinstance(self) -> None:
    """
    Testing that the presence of '__origin__' decides the rendering, not
    'isinstance(arg, type)'.

    'Parametrized' satisfies both tests at once, so the two orderings
    disagree about it: sorting on '__origin__' falls through to the
    'typing' rendering, while sorting on 'isinstance' first would take
    the bare-name branch and report the class name. Pinning the former
    keeps the ordering from being flipped back.
    """
    rendered = PhantomBoxError._renderArg(Parametrized)
    self.assertEqual(rendered, str(Parametrized))
    self.assertNotEqual(rendered, Parametrized.__name__)

  def test_render_builtin_generic(self) -> None:
    """
    Testing the real case behind 'test_origin_outranks_isinstance' on
    the versions that can spell it. The builtin generic is only
    subscriptable from Python 3.9, so older interpreters skip this and
    rely on the stand-in.
    """
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    rendered = PhantomBoxError._renderArg(list[int])
    self.assertIn('int', rendered)
    self.assertNotEqual(rendered, 'list')

  def test_message_names_binding_and_owner(self) -> None:
    """
    Testing that the rendered message reports the attribute name, the
    owning class, and the subscript as written, since those three are
    what point at the offending declaration.
    """
    alias = AttriBox[List[int]]
    error = PhantomBoxError(alias, Parametrized, 'derp')
    message = str(error)
    self.assertIn('derp', message)
    self.assertIn('Parametrized', message)
    self.assertIn('int', message)
    self.assertIn('AttriBox', message)

  def test_message_without_owner_or_name(self) -> None:
    """
    Testing that the message stays well formed when the raising context
    supplied neither a binding nor an owner, which is the case for an
    alias installed on a finished class by 'setattr'.
    """
    alias = AttriBox[List[int]]
    error = PhantomBoxError(alias)
    message = str(error)
    self.assertIsNone(error.owner)
    self.assertIsNone(error.fieldName)
    self.assertIn('AttriBox', message)
    self.assertNotIn('None', message)

  def test_repr_matches_str(self) -> None:
    """
    Testing that the exception renders identically either way, following
    the convention the other exceptions in the package keep.
    """
    error = PhantomBoxError(AttriBox[List[int]], Parametrized, 'derp')
    self.assertEqual(repr(error), str(error))
