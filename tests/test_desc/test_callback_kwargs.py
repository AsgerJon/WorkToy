"""
TestCallbackKwargs tests that the 'BaseDescriptor' correctly passes kwargs
on to decorated callbacks that expect them by inclusion of '**kwargs'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.waitaminute.control_flow import ControlFlow, SkipSet

from . import DescTest


class _SkipDelete(ControlFlow):
  pass


class HamBox(AttriBox):

  def __delete__(self, instance: Any, **kwargs) -> None:
    try:
      AttriBox.__delete__(self, instance, **kwargs)
    except _SkipDelete:
      pass


if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Union

  IntBox: TypeAlias = Union[int, AttriBox]


class Foo:
  bar: IntBox = HamBox[int](69)
  ham: IntBox = HamBox[int](420)

  @bar.preGet
  @ham.preGet
  @bar.onGet
  @bar.onSet
  def _preCallbacks(self, **kwargs) -> None:
    pass

  @ham.preSet
  def _hamPreSet(self, value: Any, **kwargs) -> None:
    if value == self.ham:
      raise SkipSet

  @bar.preSet
  def _barPreSet(self, value: Any, **kwargs) -> None:
    if value == self.bar:
      raise SkipSet

  @bar.preDelete
  def _preDeleteBar(self, **kwargs) -> None:
    raise _SkipDelete

  @ham.preDelete
  def _preDeleteHam(self, **kwargs) -> None:
    pass

  @ham.onDelete
  def _onDeleteHam(self, **kwargs) -> None:
    pass


class TestCallbackKwargs(DescTest):

  def setUp(self) -> None:
    super().setUp()

  def test_pre_callbacks(self, ) -> None:
    foo = Foo()
    self.assertEqual(foo.bar, 69)
    foo.bar = 69  # should skip.
    self.assertEqual(foo.ham, 420)
    foo.ham = 420  # should skip.
    foo.bar = 420
    foo.ham = 69
    self.assertEqual(foo.bar, 420)
    del foo.bar
    del foo.ham
    with self.assertRaises(AttributeError):
      _ = foo.ham
    self.assertEqual(foo.bar, 420)  # del skipped.
