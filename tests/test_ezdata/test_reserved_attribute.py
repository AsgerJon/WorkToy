"""
TestReservedAttribute subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that an 'EZData' class body may not bind any of the
attributes EZData keeps for itself: '__ez_fields__', '__key_args__',
'__is_frozen__', '__is_ordered__', '__kw_only__' and '__ez_generated__'.
The class body fails at the offending line with 'ReservedAttributeError'
instead of turning the binding into a field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import new_class

from worktoy.ezdata import EZData, EZField, EZSpace
from worktoy.waitaminute.ezdata import ReservedAttributeError

from . import EZTest

_RESERVED = (
  ('__ez_fields__', {'x': None}),
  ('__key_args__', {'frozen': True}),
  ('__is_frozen__', True),
  ('__is_ordered__', True),
  ('__kw_only__', True),
  ('__ez_generated__', frozenset()),
)


class TestReservedAttribute(EZTest):
  """
  TestReservedAttribute provides tests for the refusal of the attributes
  EZData sets itself in the body of an 'EZData' class.
  """

  def test_every_reserved_attribute_refused(self) -> None:
    """
    Testing that binding each reserved attribute raises
    'ReservedAttributeError', naming the attribute and the class.
    """
    for name, value in _RESERVED:
      with self.subTest(name=name):

        def body(namespace: dict) -> None:
          namespace['x'] = EZField[int](0)
          namespace[name] = value

        with self.assertRaises(ReservedAttributeError) as context:
          new_class('Holder', (EZData,), {}, body)
        exception = context.exception
        self.assertEqual(exception.attributeName, name)
        self.assertEqual(exception.space.getClassName(), 'Holder')
        self.assertIn(name, str(exception))
        self.assertIn('Holder', str(exception))
        self.assertEqual(str(exception), repr(exception))

  def test_names_listed_on_space(self) -> None:
    """
    Testing that the refused names are the ones 'EZSpace' lists in
    '__reserved_ez_attributes__'.
    """
    names = (*(name for name, _ in _RESERVED),)
    self.assertEqual(EZSpace.__reserved_ez_attributes__, names)

  def test_message_points_to_class_keywords(self) -> None:
    """
    Testing that the message points to the class keywords, where the
    options of an EZData class are set.
    """
    with self.assertRaises(ReservedAttributeError) as context:
      class Holder(EZData):  # noqa: F841
        x = EZField[int](0)
        __kw_only__ = True
    self.assertIn('kwOnly=True', str(context.exception))

  def test_is_attribute_error(self) -> None:
    """
    Testing that 'ReservedAttributeError' is an 'AttributeError', like
    'ReservedMethodError'.
    """
    with self.assertRaises(AttributeError):
      class Holder(EZData):  # noqa: F841
        __is_frozen__ = True

  def test_refused_at_the_line(self) -> None:
    """
    Testing that the refusal comes at the binding, before the rest of the
    class body runs.
    """
    ran = []
    body = lambda namespace: (
      namespace.__setitem__('__is_ordered__', True), ran.append('after'),
    )
    with self.assertRaises(ReservedAttributeError):
      new_class('Holder', (EZData,), {}, body)
    self.assertEqual(ran, [])

  def test_class_keyword_still_sets_option(self) -> None:
    """
    Testing that the class keyword still sets the option the refused
    attribute names.
    """

    class Holder(EZData, kwOnly=True):
      x = EZField[int](0)

    self.assertTrue(Holder.kwOnly)
    self.assertEqual([f.fieldName for f in Holder.fields], ['x'])
