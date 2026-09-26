"""
TestFieldStorage subclasses 'EZTest' from the 'tests.test_ezdata' package
and pins where an 'EZData' instance keeps its field values: in its own
'__dict__' under the field name, with no '__slots__' and, for a field
that clashes with nothing, no class attribute at all. Python lets a data
descriptor anywhere in the method resolution order take precedence over
the instance '__dict__', so a field sharing its name with one, such as
'Object.directory' or a property on a mixin, receives an 'EZStore' that
reads and writes the dict itself. A plain class attribute of the same
name yields to the dict anyway, but must not keep the field from
receiving its default.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField, EZStore
from worktoy.waitaminute import MissingVariable

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class PropertyMixin:
  """PropertyMixin declares 'value' as a read-only property."""

  @property
  def value(self) -> str:
    return 'property'


class DeleteOnly:
  """DeleteOnly is a descriptor defining '__get__' and '__delete__' but
  no '__set__', which still makes it a data descriptor to Python."""

  def __get__(self, instance: Any, owner: type) -> str:
    return 'descriptor'

  def __delete__(self, instance: Any) -> None:
    raise AttributeError('value cannot be deleted')


class DeleteOnlyMixin:
  """DeleteOnlyMixin declares 'value' through 'DeleteOnly'."""

  value = DeleteOnly()


class LabelMixin:
  """LabelMixin declares 'label' as a plain class attribute."""

  label = 'mixin'


class TestFieldStorage(EZTest):
  """
  TestFieldStorage provides tests for the storage of 'EZData' field
  values.
  """

  def test_fields_live_in_instance_dict(self) -> None:
    """
    The field values are the entries of the instance '__dict__', and the
    class declares neither '__slots__' nor a class attribute for a field
    that clashes with nothing.
    """

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    self.assertEqual(vars(Point(1, 2)), {'x': 1.0, 'y': 2.0})
    self.assertNotIn('__slots__', Point.__dict__)
    self.assertNotIn('x', Point.__dict__)

  def test_field_named_like_object_descriptor(self) -> None:
    """
    A field named 'directory' shares its name with the read-only
    'Object.directory' descriptor. The field receives an 'EZStore', so it
    builds, casts and assigns like any other field, and reading it
    through the class gives the store.
    """

    class Located(EZData):
      directory = EZField[str]('here')

    self.assertEqual(Located().directory, 'here')
    located = Located('there')
    self.assertEqual(located.directory, 'there')
    located.directory = b'elsewhere'
    self.assertEqual(located.directory, 'elsewhere')
    self.assertIsInstance(Located.directory, EZStore)

  def test_mixin_property_does_not_take_field(self) -> None:
    """
    A read-only property of the same name on a mixin would refuse the
    value the constructor writes. The field receives an 'EZStore' and
    works as declared, while the mixin on its own keeps its property.
    """

    class Valued(EZData, PropertyMixin):
      value = EZField[str]('field')

    self.assertEqual(Valued().value, 'field')
    self.assertEqual(Valued('given').value, 'given')
    self.assertEqual(PropertyMixin().value, 'property')

  def test_delete_only_descriptor_counts(self) -> None:
    """
    A descriptor defining '__delete__' without '__set__' still takes
    precedence over the instance '__dict__', as the mixin on its own
    shows, so a field of the same name receives an 'EZStore' as well.
    """
    holder = DeleteOnlyMixin()
    holder.__dict__['value'] = 'dict'
    self.assertEqual(holder.value, 'descriptor')
    with self.assertRaises(AttributeError):
      del holder.value

    class Valued(EZData, DeleteOnlyMixin):
      value = EZField[str]('field')

    self.assertEqual(Valued().value, 'field')
    self.assertIsInstance(Valued.value, EZStore)

  def test_mixin_class_attribute_keeps_default(self) -> None:
    """
    A plain class attribute of the same name on a mixin yields to the
    instance '__dict__', so the field needs no store. It must not count
    as a value the instance already holds either, so the field still
    receives its declared default.
    """

    class Labelled(EZData, LabelMixin):
      label = EZField[str]('field')

    self.assertEqual(Labelled().label, 'field')
    self.assertNotIn('label', Labelled.__dict__)
    self.assertEqual(LabelMixin.label, 'mixin')

  def test_unset_stored_field_raises(self) -> None:
    """
    Reading a stored field on an instance that never received a value,
    such as one made by '__new__' alone, raises 'MissingVariable'.
    """

    class Located(EZData):
      directory = EZField[str]('here')

    bare = Located.__new__(Located)
    with self.assertRaises(MissingVariable):
      _ = bare.directory
