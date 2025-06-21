"""
TestTypeSig tests the TypeSig class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from worktoy.static import TypeSig
from worktoy.waitaminute import HashMismatch, CastMismatch, FlexMismatch

from typing import TYPE_CHECKING


class TestTypeSig(TestCase):
  """
  Unit tests for TypeSig: fast, cast, flex.
  """

  def testFastExactMatch(self) -> None:
    sig = TypeSig(int, str)
    args = (5, 'hello')
    result = sig.fast(*args)
    self.assertEqual(result, args)

  def testFastHashMismatch(self) -> None:
    sig = TypeSig(int, str)
    args = ('oops', 5)
    with self.assertRaises(HashMismatch):
      sig.fast(*args)
    with self.assertRaises(CastMismatch):
      sig.cast(*args)
    flexed = sig.flex(*args)
    self.assertEqual(flexed, (5, 'oops',))

  def testCastSuccess(self) -> None:
    sig = TypeSig(int, float)
    args = ('69', '.80085')
    result = sig.cast(*args)
    with self.assertRaises(HashMismatch):
      sig.fast(*args)
    result = sig.cast(*args)
    self.assertEqual(result, (69, 0.80085))

  def testCastMismatch(self) -> None:
    sig = TypeSig(int, float)
    args = ('oops', 'still bad')
    with self.assertRaises(HashMismatch):
      sig.fast(*args)
    with self.assertRaises(CastMismatch):
      sig.cast(*args)
    with self.assertRaises(FlexMismatch):
      sig.flex(*args)

  def testFlex(self) -> None:
    sig = TypeSig(str, int)
    args = (123, 'hello')
    result = sig.flex(*args)
    self.assertEqual(result, ('hello', 123))

  def testFlexRepeatedTypes(self) -> None:
    sig = TypeSig(float, float)
    args = ('0.80085', 420)
    result = sig.flex(*args)
    self.assertEqual(result, (0.80085, 420))

  def testFlexFailure(self) -> None:
    sig = TypeSig(int, float)
    args = ('nope', 'fail')
    with self.assertRaises(HashMismatch):
      sig.fast(*args)
    with self.assertRaises(CastMismatch):
      sig.cast(*args)
    with self.assertRaises(FlexMismatch):
      sig.flex(*args)
