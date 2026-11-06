"""
TestMetaType tests 'MetaType' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from dataclasses import dataclass
from unittest import skipIf

from worktoy.core import MetaType
from worktoy.core._meta_type import _Chill, _DefinedAnnotationsBehaviour
from . import CoreTest, RecordingMeta


class TestMetaType(CoreTest):
  """
  'MetaType' builds every class of the library and gives each what plain
  'type' does not: '_Chill' last in the resolution order so the class
  statement may carry keywords, the namespace of the body kept under
  '__namespace__', an annotations entry of the class's own, the
  '__skip_hash__' mark, a text naming the metaclass, and an '__init__'
  that hands on to the next metaclass with every keyword. The tests pin
  each of these on classes built by statement and by call.
  """

  def test_chill_appended_after_plain_bases(self) -> None:
    class A(metaclass=MetaType):
      pass

    self.assertEqual(A.__bases__, (_Chill,))
    self.assertIs(A.__mro__[-2], _Chill)
    self.assertIs(A.__mro__[-1], object)

  def test_chill_not_appended_after_worktoy_base(self) -> None:
    class A(metaclass=MetaType):
      pass

    class B(A):
      pass

    self.assertEqual(B.__bases__, (A,))
    self.assertEqual(B.__mro__.count(_Chill), 1)

  def test_object_dropped_from_explicit_bases(self) -> None:
    class A(object, metaclass=MetaType):
      pass

    self.assertEqual(A.__bases__, (_Chill,))

  def test_plain_base_kept_before_chill(self) -> None:
    class Plain:
      pass

    class A(Plain, metaclass=MetaType):
      pass

    self.assertEqual(A.__bases__, (Plain, _Chill))

  def test_class_keywords_accepted(self) -> None:
    class A(metaclass=MetaType, flavour='mint'):
      pass

    self.assertTrue(issubclass(A, _Chill))

  def test_namespace_kept_on_class_and_removed_from_body(self) -> None:
    space = {'value': 1}
    A = MetaType('A', (), space)
    self.assertIs(A.__namespace__, space)
    self.assertIs(A.__dict__['__namespace__'], space)
    self.assertNotIn('__namespace__', space)
    self.assertEqual(A.value, 1)

  def test_body_defining_namespace_kept(self) -> None:
    marker = {'from': 'compile'}
    space = {'__namespace__': marker}
    A = MetaType('A', (), space)
    self.assertIs(A.__namespace__, marker)
    self.assertIs(space['__namespace__'], marker)

  def test_skip_hash_marks(self) -> None:
    class A(metaclass=MetaType):
      pass

    self.assertTrue(_Chill.__skip_hash__)
    self.assertFalse(A.__skip_hash__)
    self.assertIn('__skip_hash__', vars(A))

  def test_text_names_metaclass(self) -> None:
    class Meta(MetaType, metaclass=MetaType):
      pass

    class A(metaclass=MetaType):
      pass

    class B(metaclass=Meta):
      pass

    self.assertEqual(str(A), 'A[metaclass=MetaType]')
    self.assertEqual(repr(A), 'A[metaclass=MetaType]')
    self.assertEqual(str(B), 'B[metaclass=Meta]')
    self.assertEqual(str(Meta), 'Meta[metaclass=MetaType]')

  def test_init_hands_on_to_following_metaclass(self) -> None:
    class Both(MetaType, RecordingMeta, metaclass=MetaType):
      pass

    RecordingMeta.records.clear()

    class X(metaclass=Both, tag=1):
      pass

    self.assertEqual(RecordingMeta.records, [('X', {'tag': 1})])
    self.assertFalse(X.__skip_hash__)
    self.assertIs(X.__mro__[-2], _Chill)

  def test_init_reached_from_preceding_metaclass(self) -> None:
    class Both(RecordingMeta, MetaType):
      pass

    RecordingMeta.records.clear()

    class Y(metaclass=Both, tag=2):
      pass

    self.assertEqual(RecordingMeta.records, [('Y', {'tag': 2})])
    self.assertFalse(Y.__skip_hash__)
    self.assertIs(Y.__namespace__, Y.__dict__['__namespace__'])

  def test_annotations_are_the_class_own(self) -> None:
    class A(metaclass=MetaType):
      x: int

    class B(A):
      y: str

    class E(metaclass=MetaType):
      pass

    self.assertIsInstance(A.__dict__['__annotations__'],
                          _DefinedAnnotationsBehaviour)
    self.assertEqual(A.__annotations__, {'x': 'int'})
    self.assertEqual(B.__annotations__, {'y': 'str'})
    self.assertEqual(E.__annotations__, {})
    self.assertIs(A().__annotations__, A.__dict__['__annotations__'])

  def test_custom_annotations_value_kept(self) -> None:
    class A(metaclass=MetaType):
      __annotations__ = ['x']

    self.assertEqual(A.__annotations__, ['x'])
    self.assertIs(type(A.__dict__['__annotations__']), list)

  def test_rebuilt_from_own_bases(self) -> None:
    #  A class rebuilt from its own bases hands '_Chill' back in, and
    #  must not receive it a second time.
    class A(metaclass=MetaType):
      x: int = 1

    space = {k: v for k, v in A.__dict__.items()
             if k not in ('__dict__', '__weakref__')}
    B = MetaType('B', A.__bases__, space)
    self.assertEqual(B.__bases__, (_Chill,))
    self.assertEqual(B.__mro__.count(_Chill), 1)
    self.assertEqual(B.x, 1)

  @skipIf(sys.version_info < (3, 10), 'dataclass slots came in 3.10')
  def test_dataclass_slots_rebuild(self) -> None:
    @dataclass(slots=True)
    class Point(metaclass=MetaType):
      x: int = 0
      y: int = 0

    self.assertEqual(Point.__slots__, ('x', 'y'))
    self.assertEqual(Point(1, 2).y, 2)
    self.assertEqual(Point.__annotations__, {'x': 'int', 'y': 'int'})
    self.assertEqual(Point.__mro__.count(_Chill), 1)
    self.assertIs(Point.__mro__[-2], _Chill)

  def test_metaclass_is_instance_and_subclass(self) -> None:
    class Meta(MetaType, metaclass=MetaType):
      pass

    self.assertIsInstance(Meta, MetaType)
    self.assertIsSubclass(Meta, MetaType)
    self.assertFalse(Meta.__skip_hash__)
