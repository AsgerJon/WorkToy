"""
TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
AbstractMetaclass from the worktoy.mcls module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests import WYD
from worktoy.core.sentinels import WILDCARD
from worktoy.desc import AttriBox
from worktoy.static import overload
from worktoy.waitaminute.meta import ReservedName
from .. import MCLSTest
from worktoy.core import MetaType, Object
from worktoy.core._meta_type import _Space  # NOQA
from worktoy.mcls import AbstractMetaclass, AbstractNamespace
from worktoy.mcls import BaseMeta, BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never


class TestMetaUmbrella(MCLSTest):
  """
  TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
  AbstractMetaclass from the worktoy.mcls module.
  """

  def testNamespaceDescriptor(self) -> None:
    """
    Test ad-hoc metaclass functionality.
    """
    self.assertIsInstance(MetaType.namespaceClass, _Space)
    self.assertIs(AbstractMetaclass.namespaceClass, AbstractNamespace)

  def testGetNamespace(self) -> None:
    """
    Test ad-hoc metaclass functionality.
    """

    class Bar(metaclass=AbstractMetaclass):
      """Test class with AbstractMetaclass."""
      pass

    space = Bar.getNamespace()
    self.assertIsInstance(space, AbstractNamespace)
    self.assertIs(space.getMetaclass(), AbstractMetaclass)
    self.assertFalse(space.getBases())

  def testNotOverloadedBase(self) -> None:
    """
    Tests the function of subclassing a non-overloaded base class with the
    BaseMeta metaclass.
    """

    class NotOverloaded(Object, metaclass=AbstractMetaclass):
      """A class that is not overloaded."""

      def __init__(self, *args, **kwargs) -> Never:
        raise WYD('breh')

    class Overloaded(NotOverloaded, metaclass=BaseMeta):
      """A class that is overloaded."""

      x = AttriBox[int](0)
      y = AttriBox[int](0)

      @overload(int, int)
      def __init__(self, x: int, y: int) -> None:
        """Overloaded constructor."""
        self.x = x
        self.y = y

      @overload(int)
      def __init__(self, x: int) -> None:
        self.__init__(x, 0)

    with self.assertRaises(WYD):
      _ = NotOverloaded()

    loaded = Overloaded(69, 420)
    self.assertIsInstance(loaded, Overloaded)
    self.assertEqual(loaded.x, 69)
    self.assertEqual(loaded.y, 420)

    loaded2 = Overloaded(69)
    self.assertIsInstance(loaded2, Overloaded)
    self.assertEqual(loaded2.x, 69)
    self.assertEqual(loaded2.y, 0)

  def testSubclassWildcard(self) -> None:
    """
    Tests that an overloaded class using the WILDCARD sentinel to overload
    a function object behaves correctly when subclassed with a class
    extending the overloads.
    """

    class Baseload(BaseObject):
      """A class that is overloaded."""
      x = AttriBox[float](0.0)
      y = AttriBox[float](0.0)
      note = AttriBox[str]('')

      @overload(float, float)
      def __init__(self, x: float, y: float) -> None:
        """Overloaded constructor."""
        self.x = x
        self.y = y
        self.note = 'float, float'

      @overload(float, float, str)
      def __init__(self, x: float, y: float, note: str) -> None:
        """Overloaded constructor with note."""
        self.__init__(x, y)
        self.note = note

      @overload(float, float, WILDCARD)
      def __init__(self, x: float, y: float, wild: Any) -> None:
        """Overloaded constructor with wildcard."""
        self.__init__(x, y, str(wild))

    class Subload(Baseload):
      """A subclass of Baseload with additional overloads."""
      z = AttriBox[float](0.0)

      @overload(float, float, float)
      def __init__(self, x: float, y: float, z: float) -> None:
        """Overloaded constructor with z."""
        self.x = x
        self.y = y
        self.z = z
        self.note = 'float, float, float'

    sub = Subload(0.1337, 0.80085, 0.8008135)
    self.assertIsInstance(sub, Subload)
    self.assertAlmostEqual(sub.x, 0.1337)
    self.assertAlmostEqual(sub.y, 0.80085)
    self.assertAlmostEqual(sub.z, 0.8008135)
    base = Baseload(0.69, 0.420, )
    self.assertIsInstance(base, Baseload)
    self.assertAlmostEqual(base.x, 0.69)
    self.assertAlmostEqual(base.y, 0.420)
    base2 = Baseload(0.69, 0.420, 'test')
    self.assertIsInstance(base2, Baseload)
    self.assertAlmostEqual(base2.x, 0.69)
    self.assertAlmostEqual(base2.y, 0.420)
    self.assertEqual(base2.note, 'test')
    base3 = Baseload(0.69, 0.420, object)
    self.assertIsInstance(base3, Baseload)
    self.assertAlmostEqual(base3.x, 0.69)
    self.assertAlmostEqual(base3.y, 0.420)
    self.assertEqual(base3.note, str(object))

  def testReservedName(self) -> None:
    """
    Tests that reserved names like '__init_subclass__' are not used in
    AbstractMetaclass.
    """

    with self.assertRaises(ReservedName) as context:
      class Trololololo(metaclass=AbstractMetaclass):
        __module__ = '__main__'
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def testMetaSubclass(self) -> None:
    """
    Tests that the AbstractMetaclass can be subclassed.
    """

    self.assertIsSubclass(AbstractMetaclass, MetaType)
    self.assertIsNotSubclass(int, AbstractMetaclass)

  def testAbstractNamespace(self) -> None:
    """
    Tests that AbstractNamespace can be instantiated and behaves as expected.
    """

    class TestNamespace(Object, metaclass=AbstractMetaclass):
      """A test namespace for AbstractNamespace."""
      pass

    space = TestNamespace.__namespace__
    self.assertIsInstance(space, AbstractNamespace)
    for key, val in space.getGlobalScope().items():
      infoSpec = """%20s: %s"""
      typeStr = str(val)
      if len(typeStr) > 40:
        typeStr = typeStr[:37] + '...'
      else:
        typeStr = typeStr.ljust(40)
      info = infoSpec % (key, typeStr)

  def testAbstractNamespaceGlobalScope(self) -> None:
    """
    Tests that the global scope of AbstractNamespace behaves as expected.
    """

    class Foo:
      pass

    class Breh(Object, metaclass=AbstractMetaclass):
      """A test class for AbstractNamespace global scope."""
      x = AttriBox[int](0)
      y = AttriBox[int](0)

    with self.assertRaises(RuntimeError) as context:
      _ = Breh.__namespace__.__global_scope__
    e = context.exception
    self.assertIn('Direct access to the', str(e))
    self.assertIn('__global_scope__', str(e))

    Breh.__namespace__.setTypeAnnotation('lmao', True)
    Breh.__namespace__.setTypeAnnotation('lmao', False)
    Breh.__namespace__.setTypeAnnotation('lmao', False)

    Breh.__namespace__.setDeferredAnnotation('lol', 'bool')
    Breh.__namespace__.setDeferredAnnotation('lol', 'int')
    Breh.__namespace__.setDeferredAnnotation('lol', 'int')

    Breh.__namespace__.setAnnotation('haha', 'trolololololo')

    Breh.__namespace__.setClassAnnotation({'lmao': 'bool'})
    Breh.__namespace__.setClassAnnotation({'lmao': 'int'})
    Breh.__namespace__.setClassAnnotation({'lmao': 'float'})

    Breh.__namespace__.resolveType('annotations')

    lol = AbstractNamespace(AbstractMetaclass, 'lol', ())
    object.__setattr__(lol, '__global_scope__', dict(lmao=True))
    lol.resolveType('lmao')
