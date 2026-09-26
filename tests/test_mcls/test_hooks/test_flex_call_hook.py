"""
TestFlexCallHook exercises FlexCallHook through real class creation. No
namespace carries the hook by default, so each test builds a namespace
that declares it, a metaclass whose '__prepare__' returns that namespace,
and a base class built by that metaclass. The tests then construct real
subclasses of that base and inspect the resulting class __dict__ rather
than calling postCompilePhase directly.

The tests assert the presence of the __flex_wrapped__ marker for entries
the hook is required to wrap, and identity preservation for entries it
must skip (dunders, already-marked functions, classmethod/staticmethod
descriptors, classes, plain data). Two tests check what opting in buys:
wrapped methods drop surplus positional arguments and still take
keywords for their positional parameters.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_mcls.test_hooks import SpaceHookTest
from worktoy.mcls import BaseObject, BaseMeta, BaseSpace
from worktoy.mcls.space_hooks import FlexCallHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  TEST CASE   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TestFlexCallHook(SpaceHookTest):
  """Branch coverage for FlexCallHook on a namespace that opts in.

  Each test constructs a fresh subclass of a base built on such a
  namespace and asserts on named entries in its __dict__. The hook is
  exercised through normal class creation, never by direct invocation of
  postCompilePhase.
  """

  #  _____________________________________________________________________
  #  HELPERS
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  @staticmethod
  def _isWrapped(value: Any) -> bool:
    """True if value carries the __flex_wrapped__ marker."""
    return bool(getattr(value, '__flex_wrapped__', False))

  @staticmethod
  def _buildFlexBase() -> type:
    """Builds a 'BaseObject' subclass whose metaclass prepares a
    namespace declaring 'FlexCallHook' under its natural name."""

    class FlexSpace(BaseSpace):
      flexCallHook = FlexCallHook()

    class FlexMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> Any:
        return FlexSpace(mcls, name, bases, **kwargs)

    class FlexObject(BaseObject, metaclass=FlexMeta):
      pass

    return FlexObject

  #  _____________________________________________________________________
  #  WRAPPING APPLIES
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_clean_instance_method_is_wrapped(self) -> None:
    """A plain instance method on an opted-in class is wrapped."""

    class Subject(self._buildFlexBase()):
      def add(self, a: Any, b: Any) -> Any:
        return a + b

    subject = Subject()
    self.assertEqual(subject.add(69, 420), 420 + 69)
    self.assertTrue(self._isWrapped(Subject.__dict__['add']))

  def test_multiple_methods_all_wrapped(self) -> None:
    """Every clean instance method is wrapped independently."""

    class Subject(self._buildFlexBase()):
      def add(self, a: Any, b: Any) -> Any:
        return a + b

      def sub(self, a: Any, b: Any) -> Any:
        return a - b

      def mul(self, a: Any, b: Any) -> Any:
        return a * b

    subject = Subject()
    self.assertEqual(subject.add(69, 420), 420 + 69)
    self.assertEqual(subject.sub(69, 420), 69 - 420)
    self.assertEqual(subject.mul(69, 420), 69 * 420)
    self.assertTrue(self._isWrapped(Subject.__dict__['add']))
    self.assertTrue(self._isWrapped(Subject.__dict__['sub']))
    self.assertTrue(self._isWrapped(Subject.__dict__['mul']))

  def test_wrapped_method_drops_surplus(self) -> None:
    """A wrapped method drops positional arguments beyond those it
    declares, which is what opting in to the hook is for."""

    class Subject(self._buildFlexBase()):
      def add(self, a: Any, b: Any) -> Any:
        return a + b

    self.assertEqual(Subject().add(69, 420, 1337), 420 + 69)

  def test_wrapped_method_takes_keywords(self) -> None:
    """A wrapped method still receives its positional parameters by
    keyword."""

    class Subject(self._buildFlexBase()):
      def add(self, a: Any, b: Any) -> Any:
        return a + b

    self.assertEqual(Subject().add(69, b=420), 420 + 69)
    self.assertEqual(Subject().add(a=69, b=420), 420 + 69)

  #  _____________________________________________________________________
  #  WRAPPING SKIPPED
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_dunder_method_is_not_wrapped(self) -> None:
    """Dunder methods are skipped by name."""

    class Subject(self._buildFlexBase()):
      def __str__(self) -> str:
        return 'Never gonna give you up'

    subject = Subject()
    self.assertEqual(str(subject), 'Never gonna give you up')
    self.assertFalse(self._isWrapped(Subject.__dict__['__str__']))

  def test_already_wrapped_function_is_not_re_wrapped(self) -> None:
    """A function with __flex_wrapped__ already set is preserved.

    Identity must be preserved exactly. Re-wrapping would substitute a
    new wrapper object even though the marker check is supposed to
    short-circuit before flexCall is invoked.
    """

    def preWrapped(self_: Any, x: Any) -> Any:
      return x

    preWrapped.__flex_wrapped__ = True

    class Subject(self._buildFlexBase()):
      method = preWrapped

    subject = Subject()
    self.assertEqual(subject.method(69), 69)
    self.assertIs(Subject.__dict__['method'], preWrapped)

  #  _____________________________________________________________________
  #  NON-FUNCTION ENTRIES PASS THROUGH
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_classmethod_is_not_wrapped(self) -> None:
    """classmethod descriptors are not FunctionType, hook skips them.

    The descriptor type is established by Python before the value
    reaches the namespace dict, so the hook's isinstance guard alone
    is sufficient. Verified by direct probe of CPython behaviour.
    """

    class Subject(self._buildFlexBase()):
      @classmethod
      def make(cls) -> Any:
        return cls

    self.assertIs(Subject.make(), Subject)
    raw = Subject.__dict__['make']
    self.assertIsInstance(raw, classmethod)

  def test_staticmethod_is_not_wrapped(self) -> None:
    """staticmethod descriptors are not FunctionType, hook skips them."""

    class Subject(self._buildFlexBase()):
      @staticmethod
      def helper(x: Any) -> Any:
        return x

    someObject = object()
    self.assertIs(Subject.helper(someObject), someObject)
    raw = Subject.__dict__['helper']
    self.assertIsInstance(raw, staticmethod)

  def test_class_data_is_not_wrapped(self) -> None:
    """Plain data attributes are unaffected by the hook."""

    class Subject(self._buildFlexBase()):
      count: int = 42
      label: str = 'subject'

    self.assertEqual(Subject.__dict__['count'], 42)
    self.assertEqual(Subject.__dict__['label'], 'subject')

  def test_nested_class_is_not_wrapped(self) -> None:
    """Class objects in the namespace are left in place."""

    class Outer(self._buildFlexBase()):
      class Inner:
        pass

    self.assertIs(Outer.__dict__['Inner'], Outer.Inner)
