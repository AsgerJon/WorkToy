"""
TestInterpreterNames subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that the names the interpreter writes into a class body
on its own pass through the 'EZData' namespace untouched. 'EZHook' turns
every plain class-body value into a field, and these names hold plain
values, yet each one is plumbing the interpreter reads back when it
builds the class: '__classcell__' backs 'super()' and '__class__',
'__orig_bases__' and '__type_params__' back generic classes, and
'__classdictcell__' backs the lazily evaluated annotations of Python
3.14. Captured as fields, they break the class or leak into its fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import Generic, TypeVar
from unittest import skipIf

from worktoy.ezdata import EZData, EZField

from . import EZTest

T = TypeVar('T')

#  Compiled without the future import of this file, since that import is
#  what keeps Python 3.14 from adding '__classdictcell__' to the body.
_LAZY_ANNOTATIONS = """
class Annotated(EZData):
  x: int = EZField[int](0)
"""

#  The type parameter syntax of Python 3.12 cannot appear directly in a
#  file that must still parse on Python 3.7.
_TYPE_PARAMS = """
class Box[S](EZData):
  x = EZField[int](0)
"""


class TestInterpreterNames(EZTest):
  """
  TestInterpreterNames provides tests for class bodies that make the
  interpreter add names of its own to the 'EZData' namespace.
  """

  def test_super_in_post_init(self) -> None:
    """
    A subclass '__post_init__' reaches the one it overrides through
    'super()', which needs '__classcell__' to arrive at 'type.__new__'.
    Both hooks run, the parent's first, and the cell is not a field.
    """

    class Base(EZData):
      calls = EZField[list]()

      def __post_init__(self) -> None:
        self.calls.append('base')

    class Sub(Base):
      def __post_init__(self) -> None:
        super().__post_init__()
        self.calls.append('sub')

    self.assertEqual(Sub().calls, ['base', 'sub'])
    self.assertEqual(tuple(Sub.__ez_fields__), ('calls',))

  def test_super_in_method(self) -> None:
    """
    An ordinary method override reaches the method it overrides through
    'super()'.
    """

    class Base(EZData):
      x = EZField[int](0)

      def describe(self) -> str:
        return 'x=%d' % self.x

    class Sub(Base):
      def describe(self) -> str:
        return '<%s>' % super().describe()

    self.assertEqual(Sub(3).describe(), '<x=3>')

  def test_dunder_class_in_method(self) -> None:
    """
    A method naming '__class__' receives the class that defined it, not
    the class of the instance, which the interpreter provides through the
    same '__classcell__'.
    """

    class Holder(EZData):
      x = EZField[int](0)

      def definingClass(self) -> type:
        return __class__

    class Child(Holder):
      pass

    self.assertIs(Holder().definingClass(), Holder)
    self.assertIs(Child().definingClass(), Holder)
    self.assertEqual(tuple(Holder.__ez_fields__), ('x',))

  def test_generic_base(self) -> None:
    """
    An 'EZData' class may also derive from 'Generic[T]'. The interpreter
    records the bases as written in '__orig_bases__', and 'Generic' reads
    them back while the class is created to find its type parameters.
    """

    class Box(EZData, Generic[T]):
      x = EZField[int](0)

    self.assertEqual(tuple(Box.__ez_fields__), ('x',))
    self.assertIn(Generic[T], Box.__orig_bases__)
    self.assertEqual(Box.__parameters__, (T,))
    self.assertEqual(Box[int](3).x, 3)

  @skipIf(sys.version_info < (3, 12), 'type parameters need Python 3.12')
  def test_type_params(self) -> None:
    """
    The type parameter syntax of Python 3.12 adds '__type_params__' next
    to '__orig_bases__'. Both stay out of the fields, and the class
    exposes the type parameter it declared.
    """
    namespace = dict(__name__=__name__, EZData=EZData, EZField=EZField)
    exec(_TYPE_PARAMS, namespace)
    Box = namespace['Box']
    self.assertEqual(tuple(Box.__ez_fields__), ('x',))
    param, = Box.__type_params__
    self.assertEqual(param.__name__, 'S')
    self.assertEqual(Box(4).x, 4)

  @skipIf(sys.version_info < (3, 14), 'lazy annotations need Python 3.14')
  def test_lazy_annotations(self) -> None:
    """
    From Python 3.14, a class body with annotations and no future import
    also receives '__classdictcell__', which the interpreter fills in
    when the class is created. The cell stays out of the fields, and the
    annotations still evaluate.
    """
    #  Imported here because the package only exists from Python 3.14.
    import annotationlib
    code = compile(_LAZY_ANNOTATIONS, '<lazy>', 'exec', dont_inherit=True)
    namespace = dict(__name__=__name__, EZData=EZData, EZField=EZField)
    exec(code, namespace)
    Annotated = namespace['Annotated']
    self.assertEqual(tuple(Annotated.__ez_fields__), ('x',))
    self.assertEqual(annotationlib.get_annotations(Annotated), {'x': int})
