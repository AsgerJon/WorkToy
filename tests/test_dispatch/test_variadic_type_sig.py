"""
TestVariadicTypeSig subclasses 'DispatcherTest' and pins the string
representations of a 'TypeSig' ending in an 'ARGS' sentinel. Such a
signature carries an 'ARGS' instance as its last entry rather than a
class, and it renders that entry the way the signature is written in an
'@overload' declaration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import TypeSig
from . import DispatcherTest


class TestVariadicTypeSig(DispatcherTest):
  """
  TestVariadicTypeSig pins 'str' and 'repr' of variadic signatures, both
  with and without a fixed prefix.
  """

  def test_str_with_prefix(self) -> None:
    """
    Testing that 'str' renders the variadic entry as 'ARGS[int]' after
    the prefix types.
    """
    sig = TypeSig(int, ARGS[int])
    self.assertEqual(str(sig), '<TypeSig: [int, ARGS[int]]>')

  def test_repr_with_prefix(self) -> None:
    """
    Testing that 'repr' renders the variadic entry the same way, inside
    the constructor form of the signature.
    """
    sig = TypeSig(int, ARGS[int])
    self.assertEqual(repr(sig), 'TypeSig(int, ARGS[int])')

  def test_variadic_only(self) -> None:
    """
    Testing both representations of a signature that consists of the
    variadic entry alone.
    """
    sig = TypeSig(ARGS[str])
    self.assertEqual(str(sig), '<TypeSig: [ARGS[str]]>')
    self.assertEqual(repr(sig), 'TypeSig(ARGS[str])')
