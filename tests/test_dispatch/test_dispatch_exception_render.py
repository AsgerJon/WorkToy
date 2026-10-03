"""
TestDispatchExceptionRender subclasses 'DispatcherTest' from the
'tests.test_dispatch' package and pins that a 'DispatchException' renders
its message for a 'Dispatcher' without concrete signatures, as one holding
only a finalizer. The message used to iterate the raw storage of the
signatures, which is 'None' until the first signature is registered, so
'str()' raised 'TypeError' and tracebacks showed '<exception str()
failed>'. The exception now reads the signatures through
'Dispatcher._getSigFuncList', which gives an empty list in that case.

A variadic declaration such as '@overload(int, ARGS[str])' is one
registration, listed as the class body declared it. It used to be
registered as six concrete expansions for short calls beside the variadic
signature itself, and the message listed the expansions and never the
declaration; no such expansion exists any more.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import TypeSig, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import DispatcherTest


class Finished(BaseObject):
  """Finished declares a name with a finalizer and nothing else."""

  __finalized__ = 0

  @overload.finalize
  def bar(self, *args) -> None:
    type(self).__finalized__ += 1


class Plain(BaseObject):
  """Plain declares an ordinary overload."""

  @overload(int)
  def bar(self, value: int) -> int:
    return value


class Tail(BaseObject):
  """Tail declares a variadic overload beside two explicit ones, one of
  which the variadic accepts as well."""

  @overload(int, ARGS[str])
  def bar(self, *args) -> str:
    return 'tail'

  @overload(int)
  def bar(self, value: int) -> str:
    return 'int'

  @overload(float)
  def bar(self, value: float) -> str:
    return 'float'


def _listing(exception: DispatchException) -> str:
  """The part of the message after 'available signatures:'."""
  return str(exception).split('available signatures:')[-1]


class TestDispatchExceptionRender(DispatcherTest):
  """
  TestDispatchExceptionRender provides tests for the message of a
  'DispatchException'.
  """

  def test_finalizer_only_renders(self) -> None:
    """A call on a finalizer-only name raises a 'DispatchException' whose
    message renders, naming the method and listing no signature."""
    with self.assertRaises(DispatchException) as context:
      Finished().bar(1)
    info = str(context.exception)
    self.assertIn("'Finished.bar'", info)
    self.assertIn('available signatures:', info)
    self.assertNotIn('TypeSig', info.split('available signatures:')[-1])

  def test_finalizer_still_runs(self) -> None:
    """The finalizer runs although no signature matched."""
    before = Finished.__finalized__
    with self.assertRaises(DispatchException):
      Finished().bar(1)
    self.assertEqual(Finished.__finalized__, before + 1)

  def test_signatures_listed(self) -> None:
    """A 'Dispatcher' with signatures still lists them."""
    self.assertEqual(Plain().bar(3), 3)
    with self.assertRaises(DispatchException) as context:
      Plain().bar('x', 'y')
    info = str(context.exception)
    self.assertIn(str(TypeSig(int)), info.split('available signatures:')[-1])

  def test_variadic_declaration_listed(self) -> None:
    """The variadic signature appears as declared."""
    self.assertEqual(Tail().bar(1, 'a', 'b'), 'tail')
    with self.assertRaises(DispatchException) as context:
      Tail().bar('x')
    self.assertIn(str(TypeSig(int, ARGS[str])), _listing(context.exception))

  def test_expansions_not_listed(self) -> None:
    """None of the concrete signatures the variadic accepts appear, since
    the class body declared none of them."""
    with self.assertRaises(DispatchException) as context:
      Tail().bar('x')
    listing = _listing(context.exception)
    for n in range(1, 7):
      with self.subTest(n=n):
        self.assertNotIn(str(TypeSig(int, *[str] * n)), listing)

  def test_explicit_declarations_listed(self) -> None:
    """The explicit declarations appear, the one the variadic accepts as
    well included."""
    self.assertEqual(Tail().bar(1), 'int')
    self.assertEqual(Tail().bar(1.5), 'float')
    with self.assertRaises(DispatchException) as context:
      Tail().bar('x')
    listing = _listing(context.exception)
    self.assertIn(str(TypeSig(int)), listing)
    self.assertIn(str(TypeSig(float)), listing)
