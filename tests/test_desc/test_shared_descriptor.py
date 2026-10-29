"""
TestSharedDescriptor subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a descriptor based on 'BaseDescriptor' is placed
once: one object bound in the bodies of two classes, at the same name or
another, is refused with 'SharedDescriptor' as the second class is
created, and the first class keeps the descriptor as it placed it. Before,
the second class took the box over, and the values built for the first
class named the second as their owner. A descriptor bound to two names in
one class body, a box or a 'Field', places a clone at the second name
instead (see 'test_box_two_names'); 'BaseDescriptor.__set_name__' decides
both cases.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from traceback import format_exception_only
from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.waitaminute.desc import SharedDescriptor

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Point(BaseObject):
  """Point is the field type of the boxes below."""


class TestSharedDescriptor(DescTest):
  """
  TestSharedDescriptor provides tests for a descriptor placed a second
  time.
  """

  def _unwrap(self, exception: BaseException) -> Any:
    """
    On Python 3.7 through 3.11 the interpreter wraps an exception raised
    from '__set_name__' in a 'RuntimeError', with the original on
    '__cause__'; from Python 3.12 onward it propagates unchanged. This
    returns the 'SharedDescriptor' either way.
    """
    if isinstance(exception, SharedDescriptor):
      return exception
    return exception.__cause__  # pragma: no cover (Python < 3.12)

  def test_box_in_two_classes(self) -> None:
    """One box bound in two class bodies at one name is refused at the
    second, naming both places."""
    shared = AttriBox[Point]()

    class A(BaseObject):
      p = shared

    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class B(BaseObject):
        p = shared
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, SharedDescriptor)
    self.assertIs(e.desc, shared)
    self.assertIs(e.owner, A)
    self.assertEqual(e.fieldName, 'p')
    self.assertEqual(e.newOwner.__name__, 'B')
    self.assertEqual(e.newName, 'p')

  def test_box_in_two_classes_other_name(self) -> None:
    """At another name in the second class the box is refused as well;
    only a second name in the same class body takes a clone."""
    shared = AttriBox[Point]()

    class A(BaseObject):
      p = shared

    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class B(BaseObject):
        q = shared
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, SharedDescriptor)
    self.assertEqual((e.fieldName, e.newName), ('p', 'q'))

  def test_first_class_keeps_its_box(self) -> None:
    """The refused class leaves the box as the first class placed it, and
    the values it builds name that class."""
    shared = AttriBox[Point]()

    class A(BaseObject):
      p = shared

    with self.assertRaises((SharedDescriptor, RuntimeError)):
      class B(BaseObject):
        p = shared
    self.assertIs(shared.getFieldOwner(), A)
    self.assertEqual(shared.getFieldName(), 'p')
    self.assertIs(A().p.__field_owner__, A)

  def test_classes_from_one_namespace(self) -> None:
    """Two classes built from one dict of boxes by calling the metaclass
    are refused at the second."""
    spec = {'p': AttriBox[Point]()}
    BaseMeta('E', (BaseObject,), dict(spec))
    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      BaseMeta('F', (BaseObject,), dict(spec))
    self.assertIsInstance(self._unwrap(context.exception), SharedDescriptor)

  def test_field_in_two_classes(self) -> None:
    """A 'Field' bound in two class bodies is refused at the second."""
    shared = Field()

    class A(BaseObject):
      f = shared

    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class B(BaseObject):
        f = shared
    self.assertIsInstance(self._unwrap(context.exception), SharedDescriptor)

  def test_field_bound_to_two_names(self) -> None:
    """A 'Field' bound to two names in one class body places a clone at
    the second name, as a box does: two objects, each recording its own
    name, both with the accessors the class body registered."""

    class A(BaseObject):
      f = g = Field()

      @f.GET
      def _getValue(self) -> int:
        return 42

    first, second = A.__dict__['f'], A.__dict__['g']
    self.assertIsNot(first, second)
    self.assertIs(type(second), Field)
    self.assertEqual(first.getFieldName(), 'f')
    self.assertEqual(second.getFieldName(), 'g')
    self.assertIs(second.getFieldOwner(), A)
    self.assertEqual((A().f, A().g), (42, 42))

  def test_message_shown(self) -> None:
    """The message names both places, and a traceback shows it, as for
    the other refusals of a class-body line. From Python 3.12 the
    interpreter adds a note naming the '__set_name__' call, which the
    traceback prints after the message."""
    shared = AttriBox[Point]()

    class A(BaseObject):
      p = shared

    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class B(BaseObject):
        p = shared
    e = self._unwrap(context.exception)
    self.assertIn("'A.p'", str(e))
    self.assertIn("'B.p'", str(e))
    self.assertEqual(e.msg, str(e))
    shown = ''.join(format_exception_only(type(e), e))
    self.assertIn(str(e), shown)
    self.assertNotIn('<no detail available>', shown)
