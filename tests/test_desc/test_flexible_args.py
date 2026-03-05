"""
TestFlexibleArgs tests that the 'BaseDescriptor' system for descriptor
notifiers correctly passes only arguments that the decorated method
accepts, allowing for flexible argument signatures.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, Field
from worktoy.utilities import argsCount, takesKwargs, maybe
from worktoy.waitaminute.control_flow import ControlFlow

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class _SkipDelete(ControlFlow):
  pass


class HamBox(AttriBox):

  def __delete__(self, instance: Any, **kwargs) -> None:
    try:
      AttriBox.__delete__(self, instance, **kwargs)
    except _SkipDelete:
      pass


class Meta(type):
  __latest_instance__ = None
  instance = Field()

  @instance.GET
  def _getInstance(self, ) -> Any:
    return self.__latest_instance__

  def __call__(cls, *args: Any, **kwargs: Any) -> Any:
    self = super().__call__(*args, **kwargs)
    cls.__latest_instance__ = self
    return self


class Foo(metaclass=Meta):
  __latest_args__ = None

  bar = HamBox[int](69)
  latest = Field()

  @bar.preGet
  @bar.preSet
  @bar.preDelete
  def resetLatest(self, ) -> None:
    self.__latest_args__ = None

  @latest.GET
  def _getLatestArgs(self, ) -> Any:
    return self.__latest_args__

  @latest.SET
  def _setLatestArgs(self, *args: Any, **kwargs: Any) -> Any:
    existing = maybe(self.__latest_args__, ())
    self.__latest_args__ = (*existing, *args)

  #  no args
  @staticmethod
  @bar.preGet
  def _noArgsPreGet() -> Any:
    Foo.instance.latest = ()

  @staticmethod
  @bar.onGet
  def _noArgsOnGet() -> Any:
    Foo.instance.latest = ()

  @staticmethod
  @bar.preSet
  def _noArgsPreSet() -> Any:
    Foo.instance.latest = ()

  @staticmethod
  @bar.onSet
  def _noArgsOnSet() -> Any:
    Foo.instance.latest = ()

  @staticmethod
  @bar.preDelete
  def _noArgsPreDelete() -> Any:
    Foo.instance.latest = ()

  @staticmethod
  @bar.onDelete
  def _noArgsOnDelete() -> Any:
    Foo.instance.latest = ()

  #  one arg
  @staticmethod
  @bar.preGet
  def _oneArgPreGet(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  @staticmethod
  @bar.onGet
  def _oneArgOnGet(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  @staticmethod
  @bar.preSet
  def _oneArgPreSet(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  @staticmethod
  @bar.onSet
  def _oneArgOnSet(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  @staticmethod
  @bar.preDelete
  def _oneArgPreDelete(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  @staticmethod
  @bar.onDelete
  def _oneArgOnDelete(instance: Any) -> Any:
    Foo.instance.latest = (instance,)

  #  two args

  @staticmethod
  @bar.preGet
  def _twoArgsPreGet(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value,)

  @staticmethod
  @bar.onGet
  def _twoArgsOnGet(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value)

  @staticmethod
  @bar.preSet
  def _twoArgsPreSet(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value)

  @staticmethod
  @bar.onSet
  def _twoArgsOnSet(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value)

  @staticmethod
  @bar.preDelete
  def _twoArgsPreDelete(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value)

  @staticmethod
  @bar.onDelete
  def _twoArgsOnDelete(instance: Any, value: Any = 'lmao') -> Any:
    Foo.instance.latest = (instance, value,)

  def __str__(self, ) -> str:
    return """Foo object"""

  __repr__ = __str__


class Eggs:
  spam = HamBox[int](420)

  @spam.preDelete
  def _spamPreDelete(self, ) -> None:
    raise _SkipDelete


class TestFlexibleArgs(DescTest):
  """
  TestFlexibleArgs tests that the 'BaseDescriptor' system for descriptor
  notifiers correctly passes only arguments that the decorated method
  accepts, allowing for flexible argument signatures.
  """

  def setUp(self, ) -> None:
    self.foo = Foo()
    self.noArgs = (
      Foo._noArgsPreGet,
      Foo._noArgsOnGet,
      Foo._noArgsPreSet,
      Foo._noArgsOnSet,
      Foo._noArgsPreDelete,
      Foo._noArgsOnDelete,
      )
    self.oneArg = (
      Foo._oneArgPreGet,
      Foo._oneArgOnGet,
      Foo._oneArgPreSet,
      Foo._oneArgOnSet,
      Foo._oneArgPreDelete,
      Foo._oneArgOnDelete,
      )
    self.twoArgs = (
      Foo._twoArgsPreGet,
      Foo._twoArgsOnGet,
      Foo._twoArgsPreSet,
      Foo._twoArgsOnSet,
      Foo._twoArgsPreDelete,
      Foo._twoArgsOnDelete,
      )

  def test_dev_null(self, ) -> None:
    self.assertTrue(True)
    self.assertEqual(str(Foo()), """Foo object""")

  def test_get(self, ) -> None:
    self.assertFalse(self.foo.latest)
    self.assertEqual(self.foo.bar, 69)  # triggers preGet and onGet
    self.assertEqual(len(self.foo.latest), 6)
    for recent in self.foo.latest:
      if any(recent):
        self.assertIs(recent[0], self.foo)
      if len(recent) > 1:
        self.assertIn(recent[1], (69, 420, 'lmao'))

  def test_set(self, ) -> None:
    self.assertFalse(self.foo.latest)
    self.foo.bar = 420  # triggers preSet and onSet
    self.assertEqual(len(self.foo.latest), 6)
    for recent in self.foo.latest:
      if any(recent):
        self.assertIs(recent[0], self.foo)
      if len(recent) > 1:
        self.assertIn(recent[1], (69, 420, 'lmao'))

  def test_delete(self, ) -> None:
    self.assertFalse(self.foo.latest)
    del self.foo.bar  # triggers preDelete and onDelete
    self.assertEqual(len(self.foo.latest), 6)
    for recent in self.foo.latest:
      if any(recent):
        self.assertIs(recent[0], self.foo)
      if len(recent) > 1:
        self.assertIn(recent[1], (69, 420, 'lmao'))

  def test_skip_delete(self, ) -> None:
    eggs = Eggs()
    self.assertEqual(eggs.spam, 420)
    del eggs.spam  # should be ignored due to _SkipDelete
    self.assertEqual(eggs.spam, 420)
