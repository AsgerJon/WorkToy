"""
TestMetaclassAnnotations subclasses 'CoreTest' and pins that
'cls.__annotations__' on a class built by a worktoy metaclass answers
for that class alone. Every module of the library declares
'from __future__ import annotations', so a metaclass whose body carries
annotations holds them as a plain dict under '__annotations__', which
sits ahead of 'type' in the lookup of its classes; a class without
annotations of its own then fell through to the annotations of a base,
'Object' for every 'BaseObject' subclass. 'MetaType' now replaces that
dict on every metaclass it builds with '_AnnotationsDescriptor', which
hands a class to 'type' and answers the metaclass's own annotations on
the metaclass.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import skipIf

from worktoy.core._annotations_descriptor import _AnnotationsDescriptor
from worktoy.mcls import AbstractMetaclass, BaseMeta, BaseObject

from . import CoreTest


class Bare(BaseObject):
  """Bare annotates nothing."""


class Noted(BaseObject):
  """Noted annotates one attribute."""

  x: int = 1


class TestMetaclassAnnotations(CoreTest):
  """
  TestMetaclassAnnotations provides tests for '__annotations__' on the
  classes of a worktoy metaclass.
  """

  @skipIf(sys.version_info < (3, 10), 'type has no descriptor before 3.10')
  def test_class_without_annotations(self) -> None:
    """A class annotating nothing answers an empty mapping, not the
    annotations of a base."""
    self.assertEqual(dict(Bare.__annotations__), {})

  def test_class_with_annotations(self) -> None:
    """A class annotating an attribute answers its own."""
    self.assertEqual(list(Noted.__annotations__), ['x'])
    self.assertIn(Noted.__annotations__['x'], (int, 'int'))

  @skipIf(sys.version_info < (3, 10), 'type has no descriptor before 3.10')
  def test_metaclass_keeps_its_own(self) -> None:
    """The metaclass answers the annotations of its own body through
    the descriptor 'MetaType' installed."""
    descriptor = AbstractMetaclass.__dict__['__annotations__']
    self.assertIsInstance(descriptor, _AnnotationsDescriptor)
    metaAnnotations = AbstractMetaclass.__annotations__
    self.assertIn('__abstract_metaclass__', metaAnnotations)
    self.assertNotIn('__abstract_metaclass__', Bare.__annotations__)

  @skipIf(sys.version_info < (3, 10), 'type has no descriptor before 3.10')
  def test_assignment_and_deletion(self) -> None:
    """Writing and deleting '__annotations__' on a class still reach
    'type', as they do without the descriptor."""

    class Scratch(metaclass=BaseMeta):
      pass

    Scratch.__annotations__ = {'y': int}
    self.assertEqual(dict(Scratch.__annotations__), {'y': int})
    del Scratch.__annotations__
    self.assertEqual(dict(Scratch.__annotations__), {})
