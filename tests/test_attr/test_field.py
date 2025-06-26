"""TestField tests the Field descriptor functionality."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import WYD
from unittest import TestCase
from types import FunctionType as Func
from typing import TYPE_CHECKING

from tests.test_attr import ComplexField
from worktoy.attr import Field
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.parse import maybe
from worktoy.static import overload, AbstractObject
from worktoy.static.zeroton import THIS, DELETED
from worktoy.text import stringList
from worktoy.waitaminute import ProtectedError, MissingVariable, \
  TypeException, ReadOnlyError, WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  pass


class R2(metaclass=BaseMeta):
  """R2 is a class that represents a point in 2D space."""

  __fallback_r0__ = 0.0
  __fallback_r1__ = 0.0

  __r_0__ = None
  __r_1__ = None

  r0 = Field()
  r1 = Field()

  @r0.GET
  def _getR0(self) -> float:
    """Get the x-coordinate."""
    return maybe(self.__r_0__, self.__fallback_r0__)

  @r0.SET
  def _setR0(self, value: float) -> None:
    """Set the x-coordinate."""
    self.__r_0__ = float(value)

  @r1.GET
  def _getR1(self) -> float:
    """Get the y-coordinate."""
    return maybe(self.__r_1__, self.__fallback_r1__)

  @r1.SET
  def _setR1(self, value: float) -> None:
    """Set the y-coordinate."""
    self.__r_1__ = float(value)

  @overload(int, int)
  @overload(float, float)
  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    """Initialize the R2 object."""
    self.r0 = float(x)
    self.r1 = float(y)

  @overload(THIS)
  def __init__(self, other: R2) -> None:
    """Initialize the R2 object."""
    self.r0 = other.r0
    self.r1 = other.r1

  @overload()
  def __init__(self, ) -> None:
    pass


class ComplexNumber(R2):
  """ComplexNumber is a class that represents a complex number."""

  @overload(complex)
  def __init__(self, z: complex) -> None:
    """Initialize the R2 object."""
    self.r0 = z.real
    self.r1 = z.imag


class TestField(TestCase):
  """Test the Field descriptor functionality."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self, ) -> None:
    """Testing that complex numbers initialize correctly."""
    self.R2_0 = R2()
    self.R2_1 = R2(69, 420)
    self.R2_2 = R2(69.0, 420.0)
    self.R2_3 = R2(self.R2_0)
    self.C_0 = ComplexNumber()
    self.C_1 = ComplexNumber(69, 420)
    self.C_2 = ComplexNumber(69.0, 420.0)
    self.C_3 = ComplexNumber(self.C_0)
    self.C_4 = ComplexNumber(complex(69.0, 420.0))

  def test_init_get(self, ) -> None:
    """Test the values of the R2 class."""
    self.assertEqual(self.R2_0.r0, 0.0)
    self.assertEqual(self.R2_0.r1, 0.0)
    self.assertEqual(self.R2_1.r0, 69.0)
    self.assertEqual(self.R2_1.r1, 420.0)
    self.assertEqual(self.R2_2.r0, 69.0)
    self.assertEqual(self.R2_2.r1, 420.0)
    self.assertEqual(self.R2_3.r0, 0.0)
    self.assertEqual(self.R2_3.r1, 0.0)

  def test_good_set(self) -> None:
    """Test the accessors of the R2 class."""
    self.assertEqual(self.R2_0.r0, 0.0)
    self.R2_0.r0 = 69.0
    self.assertEqual(self.R2_0.r0, 69.0)
    self.assertEqual(self.R2_0.r1, 0.0)
    self.R2_0.r1 = 420.0
    self.assertEqual(self.R2_0.r1, 420.0)
    self.assertEqual(self.C_0.r0, 0.0)
    self.C_0.r0 = 69.0
    self.assertEqual(self.C_0.r1, 0.0)
    self.C_0.r1 = 420.0
    self.assertEqual(self.C_0.r0, 69.0)
    self.assertEqual(self.C_0.r1, 420.0)

  def test_bad_delete(self) -> None:
    """Tests that the correct errors are raised."""
    with self.assertRaises(ProtectedError):
      del self.R2_0.r0
    with self.assertRaises(ProtectedError):
      del self.R2_0.r1
    with self.assertRaises(ProtectedError):
      del self.C_0.r0
    with self.assertRaises(ProtectedError):
      del self.C_0.r1

  def test_no_key(self, ) -> None:
    """Tests that the correct errors are raised."""

    class KeysScumbag:
      """
      The universal symbol for keys.
      """
      mrFFFFFF = Field()

    FF0088 = KeysScumbag()
    with self.assertRaises(MissingVariable) as context:
      _ = FF0088.mrFFFFFF

    exception = context.exception
    self.assertEqual(exception.varName, '__getter_key__')
    self.assertIs(exception.varType[0], str)

    setattr(KeysScumbag.mrFFFFFF, '__getter_key__', 80085)

    with self.assertRaises(TypeException) as context:
      _ = FF0088.mrFFFFFF

    exception = context.exception
    self.assertEqual(exception.varName, '__getter_key__')
    self.assertIs(exception.actualObject, 80085)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], str)

  def test_bad_setter_key_type(self) -> None:
    """Tests that the correct errors are raised."""

    class Foo:
      """
      Foo is a class with a Field descriptor.
      """
      bar = Field()
      eggs = Field()
      ham = Field()

      @ham.DELETE
      def _deleteHam(self) -> None:
        """Delete the ham field."""
        raise ProtectedError(self, type(self).ham, 'tofu')

    setattr(Foo.bar, '__setter_keys__', [69, 420])
    setattr(Foo.bar, '__deleter_keys__', [1337, 80085])
    setattr(Foo.eggs, '__setter_keys__', 'imma key, trust!')
    setattr(Foo.eggs, '__deleter_keys__', 'imma key, trust!')
    foo = Foo()
    with self.assertRaises(TypeException) as context:
      foo.bar = 80085

    exception = context.exception
    self.assertEqual(exception.varName, 'key')
    self.assertEqual(exception.actualObject, 69)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], str)

    with self.assertRaises(TypeException) as context:
      foo.eggs = 8008135
    exception = context.exception
    self.assertEqual(exception.varName, '__setter_keys__')
    self.assertEqual(exception.actualObject, 'imma key, trust!')
    self.assertIs(exception.actualType, str)
    self.assertIs(exception.expectedType[0], tuple)

    with self.assertRaises(TypeException) as context:
      del foo.bar
    exception = context.exception
    self.assertEqual(exception.varName, 'key')
    self.assertEqual(exception.actualObject, 1337)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], str)

    with self.assertRaises(TypeException) as context:
      del foo.eggs
    exception = context.exception
    self.assertEqual(exception.varName, '__deleter_keys__')
    self.assertEqual(exception.actualObject, 'imma key, trust!')
    self.assertIs(exception.actualType, str)
    self.assertIs(exception.expectedType[0], tuple)

    with self.assertRaises(ProtectedError) as context:
      del foo.ham
    exception = context.exception
    self.assertIs(exception.owningInstance, foo)
    self.assertIs(exception.descriptorObject, Foo.ham)
    self.assertEqual(exception.existingValue, 'tofu')

  def test_good_deleter(self, ) -> None:
    """
    Testing a good deleter for the Field descriptor.
    """

    class Foo(BaseObject):
      __to_fu__ = 'you like it in GTNH tho!'

      eggs = Field()
      ham = Field()
      tofu = Field()

      @tofu.GET
      def _eeew(self) -> str:
        return self.__to_fu__

      @eggs.GET
      def _getEggs(self) -> str:
        return 'eggs'

      @tofu.DELETE
      def _imagineEatingTofu(self) -> None:
        pass

      @tofu.DELETE
      def _getThatTofuAwayFromMe(self) -> None:
        pass

      @tofu.DELETE
      def _setToDELETED(self) -> None:
        """Delete the tofu field."""
        setattr(self, '__to_fu__', DELETED)

    foo = Foo()
    self.assertIsInstance(Foo.tofu, Field)
    self.assertIsInstance(foo.tofu, str)
    del foo.tofu
    with self.assertRaises(AttributeError) as context:
      _ = foo.tofu
    exception = context.exception
    words = stringList("""AttributeError, foo, object, has, no, tofu""")
    for word in words:
      self.assertIn(word.lower(), str(exception).lower())

    self.assertEqual(foo.eggs, 'eggs')

  def test_getter_bad_type(self, ) -> None:
    """
    Testing a bad getter for the Field descriptor.
    """

    def breh(*args) -> None:
      """
      No-op
      """

    class Pig:
      foo = Field()
      bar = Field()
      bad = Field()  # Has no getter

      foo.GET(breh)

      @bar.GET
      def _getBar(self) -> str:
        """Get the bar field."""
        return 'bar'

    class Ham(Pig):
      breh = None

    ham = Ham()
    with self.assertRaises(MissingVariable) as context:
      _ = ham.foo
    exception = context.exception
    self.assertEqual(exception.varName, 'breh')
    self.assertIs(exception.varType[0], Func)

    setattr(Ham, 'breh', 69)

    with self.assertRaises(TypeException) as context:
      _ = ham.foo
    exception = context.exception
    self.assertEqual(exception.varName, 'breh')
    self.assertEqual(exception.actualObject, 69)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)
    self.assertIs(Pig.foo._getGetFuncObject(), breh)
    pig = Pig()
    self.assertEqual(pig.bar, 'bar')  # Gets the function object directly
    ham = Ham()
    self.assertEqual(ham.bar, 'bar')

    class Sandwich(Ham):
      """Sandwich is a class that inherits from Ham."""

      def _getBar(self, ) -> str:
        """Get the bar field."""
        return 'sandwich bar'

    sandwich = Sandwich()
    self.assertEqual(sandwich.bar, 'sandwich bar')

    #  The Field._getGetFuncObject is always able to retrieve a function
    #  object when it is called. When a subclass overrides the getter,
    #  it does not remove the function object. Instead, the subclass
    #  always retrieves directly by name. Thus, the _getGetFuncObject is
    #  never called in this case.

    #  If a 'Field' object fails to provide a getter function, then the
    #  control flow raises an exception when unable to retrieve the
    #  getter-key. Thus, the missing getter function also does not see an
    #  invocation of the _getGetFuncObject method under conditions where
    #  there is no getter function object.

    #  The Pig.bad field has no getter function.

    setattr(Pig.bad, '__getter_key__', 'bad_getter')  # Valid string

    with self.assertRaises(AttributeError) as context:
      _ = pig.bad
    exception = context.exception
    expectedMessage = """type object 'Pig' has no attribute 'bad_getter'"""
    self.assertIn(expectedMessage.lower(), str(exception).lower())

    #  The above does raise an AttributeError. It should cover the
    #  _getGetFuncObject method where no getter function is found.

    #  In the _getGet, the clause: 'if self.__getter_func__ is not None:'
    #  is repeated in the '_getGetFuncObject' method preventing coverage.
    #  Removing this clause from _getGetFuncObject would have no effect.
    #  It will still have a clause type-checking the __getter_func__
    #  object raising TypeException if not a function. Removing the
    #  repeated 'is not None' clause also allows removal of the recursive
    #  call.

    #  With this redundancy removed, the coverage still requires a case
    #  where the getter function object is not a function object.

    setattr(Pig.bad, '__getter_func__', 80085)  # Invalid function object

    with self.assertRaises(TypeException) as context:
      _ = pig.bad
    exception = context.exception
    self.assertEqual(exception.varName, '__getter_func__')
    self.assertEqual(exception.actualObject, 80085)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)

  def test_missing_setter_at_key(self) -> None:
    """
    Testing that a 'Field' object has a setter key that fails to resolve
    to a value:
      'setterFunc = getattr(self.owner, setterKey, None)'  # -> None
    This requires a baseclass with a normal setter function later removed
    and a subclass that explicitly sets 'None' as the object at the key.
    Thus, the above clause should be truncated to:
      'setterFunc = getattr(self.owner, setterKey, )'  # -> None
    Even if a subclass has the setter function explicitly removed,
    the getattr call will simply find it on the baseclass, but if the
    subclass explicitly sets the key to 'None', then 'hasattr' would
    recognize the key as present on the subclass. Doing so eliminates the
    need for the third argument to 'getattr' in this case.
    """

    class Pig:
      """Pig is a class with a Field descriptor."""
      bad = Field()
      good = Field()
      derp = Field()  # Subclass replaces setter with wrong type
      extraBad = Field()  # Replaces setter with wrong type on baseclass

      @bad.GET
      def _getBad(self) -> str:
        """Get the bad field."""
        return 'bad'

      @bad.SET
      def _setBad(self, value: str) -> None:
        """Set the bad field."""

      @good.GET
      def _getGood(self) -> str:
        """Get the good field."""
        return 'good'

      @good.SET
      def _setGood(self, value: str) -> None:
        """Set the good field."""
        pass

      @derp.GET
      def _getDerp(self) -> str:
        """Get the derp field."""
        return 'derp'

      @derp.SET
      def _setDerp(self, value: str) -> None:
        """Set the derp field."""

      @extraBad.GET
      def _getExtraBad(self) -> str:
        """Get the extraBad field."""
        return 'yikes!'

      @extraBad.SET
      def _setExtraBad(self, value: str) -> None:
        """Set the 'extraBad' field."""

    pig = Pig()
    self.assertEqual(pig.good, 'good')
    self.assertEqual(pig.bad, 'bad')
    self.assertEqual(pig.derp, 'derp')
    self.assertEqual(pig.extraBad, 'yikes!')

    class Ham(Pig):
      """Ham is a class that inherits from Pig."""
      pass

    setattr(Ham, Pig.bad.__setter_keys__[0], None)
    setattr(Ham, Pig.derp.__setter_keys__[0], 420)  # Wrong type
    ham = Ham()
    ham.good = 'good'  # Covers 'Field._getSet'
    with self.assertRaises(MissingVariable) as context:
      ham.bad = 69
    exception = context.exception
    self.assertEqual(exception.varName, Pig.bad.__setter_keys__[0])
    self.assertIs(exception.varType[0], Func)

    with self.assertRaises(TypeException) as context:
      ham.derp = 80085
    exception = context.exception
    self.assertEqual(exception.varName, Pig.derp.__setter_keys__[0])
    self.assertEqual(exception.actualObject, 420)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)

  def test_bad_setter_type(self) -> None:
    """
    Testing exceptions related to bad setter types.
    """

    class Pig:
      """Pig is a class with a Field descriptor."""
      good = Field()
      bad = Field()  # Subclass replaces with wrong type
      extraBad = Field()  # Subclasses replaces with tuple with wrong type

      @good.GET
      def _getGood(self) -> str:
        """Get the good field."""
        return 'good'

      @good.SET
      def _setGood(self, value: str) -> None:
        """Set the good field."""
        pass

      @bad.GET
      def _getBad(self) -> str:
        """Get the bad field."""
        return 'bad'

      @bad.SET
      def _setBad(self, value: str) -> None:
        """Set the bad field."""
        pass

      @extraBad.GET
      def _getExtraBad(self) -> str:
        """Get the 'extraBad' field."""
        return 'yikes!'

      @extraBad.SET
      def _setExtraBad(self, value: str) -> None:
        """Set the 'extraBad' field."""
        pass

    pig = Pig()
    self.assertEqual(pig.good, 'good')
    self.assertEqual(pig.bad, 'bad')
    self.assertEqual(pig.extraBad, 'yikes!')
    pig.good = 'lol setter is noop'
    pig.bad = 'lol setter is noop'
    pig.extraBad = 'lol setter is noop'
    self.assertEqual(pig.good, 'good')
    self.assertEqual(pig.bad, 'bad')
    self.assertEqual(pig.extraBad, 'yikes!')

    setattr(Pig.bad, '__setter_funcs__', 80085)  # Wrong type
    func = lambda *_: None
    setattr(Pig.extraBad, '__setter_funcs__', (func, 420))  # Wrong type

    pig = Pig()

    with self.assertRaises(TypeException) as context:
      pig.bad = 69
    exception = context.exception
    self.assertEqual(exception.varName, '__setter_funcs__')
    self.assertEqual(exception.actualObject, 80085)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], tuple)

    with self.assertRaises(TypeException) as context:
      pig.extraBad = 80085
    exception = context.exception
    self.assertEqual(exception.varName, 'setterFunc')
    self.assertEqual(exception.actualObject, 420)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)

  def test_good_deleter_inherited(self, ) -> None:
    """
    Testing a good deleter for the Field descriptor inherited by a subclass.
    """

    class Pig:
      """
      Class with deletable 'Field': 'sus'
      """
      __sus_object__ = 'u sus!'
      sus = Field()

      @sus.GET
      def _getSus(self) -> str:
        """Get the sus field."""
        return self.__sus_object__

      @sus.DELETE
      def _deleteSus(self) -> None:
        """Delete the sus field."""
        setattr(self, '__sus_object__', DELETED)

    class Ham(Pig):
      """
      Class inheriting from Pig with a deleter for 'sus'.
      """
      pass

    ham = Ham()
    self.assertEqual(ham.sus, 'u sus!')

    del ham.sus

    with self.assertRaises(AttributeError) as context:
      _ = ham.sus
    exception = context.exception
    words = stringList("""AttributeError, ham, object, has, no, sus""")
    for word in words:
      self.assertIn(word.lower(), str(exception).lower())

  def test_bad_deleter(self, ) -> None:
    """
    Testing a bad deleter for the Field descriptor.
    """

    class Pig(AbstractObject):
      """
      Class with a bad deleter for Field: 'bad'.
      """
      __good_object__ = 'good'
      __bad_object__ = 'bad'
      __extra_bad_object__ = 'extra bad'
      good = Field()
      bad = Field()
      extraBad = Field()
      brand = Field()  # Deleter removed

      @good.GET
      def _getGood(self) -> str:
        """Get the good field."""
        return self.__good_object__

      @good.DELETE
      def _deleteGood(self) -> None:
        """Delete the good field."""
        setattr(self, '__good_object__', DELETED)

      @bad.GET
      def _getBad(self) -> str:
        """Get the bad field."""
        return self.__bad_object__

      @bad.DELETE
      def _deleteBad(self) -> None:
        """Delete the bad field."""
        setattr(self, '__bad_object__', DELETED)

      @extraBad.GET
      def _getExtraBad(self) -> str:
        """Get the 'extraBad' field."""
        return self.__extra_bad_object__

      @extraBad.DELETE
      def _deleteExtraBad(self) -> None:
        """Delete the 'extraBad' field."""
        setattr(self, '__extra_bad_object__', DELETED)

      @brand.DELETE
      def _deleteBrand(self) -> None:
        """Subclass replaces this with None. """

      @brand.DELETE
      def _deleteBrand2(self) -> None:
        """Subclass replaces this with wrong type. """

    pig = Pig()
    self.assertEqual(pig.good, 'good')
    self.assertEqual(pig.bad, 'bad')
    self.assertEqual(pig.extraBad, 'extra bad')
    del pig.good
    del pig.bad
    del pig.extraBad
    with self.assertRaises(AttributeError):
      _ = pig.good
    with self.assertRaises(AttributeError):
      _ = pig.bad
    with self.assertRaises(AttributeError):
      _ = pig.extraBad
    pig = Pig()

    class Ham(Pig):
      """
      Class inheriting from Pig with a bad deleter for 'bad'.
      """
      pass

    class Sandwich(Ham):
      """
      Class inheriting from Ham with a bad deleter for 'brand'.
      """
      pass

    setattr(Pig.bad, '__deleter_funcs__', 80085)  # Wrong type
    func = lambda *_: None
    setattr(Pig.extraBad, '__deleter_funcs__', (func, 420))
    setattr(Ham, Pig.brand.__deleter_keys__[0], None)  # None-deleter
    setattr(Sandwich, Pig.brand.__deleter_keys__[0], func)  # None-deleter
    setattr(Sandwich, Pig.brand.__deleter_keys__[1], 1337)  # None-deleter

    pig = Pig()
    ham = Ham()
    sandwich = Sandwich()

    with self.assertRaises(TypeException) as context:
      del pig.bad
    exception = context.exception
    self.assertEqual(exception.varName, '__deleter_funcs__')
    self.assertEqual(exception.actualObject, 80085)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], tuple)

    with self.assertRaises(TypeException) as context:
      del pig.extraBad
    exception = context.exception
    self.assertEqual(exception.varName, 'deleterFunc')
    self.assertEqual(exception.actualObject, 420)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)

    with self.assertRaises(MissingVariable) as context:
      del ham.brand
    exception = context.exception
    self.assertEqual(exception.varName, Pig.brand.__deleter_keys__[0])
    self.assertIs(exception.varType[0], Func)

    with self.assertRaises(TypeException) as context:
      del sandwich.brand
    exception = context.exception
    self.assertEqual(exception.varName, Pig.brand.__deleter_keys__[1])
    self.assertEqual(exception.actualObject, 1337)
    self.assertIs(exception.actualType, int)
    self.assertIs(exception.expectedType[0], Func)

  def test_decorate_non_function(self) -> None:
    """
    Testing that the Field decorator does not allow non-function objects.
    """

    class Foo:
      """Pig is a class with a Field descriptor."""

      bar = Field()

      with self.assertRaises(TypeException) as context:
        bar.GET(69)
      exception = context.exception
      self.assertEqual(exception.varName, 'getterFunc')
      self.assertEqual(exception.actualObject, 69)
      self.assertIs(exception.actualType, int)
      self.assertIs(exception.expectedType[0], Func)

      with self.assertRaises(TypeException) as context:
        bar.SET(420)
      exception = context.exception
      self.assertEqual(exception.varName, 'setterFunc')
      self.assertEqual(exception.actualObject, 420)
      self.assertIs(exception.actualType, int)
      self.assertIs(exception.expectedType[0], Func)

      with self.assertRaises(TypeException) as context:
        bar.DELETE(80085)
      exception = context.exception
      self.assertEqual(exception.varName, 'deleterFunc')
      self.assertEqual(exception.actualObject, 80085)
      self.assertIs(exception.actualType, int)
      self.assertIs(exception.expectedType[0], Func)

  def test_missing_setter(self, ) -> None:
    """
    Testing that the Field descriptor raises MissingVariable when a setter
    is missing.
    """

    class Foo:
      """Foo is a class with a Field descriptor."""
      bar = Field()

      @bar.GET
      def _getBar(self) -> str:
        """Get the bar field."""
        return 'bar'

    foo = Foo()

    with self.assertRaises(ReadOnlyError) as context:
      foo.bar = 69
    exception = context.exception
    self.assertIs(exception.owningInstance, foo)
    self.assertIs(exception.descriptorObject, Foo.bar)
    self.assertEqual(exception.existingValue, 'bar')
    self.assertEqual(exception.newValue, 69)

  def test_write_twice(self) -> None:
    """
    Tries to write to a ComplexField class twice
    """
    z = ComplexField()
    with self.assertRaises(WriteOnceError) as context:
      z.RE = 420.0
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, '__real_part__')
