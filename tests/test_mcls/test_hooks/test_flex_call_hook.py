"""
TestFlexCallHook exercises FlexCallHook through real class creation
via worktoy.mcls.BaseObject. The hook is a descriptor declared on the
namespace class behind BaseMeta, so verifying its behaviour means
constructing real BaseObject subclasses and inspecting the resulting
class __dict__ rather than calling postCompilePhase directly.

Each test builds a fresh subclass inside its body and asserts on the
post-construction state of named entries: presence of the
__flex_wrapped__ marker for entries the hook is required to wrap, and
identity preservation for entries it must skip (dunders, already-marked
functions, classmethod/staticmethod descriptors, classes, plain data).
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_mcls.test_hooks import SpaceHookTest
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  TEST CASE   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class TestFlexCallHook(SpaceHookTest):
  """Branch coverage for FlexCallHook via the BaseMeta pipeline.

  Each test constructs a fresh subclass of BaseObject and asserts on
  named entries in its __dict__. The hook is exercised through normal
  class creation, never by direct invocation of postCompilePhase.
  """

  #  _____________________________________________________________________
  #  HELPERS
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  @staticmethod
  def _isWrapped(value: Any) -> bool:
    """True if value carries the __flex_wrapped__ marker."""
    return bool(getattr(value, '__flex_wrapped__', False))

  #  _____________________________________________________________________
  #  WRAPPING APPLIES
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_clean_instance_method_is_wrapped(self) -> None:
    """A plain instance method on a BaseObject subclass is wrapped."""

    class Subject(BaseObject):
      def add(self, a: Any, b: Any) -> Any:
        return a + b

    subject = Subject()
    self.assertEqual(subject.add(69, 420), 420 + 69)
    self.assertTrue(self._isWrapped(Subject.__dict__['add']))

  def test_multiple_methods_all_wrapped(self) -> None:
    """Every clean instance method is wrapped independently."""

    class Subject(BaseObject):
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

  #  _____________________________________________________________________
  #  WRAPPING SKIPPED
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_dunder_method_is_not_wrapped(self) -> None:
    """Dunder methods are skipped by name."""

    class Subject(BaseObject):
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

    class Subject(BaseObject):
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

    class Subject(BaseObject):
      @classmethod
      def make(cls) -> Any:
        return cls

    self.assertIs(Subject.make(), Subject)
    raw = Subject.__dict__['make']
    self.assertIsInstance(raw, classmethod)

  def test_staticmethod_is_not_wrapped(self) -> None:
    """staticmethod descriptors are not FunctionType, hook skips them."""

    class Subject(BaseObject):
      @staticmethod
      def helper(x: Any) -> Any:
        return x

    someObject = object()
    self.assertIs(Subject.helper(someObject), someObject)
    raw = Subject.__dict__['helper']
    self.assertIsInstance(raw, staticmethod)

  def test_class_data_is_not_wrapped(self) -> None:
    """Plain data attributes are unaffected by the hook."""

    class Subject(BaseObject):
      count: int = 42
      label: str = 'subject'

    self.assertEqual(Subject.__dict__['count'], 42)
    self.assertEqual(Subject.__dict__['label'], 'subject')

  def test_nested_class_is_not_wrapped(self) -> None:
    """Class objects in the namespace are left in place."""

    class Outer(BaseObject):
      class Inner:
        pass

    self.assertIs(Outer.__dict__['Inner'], Outer.Inner)
