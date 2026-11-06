"""
TestDefinedAnnotations tests '_DefinedAnnotationsBehaviour' from
'worktoy.core._meta_type'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import skipIf

from worktoy.core import MetaType
from worktoy.core._meta_type import _DefinedAnnotationsBehaviour
from . import CoreTest


class TestDefinedAnnotations(CoreTest):
  """
  Reading '__annotations__' on a class whose metaclass annotates its own
  body has undefined behaviour under PEP 649, and may give the
  annotations of the metaclass. '_DefinedAnnotationsBehaviour' is the
  entry 'MetaType' writes into every class so the read gives the class's
  own, evaluated no sooner than the first read on Python 3.14. The tests
  pin the four routes 'fromNamespace' takes, the deferred evaluation
  with its retry after a 'NameError', and the read through class and
  instance.
  """

  @staticmethod
  def _deferred(**names) -> tuple[type, dict]:
    """A class whose body left its annotations to an annotate function,
    as Python 3.14 does for a body compiled without the future import:
    the function answers from 'names', which the test may fill after
    the class exists, and raises 'NameError' for a name not there yet."""
    def __annotate__(format: int) -> dict:
      try:
        return {'x': int, 'y': names['Later']}
      except KeyError as keyError:
        raise NameError("name 'Later' is not defined") from keyError

    space = {'__annotate__': __annotate__, '__module__': __name__}
    return MetaType('Made', (), space), names

  def test_plain_dict_route(self) -> None:
    entry = _DefinedAnnotationsBehaviour.fromNamespace(
        {'__annotations__': {'a': int}})
    self.assertIsInstance(entry, _DefinedAnnotationsBehaviour)
    self.assertEqual(entry, {'a': int})
    self.assertIsNone(entry.__annotate_function__)

  def test_empty_body_route(self) -> None:
    entry = _DefinedAnnotationsBehaviour.fromNamespace({'x': 1})
    self.assertEqual(entry, {})
    self.assertIsNone(entry.__annotate_function__)

  def test_custom_value_route(self) -> None:
    class Other(dict):
      pass

    self.assertIsNone(_DefinedAnnotationsBehaviour.fromNamespace(
        {'__annotations__': ['x']}))
    self.assertIsNone(_DefinedAnnotationsBehaviour.fromNamespace(
        {'__annotations__': Other(a=1)}))

  @skipIf(sys.version_info < (3, 14), 'deferred annotations came in 3.14')
  def test_entry_route_copies_pending_function(self) -> None:
    Made, _ = self._deferred(Later=str)
    first = Made.__dict__['__annotations__']
    self.assertIsNotNone(first.__annotate_function__)
    entry = _DefinedAnnotationsBehaviour.fromNamespace(
        {'__annotations__': first})
    self.assertIsNot(entry, first)
    self.assertIs(entry.__annotate_function__, first.__annotate_function__)
    self.assertEqual(entry.__get__(None, Made), {'x': int, 'y': str})
    self.assertIsNotNone(first.__annotate_function__)

  def test_rebuilt_class_gets_own_entry(self) -> None:
    class A(metaclass=MetaType):
      x: int = 1

    space = {k: v for k, v in A.__dict__.items()
             if k not in ('__dict__', '__weakref__')}
    B = MetaType('B', (), space)
    self.assertEqual(B.__annotations__, {'x': 'int'})
    self.assertIsNot(B.__dict__['__annotations__'],
                     A.__dict__['__annotations__'])
    self.assertIs(B.__namespace__, A.__namespace__)

  @skipIf(sys.version_info < (3, 14), 'deferred annotations came in 3.14')
  def test_deferred_evaluated_at_first_read_only(self) -> None:
    Made, _ = self._deferred(Later=str)
    entry = Made.__dict__['__annotations__']
    self.assertEqual(dict.__len__(entry), 0)
    self.assertEqual(Made.__annotations__, {'x': int, 'y': str})
    self.assertIsNone(entry.__annotate_function__)
    self.assertIs(Made.__annotations__, entry)
    self.assertIs(Made().__annotations__, entry)

  @skipIf(sys.version_info < (3, 14), 'deferred annotations came in 3.14')
  def test_name_error_retried_on_next_read(self) -> None:
    Made, names = self._deferred()
    with self.assertRaises(NameError):
      _ = Made.__annotations__
    entry = Made.__dict__['__annotations__']
    self.assertIsNotNone(entry.__annotate_function__)
    names['Later'] = float
    self.assertEqual(Made.__annotations__, {'x': int, 'y': float})
    self.assertIsNone(entry.__annotate_function__)

  def test_get_returns_entry_without_function(self) -> None:
    entry = _DefinedAnnotationsBehaviour({'a': 1})
    self.assertIs(entry.__get__(None, dict), entry)
    self.assertIs(entry.__get__(object(), None), entry)
