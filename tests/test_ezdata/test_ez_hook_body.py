"""
TestEZHookBody tests how 'EZHook' from 'worktoy.ezdata' screens each
binding of a dataclass body.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.desc import Alias, AttriBox, Field
from worktoy.dispatch import overload, Dispatcher
from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace, EZHook
from worktoy.waitaminute.ezdata import ReservedMethodError
from worktoy.waitaminute.ezdata import ReservedAttributeError
from worktoy.waitaminute.ezdata import IncompleteFieldException
from worktoy.waitaminute.ezdata import ClassFieldError, DuplicateError
from . import EzdataTest, Point2D, Peek


class TestEZHookBody(EzdataTest):
  """
  Each binding of a dataclass body is a field, a method, a descriptor
  or a refusal. An 'EZField' is registered, a bare value becomes a
  field of its type, a function or a descriptor stays as it is, and a
  class, a bare 'None', an incomplete field, a reserved method name or
  a reserved attribute name fails at its line. The tests pin every
  route of 'setItemPhase' and the helpers it decides by.
  """

  def test_reserved_method_refused(self) -> None:
    with self.assertRaises(ReservedMethodError) as context:
      class A(EZData):
        def __init__(self, *args) -> None:
          """Generated, not written."""

    exception = context.exception
    self.assertEqual(exception.methodName, '__init__')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("The class body of EZData class 'A' defines '__init__'",
                  str(exception))
    self.assertIn("'__post_init__'", str(exception))
    space = EZSpace(EZMeta, 'B', ())
    for name in EZSpace.__reserved_ez_methods__:
      with self.subTest(name=name):
        with self.assertRaises(ReservedMethodError) as context:
          space[name] = None
        self.assertEqual(context.exception.methodName, name)
        self.assertIs(context.exception.space, space)
        self.assertIn("EZData class 'B' defines '%s'" % name,
                      str(context.exception))

  def test_overloaded_reserved_method_refused(self) -> None:
    with self.assertRaises(ReservedMethodError) as context:
      class A(EZData):
        @overload(int)
        def __init__(self, n: int) -> None:
          """Claimed by the overload hook, refused as the class is made."""

    self.assertEqual(context.exception.methodName, '__init__')
    self.assertEqual(context.exception.space.getClassName(), 'A')
    self.assertIn("EZData class 'A' defines '__init__'",
                  str(context.exception))

    class B(EZData):
      x = 1

      @overload(int)
      def scale(self, n: int) -> int:
        return self.x * n

    self.assertIsInstance(B.__dict__['scale'], Dispatcher)
    self.assertEqual(B(2).scale(3), 6)

  def test_reserved_attribute_refused(self) -> None:
    with self.assertRaises(ReservedAttributeError) as context:
      class A(EZData):
        __kw_only__ = True

    exception = context.exception
    self.assertEqual(exception.attributeName, '__kw_only__')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("EZData class 'A' binds '__kw_only__'", str(exception))
    self.assertIn("'class A(EZData, kwOnly=True)'", str(exception))
    space = EZSpace(EZMeta, 'B', ())
    for name in EZSpace.__reserved_ez_attributes__:
      with self.subTest(name=name):
        with self.assertRaises(ReservedAttributeError) as context:
          space[name] = 1
        self.assertEqual(context.exception.attributeName, name)
        self.assertIs(context.exception.space, space)
        self.assertIn("EZData class 'B' binds '%s'" % name,
                      str(context.exception))

  def test_interpreter_names_pass(self) -> None:
    class A(EZData):
      """A docstring binds '__doc__'."""
      x = 1

    self.assertEqual([*A.__ez_fields__], ['x'])
    self.assertEqual(A.__doc__, "A docstring binds '__doc__'.")
    self.assertEqual(A.__module__, __name__)

  def test_fields_registered(self) -> None:
    class A(EZData):
      declared = EZField[int](1)
      bare = 2.5
      text = 'word'
      point = Point2D(1.0, 2.0)
      obj = Object()

    types = {k: f.fieldType for k, f in A.__ez_fields__.items()}
    expected = {
      'declared': int, 'bare': float, 'text': str, 'point': Point2D,
      'obj': Object,
    }
    self.assertEqual(types, expected)
    first, second = A(), A()
    self.assertEqual(first.point, Point2D(1.0, 2.0))
    self.assertIsNot(first.point, second.point)
    self.assertFalse(dict.__contains__(A.__namespace__, 'bare'))

  def test_incomplete_field_refused(self) -> None:
    with self.assertRaises(IncompleteFieldException) as context:
      class A(EZData):
        x = EZField(1)

    exception = context.exception
    self.assertEqual(exception.clsName, 'A')
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.missing, 'no field type was set')
    self.assertIn("'A' has incomplete field 'x': no field type was set",
                  str(exception))
    with self.assertRaises(IncompleteFieldException) as context:
      class B(EZData):
        y = EZField[int]

    self.assertEqual(context.exception.clsName, 'B')
    self.assertEqual(context.exception.fieldName, 'y')
    self.assertEqual(context.exception.missing,
                     'no construction arguments were given')
    self.assertIn("'B' has incomplete field 'y': no construction "
                  "arguments were given", str(context.exception))
    with self.assertRaises(IncompleteFieldException) as context:
      class C(EZData):
        z = None

    self.assertEqual(context.exception.clsName, 'C')
    self.assertEqual(context.exception.fieldName, 'z')
    self.assertEqual(context.exception.missing,
                     'a bare None default cannot infer a field type')
    self.assertIn("'C' has incomplete field 'z': a bare None default",
                  str(context.exception))

  def test_complete_field_check_by_hand(self) -> None:
    space = EZSpace(EZMeta, 'A', ())
    hook = EZSpace.__dict__['ezHook'].__get__(space, EZSpace)
    hook._assertCompleteField('a', EZField[int](1))
    hook._assertCompleteField('b', EZField[int](k=1))
    keyed = EZField[int]
    setattr(keyed, '__key_args__', {})
    hook._assertCompleteField('c', keyed)
    with self.assertRaises(IncompleteFieldException) as context:
      hook._assertCompleteField('d', EZField[int])
    self.assertEqual(context.exception.clsName, 'A')
    self.assertEqual(context.exception.fieldName, 'd')
    self.assertEqual(context.exception.missing,
                     'no construction arguments were given')
    self.assertIn("'A' has incomplete field 'd'", str(context.exception))
    with self.assertRaises(IncompleteFieldException) as context:
      hook._assertCompleteField('e', EZField(1))
    self.assertEqual(context.exception.clsName, 'A')
    self.assertEqual(context.exception.fieldName, 'e')
    self.assertEqual(context.exception.missing, 'no field type was set')
    self.assertIn("'A' has incomplete field 'e'", str(context.exception))

  def test_functions_stay(self) -> None:
    class A(EZData):
      x = 1
      size = len
      double = lambda self: self.x * 2

      def triple(self) -> int:
        return self.x * 3

    self.assertEqual([*A.__ez_fields__], ['x'])
    self.assertIs(A.size, len)
    self.assertEqual(A(2).double(), 4)
    self.assertEqual(A(2).triple(), 6)

  def test_classes_refused(self) -> None:
    with self.assertRaises(ClassFieldError) as context:
      class A(EZData):
        kind = int

    exception = context.exception
    self.assertEqual(exception.clsName, 'A')
    self.assertEqual(exception.fieldName, 'kind')
    self.assertIs(exception.classObject, int)
    self.assertIn("'A' binds the name 'kind' to the class 'int'",
                  str(exception))
    with self.assertRaises(ClassFieldError) as context:
      class B(EZData):
        class Nested:
          """A nested class statement binds a class."""

    self.assertEqual(context.exception.clsName, 'B')
    self.assertEqual(context.exception.fieldName, 'Nested')
    self.assertEqual(context.exception.classObject.__name__, 'Nested')
    self.assertIn("'B' binds the name 'Nested' to the class 'Nested'",
                  str(context.exception))

  def test_descriptors_stay(self) -> None:
    class SetOnly:
      def __set__(self, instance: object, value: object) -> None:
        instance.__dict__['held'] = value

    class DelOnly:
      def __delete__(self, instance: object) -> None:
        """Deletes nothing."""

    class A(EZData):
      x = 1
      prop = property(lambda self: self.x + 1)
      static = staticmethod(len)
      classy = classmethod(lambda cls: cls.__name__)
      field = Field()
      box = AttriBox[int](7)
      alias = Alias('triple')
      peek = Peek()
      setOnly = SetOnly()
      delOnly = DelOnly()

      def triple(self) -> int:
        return self.x * 3

    self.assertEqual([*A.__ez_fields__], ['x'])
    a = A(2)
    self.assertEqual(a.prop, 3)
    self.assertEqual(A.static('abc'), 3)
    self.assertEqual(A.classy(), 'A')
    self.assertIsInstance(A.__dict__['field'], Field)
    self.assertEqual(a.box, 7)
    self.assertEqual(a.alias(), 6)
    self.assertEqual(a.peek, 'peeked')
    self.assertIsInstance(A.__dict__['setOnly'], SetOnly)
    self.assertIsInstance(A.__dict__['delOnly'], DelOnly)
    a.setOnly = 5
    self.assertEqual(a.__dict__['held'], 5)

  def test_method_or_descriptor_at_a_field_name_refused(self) -> None:
    with self.assertRaises(DuplicateError) as context:
      class A(EZData):
        x = 1

        def x(self) -> None:
          """Never bound: the line binding it is refused."""

    exception = context.exception
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("class 'A', the already existing attribute name 'x'",
                  str(exception))
    self.assertNotIn('inherits', str(exception))
    with self.assertRaises(DuplicateError) as context:
      class B(EZData):
        y = EZField[int](1)
        y = property(len)

    self.assertEqual(context.exception.fieldName, 'y')
    self.assertEqual(context.exception.space.getClassName(), 'B')
    self.assertIn("class 'B', the already existing attribute name 'y'",
                  str(context.exception))
    with self.assertRaises(DuplicateError) as context:
      class C(EZData):
        z = 1
        z = AttriBox[int](2)

    self.assertEqual(context.exception.fieldName, 'z')
    self.assertEqual(context.exception.space.getClassName(), 'C')
    self.assertIn("class 'C', the already existing attribute name 'z'",
                  str(context.exception))
    space = EZSpace(EZMeta, 'D', ())
    hook = EZSpace.__dict__['ezHook'].__get__(space, EZSpace)
    self.assertTrue(hook.setItemPhase('n', 1))
    for value in (len, property(), staticmethod(len), Alias('m')):
      with self.subTest(value=type(value).__name__):
        with self.assertRaises(DuplicateError) as context:
          hook.setItemPhase('n', value)
        self.assertEqual(context.exception.fieldName, 'n')
        self.assertIs(context.exception.space, space)
        self.assertIn("class 'D', the already existing attribute name 'n'",
                      str(context.exception))
    #  At a name that is no field, the same values stay as they did.
    self.assertFalse(hook.setItemPhase('f', len))
    self.assertFalse(hook.setItemPhase('p', property()))
    self.assertEqual([*space.getEZFields()], ['n'])

  def test_method_or_descriptor_at_an_inherited_field_name_refused(
      self,
  ) -> None:
    with self.assertRaises(DuplicateError) as context:
      class A(Point2D):
        x = property(len, setattr)

    exception = context.exception
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("class 'A', the already existing attribute name 'x'",
                  str(exception))
    self.assertIn("'x' is a field the class inherits, and the name of a "
                  "field can only be declared again as a field.",
                  str(exception))
    self.assertEqual(exception.msg, str(exception))
    with self.assertRaises(DuplicateError) as context:
      class B(Point2D):
        def y(self) -> None:
          """Never bound: the line binding it is refused."""

    self.assertEqual(context.exception.fieldName, 'y')
    self.assertEqual(context.exception.space.getClassName(), 'B')
    self.assertIn("class 'B', the already existing attribute name 'y'",
                  str(context.exception))
    self.assertIn("'y' is a field the class inherits",
                  str(context.exception))
    #  A body that declares the inherited field again and then binds
    #  something else at it bound the name twice itself.
    with self.assertRaises(DuplicateError) as context:
      class D(Point2D):
        x = 1.0
        x = property(len)

    self.assertEqual(context.exception.fieldName, 'x')
    self.assertEqual(context.exception.space.getClassName(), 'D')
    self.assertIn("class 'D', the already existing attribute name 'x'",
                  str(context.exception))
    self.assertNotIn('inherits', str(context.exception))
    space = EZSpace(EZMeta, 'C', (Point2D,))
    hook = EZSpace.__dict__['ezHook'].__get__(space, EZSpace)
    self.assertEqual([*space.getEZFields()], [])
    with self.assertRaises(DuplicateError) as context:
      hook.setItemPhase('x', len)
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIs(context.exception.space, space)
    self.assertIn("class 'C', the already existing attribute name 'x'",
                  str(context.exception))
    self.assertIn("'x' is a field the class inherits",
                  str(context.exception))
    #  A name no class of the line declares as a field stays free.
    self.assertFalse(hook.setItemPhase('z', len))

  def test_overload_at_an_inherited_field_name_refused(self) -> None:
    with self.assertRaises(DuplicateError) as context:
      class A(Point2D):
        @overload(int)
        def x(self, n: int) -> None:
          """Claimed by the overload hook, refused as the class is made."""

    exception = context.exception
    self.assertEqual(exception.fieldName, 'x')
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn("class 'A', the already existing attribute name 'x'",
                  str(exception))
    self.assertIn("'x' is a field the class inherits",
                  str(exception))

    class B(Point2D):
      @overload(int)
      def scale(self, n: int) -> float:
        return self.x * n

    self.assertIsInstance(B.__dict__['scale'], Dispatcher)
    self.assertEqual(B(2, 3).scale(3), 6.0)

  def test_descriptor_helpers(self) -> None:
    class GetOnly:
      def __get__(self, instance: object, owner: type) -> int:
        return 1

    class Bare:
      """Defines nothing of the descriptor protocol."""

    self.assertTrue(EZHook._isDescriptor(Peek()))
    self.assertTrue(EZHook._isDescriptor(Alias('x')))
    self.assertFalse(EZHook._isDescriptor(Object()))
    self.assertFalse(EZHook._isDescriptor(Point2D()))
    self.assertTrue(EZHook._isDescriptor(GetOnly()))
    self.assertTrue(EZHook._isDescriptor(property()))
    self.assertFalse(EZHook._isDescriptor(Bare()))
    self.assertFalse(EZHook._isDescriptor(5))
    self.assertTrue(EZHook._overridesObjectProtocol(Peek))
    self.assertFalse(EZHook._overridesObjectProtocol(Object))
    self.assertFalse(EZHook._overridesObjectProtocol(Point2D))
    self.assertTrue(EZHook._typeDefines(int, '__add__'))
    self.assertFalse(EZHook._typeDefines(int, '__nothing__'))
    self.assertEqual(GetOnly().__get__(None, GetOnly), 1)

  def test_set_item_phase_by_hand(self) -> None:
    space = EZSpace(EZMeta, 'A', ())
    hook = EZSpace.__dict__['ezHook'].__get__(space, EZSpace)
    self.assertFalse(hook.setItemPhase('__module__', 'm'))
    self.assertFalse(hook.setItemPhase('f', len))
    self.assertFalse(hook.setItemPhase('p', property()))
    self.assertTrue(hook.setItemPhase('x', EZField[int](1)))
    self.assertTrue(hook.setItemPhase('y', 2))
    self.assertEqual([*space.getEZFields()], ['x', 'y'])
    self.assertIs(space.getEZFields()['y'].fieldType, int)

  def test_random_bare_values(self) -> None:
    self.randomWord.size = 5
    self.randomInteger.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    numbers = self.randomInteger.row[:len(words)]
    body = {word: number for word, number in zip(words, numbers)}
    cls = EZMeta('R', (EZData,), body)
    self.assertEqual([*cls.__ez_fields__], words)
    instance = cls()
    for word, number in zip(words, numbers):
      with self.subTest(word=word):
        self.assertEqual(getattr(instance, word), number)
        self.assertIs(cls.__ez_fields__[word].fieldType, int)
