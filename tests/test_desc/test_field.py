"""TestField tests the Field descriptor functionality."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescTest
from tests.test_desc import ComplexField
from worktoy.desc import Field
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.utilities import maybe, stringList
from worktoy.static import overload
from worktoy.core.sentinels import THIS, DELETED
from worktoy.core import Object
from worktoy.utilities.mathematics import pi
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError
from worktoy.waitaminute.desc import AccessError
from worktoy.waitaminute import TypeException, attributeErrorFactory
from worktoy.waitaminute import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class R2(metaclass=BaseMeta):
  """R2 is a class that represents a point in the plane."""

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


class TestField(DescTest):
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
    with self.assertRaises(ProtectedError) as context:
      del self.R2_0.r0
    e = context.exception
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(ProtectedError) as context:
      del self.R2_0.r1
    e = context.exception
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(ProtectedError) as context:
      del self.C_0.r0
    e = context.exception
    self.assertEqual(str(e), repr(e))
    with self.assertRaises(ProtectedError) as context:
      del self.C_0.r1
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def test_no_key(self, ) -> None:
    """Tests that the correct errors are raised."""

    class KeysScumbag:
      """
      The universal symbol for keys.
      """
      mrFFFFFF = Field()

    FF0088 = KeysScumbag()
    with self.assertRaises(AccessError) as context:
      _ = FF0088.mrFFFFFF
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, KeysScumbag.mrFFFFFF)

    setattr(KeysScumbag.mrFFFFFF, '__get_key__', 80085)

    with self.assertRaises(TypeException) as context:
      _ = FF0088.mrFFFFFF

    e = context.exception
    self.assertEqual(e.varName, '__get_key__')
    self.assertIs(e.actualType, int)
    self.assertIs(e.expectedTypes[0], str)

  def test_bad_setter_key_type(self) -> None:
    """Tests that the correct errors are raised."""

    class Foo:
      """
      Foo is a class with a Field descriptor.
      """

      __ham_value__ = None

      bar = Field()
      eggs = Field()
      ham = Field()

      @ham.GET
      def _getHam(self) -> Any:
        if self.__ham_value__ is None:
          attributeError = attributeErrorFactory('Foo', 'ham')
          raise attributeError
        return self.__ham_value__

      @ham.SET
      def _setHam(self, value: Any) -> None:
        self.__ham_value__ = value

      @ham.DELETE
      def _deleteHam(self) -> None:
        """Delete the ham field."""
        raise ProtectedError(self, type(self).ham, 'get rect!')

    setattr(Foo.bar, '__set_keys__', [69, 420])
    setattr(Foo.bar, '__delete_keys__', [1337, 80085])
    setattr(Foo.eggs, '__set_keys__', ('imma key, trust!',))
    setattr(Foo.eggs, '__delete_keys__', ('imma key, trust!',))
    foo = Foo()
    with self.assertRaises(TypeError) as context:
      foo.bar = 80085
    exception = context.exception
    expected = """attribute name must"""
    self.assertIn(expected, str(exception))

    with self.assertRaises(AttributeError) as context:
      foo.eggs = 8008135
    exception = context.exception
    expected = """has no attribute"""
    self.assertIn(expected, str(exception))

    with self.assertRaises(AttributeError) as context:
      del foo.bar
    exception = context.exception
    expected = """'Foo' object has no attribute 'bar'"""
    self.assertIn(expected, str(exception))

    with self.assertRaises(AttributeError) as context:
      del foo.eggs
    exception = context.exception
    expected = """'Foo' object has no attribute 'eggs'"""
    self.assertIn(expected, str(exception))

    #  Deleting when no value is present, raises AttributeError
    with self.assertRaises(AttributeError) as context:
      del foo.ham
    exception = context.exception
    expected = """'Foo' object has no attribute 'ham'"""
    self.assertIn(expected, str(exception))

    foo.ham = 69
    #  With a value set, trying to delete invokes the decorated deleter,
    #  this particular one raises ProtectedError

    with self.assertRaises(ProtectedError) as context:
      del foo.ham
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.ham)
    self.assertEqual(e.oldVal, 'get rect!')

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

  def test_no_setter(self) -> None:
    """Tests a class without setters at a descriptor"""

    class SetMeNot(Object):
      """SetMeNot is a class with a Field descriptor without a setter."""
      __foo_val__ = 69
      foo = Field()

      def __init__(self, val: int = None) -> None:
        """Initialize the SetMeNot object."""
        self.__foo_val__ = maybe(val, self.__foo_val__)

      @foo.GET
      def _getFoo(self) -> int:
        return self.__foo_val__

    setMeNot = SetMeNot()
    self.assertEqual(setMeNot.foo, 69)
    with self.assertRaises(ReadOnlyError) as context:
      setMeNot.foo = 420
    e = context.exception
    self.assertIs(e.instance, setMeNot)
    self.assertIs(e.desc, SetMeNot.foo)
    self.assertEqual(e.newVal, 420)
    with self.assertRaises(ProtectedError) as context:
      del setMeNot.foo
    e = context.exception
    self.assertIs(e.instance, setMeNot)
    self.assertIs(e.desc, SetMeNot.foo)

  def test_deleter(self) -> None:
    """Tests a deleter that it works and raises when no value to delete"""

    class YeetMeNot(Object):
      """YeetMeNot is a class with a Field descriptor with a deleter."""
      __foo_val__ = 69
      foo = Field()

      def __init__(self, val: int = None) -> None:
        """Initialize the YeetMeNot object."""
        self.__foo_val__ = maybe(val, self.__foo_val__)

      @foo.GET
      def _getFoo(self) -> int:
        return self.__foo_val__

      @foo.DELETE
      def _deleteFoo(self) -> None:
        """Delete the foo field."""
        setattr(self, '__foo_val__', DELETED)

    yeetMeNot = YeetMeNot()
    self.assertEqual(yeetMeNot.foo, 69)
    del yeetMeNot.foo
    with self.assertRaises(AttributeError) as context:
      _ = yeetMeNot.foo
    exception = context.exception
    expected = 'has no attribute'
    self.assertIn(expected, str(exception))
    with self.assertRaises(AttributeError) as context:
      del yeetMeNot.foo
    exception = context.exception
    expected = 'has no attribute'
    self.assertIn(expected, str(exception))

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

    class Pig(Object):
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

    func = lambda *_: None
    setattr(Ham, Pig.brand.__delete_keys__[0], None)  # None-deleter
    setattr(Sandwich, Pig.brand.__delete_keys__[0], func)  # None-deleter
    setattr(Sandwich, Pig.brand.__delete_keys__[1], 1337)  # None-deleter

    pig = Pig()
    ham = Ham()
    sandwich = Sandwich()

  def test_decorate_non_function(self) -> None:
    """
    Testing that the Field decorator does not allow non-function objects.
    """

    class Foo:
      """Pig is a class with a Field descriptor."""

      bar = Field()

      with self.assertRaises(AttributeError) as context:
        bar.GET(69)
      exception = context.exception
      expected = """'int' object has no attribute '__name__'"""
      self.assertIn(expected, str(exception))

      with self.assertRaises(AttributeError) as context:
        bar.SET(420)
      exception = context.exception
      expected = """'int' object has no attribute '__name__'"""
      self.assertIn(expected, str(exception))

      with self.assertRaises(AttributeError) as context:
        bar.DELETE(80085)
      exception = context.exception
      expected = """'int' object has no attribute '__name__'"""
      self.assertIn(expected, str(exception))

  def test_write_twice(self) -> None:
    """
    Tries to write to a ComplexField class twice
    """
    z = ComplexField()

    with self.assertRaises(WriteOnceError) as context:
      z.RE = 420.0
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.desc, ComplexField.RE)

  def test_complex_field(self) -> None:
    """
    Tests the ComplexField class.
    """
    z = ComplexField(69.0, 420.0, )
    self.assertAlmostEqual(abs(z) ** 2, 69 ** 2 + 420 ** 2)
    self.assertAlmostEqual(z.ABS ** 2, 69 ** 2 + 420 ** 2)
    z = ComplexField(1 + 1j)
    self.assertAlmostEqual(z.ARG * 4, pi)
    z = ComplexField(1 + 0j)
    self.assertAlmostEqual(z.ARG, 0.0)
    z = ComplexField(0 + 1j)
    self.assertAlmostEqual(z.ARG, pi / 2)

  def test_zero_arg(self) -> None:
    """
    Tests that the argument of a zero complex number is zero.
    """
    z = ComplexField(0.0, 0.0)
    self.assertFalse(z)
    self.assertAlmostEqual(z.ABS, 0.0)
    with self.assertRaises(ZeroDivisionError):
      _ = z.ARG

  def test_write_once(self) -> None:
    """
    Tests that the ComplexField class raises WriteOnceError when trying to
    write to a read-only field.
    """
    z = ComplexField(69.0, 420.0)
    with self.assertRaises(WriteOnceError) as context:
      z.RE = 80085.0
    e = context.exception
    self.assertIs(e.desc, ComplexField.RE)
    self.assertEqual(e.oldValue, 69.0)
    self.assertEqual(e.newValue, 80085.0)
    with self.assertRaises(WriteOnceError) as context:
      z.IM = 80085.0
    e = context.exception
    self.assertIs(e.desc, ComplexField.IM)
    self.assertEqual(e.oldValue, 420.0)
    self.assertEqual(e.newValue, 80085.0)

  def test_int_init(self) -> None:
    """
    Tests that the ComplexField class can be initialized with integers.
    """
    z = ComplexField(69, 420)
    self.assertAlmostEqual(z.RE, 69.0)
    self.assertAlmostEqual(z.IM, 420.0)
    z = ComplexField(z)
    self.assertAlmostEqual(z.RE, 69.0)
    self.assertAlmostEqual(z.IM, 420.0)
    z = ComplexField(69)
    self.assertAlmostEqual(z.RE, 69.0)
    self.assertAlmostEqual(z.IM, 0.0)
    z = ComplexField((69.0, 420.0), )
    self.assertAlmostEqual(z.RE, 69.0)
    self.assertAlmostEqual(z.IM, 420.0)
