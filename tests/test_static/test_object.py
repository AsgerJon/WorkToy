"""
TestObject tests the Object class central to the 'worktoy'
library, found in the 'worktoy.static' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import StaticTest
from worktoy.core import Object
from worktoy.core.sentinels import THIS, OWNER
from worktoy.utilities import stringList
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import ReadOnlyError

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Any

  Bases: TypeAlias = tuple[type, ...]


class TestObject(StaticTest):
  """
  TestObject tests the Object class central to the 'worktoy'
  library, found in the 'worktoy.static' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_free(self) -> None:
    """
    Tests that an 'Object' instance not created inside a class
    body still behaves as expected.
    """
    obj = Object.__new__(Object)
    self.assertIsNone(getattr(obj, '__pos_args__'))
    self.assertIsNone(getattr(obj, '__key_args__'))
    posArgs = obj.getPosArgs()
    keyArgs = obj.getKeyArgs()
    self.assertIsInstance(posArgs, tuple)
    self.assertIsInstance(keyArgs, dict)
    self.assertFalse(posArgs and keyArgs)
    with self.assertRaises(MissingVariable) as context:
      _ = obj.getFieldName()
    e = context.exception
    self.assertEqual(e.varName, '__field_name__')
    self.assertEqual(e.varType, str, )
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(MissingVariable) as context:
      _ = obj.getFieldOwner()
    e = context.exception
    self.assertEqual(e.varName, '__field_owner__')
    self.assertEqual(e.varType, type, )
    self.assertEqual(str(e), repr(e))

  def test_bad_arg_types(self) -> None:
    """
    Tests that 'Object' raises 'TypeException' when the
    '__pos_args__' and '__key_args__' attributes have the wrong types.
    """
    obj = Object.__new__(Object)
    setattr(obj, '__pos_args__', 69)
    setattr(obj, '__key_args__', 420)
    with self.assertRaises(TypeException) as context:
      _ = obj.getPosArgs()
    e = context.exception
    self.assertEqual(e.varName, '__pos_args__')
    self.assertEqual(e.actualObject, 69)
    self.assertEqual(e.actualType, int)
    self.assertEqual({*e.expectedTypes}, {list, tuple})
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(TypeException) as context:
      _ = obj.getKeyArgs()
    e = context.exception
    self.assertEqual(e.varName, '__key_args__')
    self.assertEqual(e.actualObject, 420)
    self.assertEqual(e.actualType, int)
    self.assertEqual(e.expectedTypes, (dict,))
    self.assertEqual(str(e), repr(e))

  def test_THIS(self, ) -> None:
    """Tests that the 'THIS' property returns the correct value. """

    class Bar(Object):
      """
      This subclass of 'Object' is actually being tested here.
      """

      def __instance_get__(self, **kwargs, ) -> Any:
        """
        This method is called when the 'THIS' property is accessed.
        It returns the 'Bar' instance itself.
        """
        keyArgs = self.getKeyArgs()
        if keyArgs:
          return keyArgs['foo'].__inner_value__
        posArgs = self.getPosArgs()
        return posArgs[0].__inner_value__

    class Foo:
      """
      This class owns the 'Object' object being tested.
      """

      __inner_value__ = 69
      bar = Bar(foo=THIS, )
      baz = Bar(THIS, )

    foo = Foo()
    self.assertEqual(foo.bar, foo.baz)

  def test_str_repr(self) -> None:
    """
    Tests the string representation of 'Object'.
    """
    obj = Object()
    strObj = str(obj)
    reprObj = repr(obj)
    self.assertIn(Object.__module__, strObj)
    self.assertIn(Object.__name__, strObj)
    self.assertIn(Object.__module__, reprObj)
    self.assertIn(Object.__name__, reprObj)

  def test_accessors(self) -> None:
    """
    Tests the accessors of 'Object'.
    """

    class Label(Object):
      """
      This subclass of 'Object' is used to test the accessors.
      """

      def __instance_get__(self, **kwargs) -> Any:
        """
        This method is called when the 'Prop' instance is accessed.
        It returns the value of the 'value' attribute.
        """
        pvtName = self.getPrivateName()
        try:
          out = getattr(self.instance, pvtName)
        except Exception as exception:
          raise MissingVariable(pvtName, object) from exception
        else:
          return out

    class Prop(Label):
      """
      This subclass of 'Object' is used to test the accessors.
      """

      def __instance_set__(self, value: Any, **kwargs) -> None:
        """
        This method is called when the 'Prop' instance is set.
        It sets the value of the 'value' attribute.
        """
        setattr(self.instance, self.getPrivateName(), value)

    class Foo:
      """
      This class owns the 'Prop' object being tested.
      """

      bar = Prop()
      baz = Label()

    foo = Foo()
    privateName = Foo.bar.getPrivateName()
    with self.assertRaises(AttributeError) as context:
      _ = foo.bar
    e = context.exception
    self.assertIsInstance(e.__cause__, MissingVariable)
    self.assertEqual(e.__cause__.varName, privateName)
    self.assertEqual(e.__cause__.varType, object, )

    privateName = Foo.baz.getPrivateName()
    with self.assertRaises(ReadOnlyError) as context:
      foo.baz = 69
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.baz)
    self.assertEqual(e.newVal, 69)

    privateName = Foo.bar.getPrivateName()
    with self.assertRaises(AttributeError) as context:
      del foo.bar
    e = context.exception
    self.assertIsInstance(e.__cause__, MissingVariable)

    foo.bar = 69
    self.assertEqual(foo.bar, 69)

  def test_kwargs_parser(self) -> None:
    """
    Tests the keyword arguments parser of 'Object'.
    """
    obj = Object(breh=True, x=69, X='420 lmao')
    typeArgs = (complex, float, int)
    kwargs = obj.getKeyArgs()
    intX, _ = obj.parseKwargs(420, *typeArgs, 'x', 'X', **kwargs)
    bre, _ = obj.parseKwargs(complex, float, 'breh', **kwargs)
    bre2, _ = obj.parseKwargs(complex, 'breh', **kwargs)
    bre3, _ = obj.parseKwargs(float, 'breh', **kwargs)
    bre4, _ = obj.parseKwargs(float, int, 'breh', **{})
    derp, _ = obj.parseKwargs(int, **kwargs)
    with self.assertRaises(TypeException) as context:
      __, _ = obj.parseKwargs(float, int, 'breh', **{'breh': 'lmao'})
    e = context.exception
    self.assertEqual(e.varName, 'breh')
    self.assertEqual(e.actualObject, 'lmao')
    self.assertEqual(e.actualType, str)
    self.assertEqual({*e.expectedTypes}, {float, int})
    self.assertEqual(intX, 69)

  def test_owner(self, ) -> None:
    """
    Tests that OWNER can be resolved correctly from keyword arguments.
    """

    class CLS(Object):
      """
      This subclass of 'Object' is used to test the owner resolution.
      """

      def __instance_get__(self, **kwargs) -> Any:
        """
        This method is called when the 'Prop' instance is accessed.
        It returns the value of the 'value' attribute.
        """
        keyArgs = self.getKeyArgs()
        ownerKeys = stringList("""owner, cls, type, class_""")
        out, _ = self.parseKwargs(type, *ownerKeys, **keyArgs)
        return out

    class Foo:
      """
      This class owns the 'CLS' object being tested.
      """

      cls1 = CLS(owner=object, )
      cls2 = CLS(owner=OWNER)
      cls3 = CLS(class_=object, )

    foo = Foo()
    clsN = [foo.cls1, foo.cls3, ]
    for cls in clsN:
      self.assertIs(cls, object)
    self.assertIs(foo.cls2, Foo)
    self.assertEqual(str(Foo.cls1), repr(Foo.cls1))

  def test_present_field_owner(self) -> None:
    """
    Tests that 'Object' returns the field owner when it is set.
    """

    class Foo:
      bar = Object()

    self.assertIs(Foo.bar.getFieldOwner(), Foo)
