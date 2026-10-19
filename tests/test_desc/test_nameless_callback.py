"""
TestNamelessCallback subclasses 'DescTest' and pins that the callback
decorators of 'BaseDescriptor' and the accessor decorators of 'Field'
refuse a function without a name of its own, a lambda or a callable
with no '__name__', with 'NamelessCallback' at the decorator. The hooks
look each callback up by name on the class of the instance, so a lambda
could never be found, and the first access used to fail with
'MissingVariable' naming '<lambda>'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from functools import partial

from worktoy.desc import AttriBox, BaseDescriptor, Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import NamelessCallback

from . import DescTest


def _named(self, *args) -> None:
  pass  # pragma: no cover


class TestNamelessCallback(DescTest):
  """
  TestNamelessCallback provides tests for the refusal of nameless
  callbacks.
  """

  def test_notification_decorators_refuse_lambda(self) -> None:
    """Each notification decorator refuses a lambda, naming the role."""
    box = AttriBox[int](0)
    roles = (
      'preGet', 'onGet', 'preSet', 'onSet', 'preDelete', 'onDelete',
      'setName',
    )
    for role in roles:
      with self.subTest(role=role):
        decorator = getattr(box, role)
        with self.assertRaises(NamelessCallback) as context:
          decorator(lambda self, *args: None)
        e = context.exception
        self.assertEqual(e.role, role)
        self.assertIs(e.desc, box)
        self.assertIn(role, str(e))
        self.assertEqual(str(e), repr(e))
        self.assertIsInstance(e, SyntaxError)

  def test_accessor_decorators_refuse_lambda(self) -> None:
    """'Field.GET', 'Field.SET' and 'Field.DELETE' refuse a lambda."""
    field = Field()
    for role in ('GET', 'SET', 'DELETE'):
      with self.subTest(role=role):
        with self.assertRaises(NamelessCallback) as context:
          getattr(field, role)(lambda self, *args: None)
        self.assertEqual(context.exception.role, role)

  def test_callable_without_name_refused(self) -> None:
    """A callable with no '__name__', such as a 'partial', is refused
    too."""
    box = AttriBox[int](0)
    with self.assertRaises(NamelessCallback):
      box.onSet(partial(_named))

  def test_nothing_recorded(self) -> None:
    """A refused callback leaves no key behind."""
    box = AttriBox[int](0)
    with self.assertRaises(NamelessCallback):
      box.onSet(lambda self, value: None)
    self.assertEqual(box._getOnSetKeys(), ())

  def test_named_function_accepted(self) -> None:
    """A function defined with 'def' is accepted and fires."""

    class Owner(BaseObject):
      x = AttriBox[int](0)
      seen = None

      @x.onSet
      def _onSet(self, value: int) -> None:
        Owner.seen = value

    owner = Owner()
    owner.x = 7
    self.assertEqual(Owner.seen, 7)

  def test_class_body_lambda_refused(self) -> None:
    """A lambda bound in a class body through a decorator call is refused
    as the body runs."""
    with self.assertRaises(NamelessCallback):
      class Owner(BaseObject):
        x = AttriBox[int](0)
        cb = x.onSet(lambda self, value: None)
