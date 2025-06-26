"""
TestBasicMeta tests some basic functionalities of the AbstractMetaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING, Iterator

from worktoy.mcls import AbstractMetaclass, BaseMeta, AbstractNamespace
from worktoy.parse import maybe
from worktoy.waitaminute import QuestionableSyntax, DelException
from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestBasicMeta(TestCase):
  """
  TestBasicMeta tests some basic functionalities of the AbstractMetaclass.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_class(self) -> None:
    """
    Test that the metaclass is set correctly.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with AbstractMetaclass as its metaclass.
      """

      def __getitem__(self, item: Any) -> Any:
        """
        Get an item from the class.
        """

      def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set an item in the class.
        """

      def __set_name__(self, name: str, owner: type) -> None:
        """
        Set the name of the class.
        """

    self.assertIsInstance(Foo, BaseMeta)
    self.assertEqual(str(Foo), """Foo[metaclass=BaseMeta]""")

    class Bar(Foo):
      """
      Bar is a subclass of Foo.
      """
      pass

    self.assertTrue(issubclass(Bar, Foo))

    class NoSub(Exception):
      """
      Custom test exception
      """

      cls = _Attribute()
      sub = _Attribute()

      def __init__(self, cls: type, sub: type) -> None:
        self.cls = cls
        self.sub = sub
        Exception.__init__(self, )

    class IHaveNoSubclasses(metaclass=BaseMeta):
      """
      NoSub is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_subclasscheck__(cls, other: type) -> bool:
        """
        Class subclass check.
        """
        raise NoSub(cls, other)

    with self.assertRaises(NoSub) as context:
      issubclass(object, IHaveNoSubclasses)
    e = context.exception
    self.assertIs(e.cls, IHaveNoSubclasses)
    self.assertIs(e.sub, object)

  def test_bad_class(self) -> None:
    """
    Test that the metaclass is set correctly.
    """

    with self.assertRaises(QuestionableSyntax) as context:
      class Foo(metaclass=AbstractMetaclass):
        """
        Foo is a class with AbstractMetaclass as its metaclass.
        """

        def __get_item__(self, item: Any) -> Any:
          """
          Get an item from the class.
          """
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.derpName, '__get_item__')
    self.assertEqual(e.realName, '__getitem__')

  def test_str_repr(self) -> None:
    """
    Test the string representation of the metaclass.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """
      pass

    self.assertEqual(str(Foo), """Foo[metaclass=BaseMeta]""")
    self.assertEqual(repr(Foo), str(Foo))

    class Bar(metaclass=BaseMeta):
      """
      Bar is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_str__(cls, ) -> str:
        """
        Class string representation.
        """
        return """Based class: %s""" % cls.__name__

      __class_repr__ = __class_str__

    self.assertEqual(str(Bar), """Based class: Bar""")
    self.assertEqual(repr(Bar), str(Bar))

  def test_good_iteration(self) -> None:
    """
    Test that the metaclass supports iteration.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_iter__(cls) -> Iterator[int]:
        """
        Iterate over the class.
        """
        yield from range(3)

    self.assertEqual(list(Foo), [0, 1, 2])

  def test_bad_iteration(self) -> None:
    """
    Test that the metaclass raises an error when iteration is not supported.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

    with self.assertRaises(TypeError) as context:
      _ = list(Foo)
    e = context.exception
    self.assertEqual(str(e), """'Foo' object is not iterable""")

  def test_good_old_fashioned_iteration(self, ) -> None:
    """
    Testing the old-fashioned iteration method by implementing both
    __class_iter__ and __class_next__ methods.
    """

    someValues = [69, 420, 1337, 80085, 8008135]

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

      __iter_contents__ = None

      @classmethod
      def __class_iter__(cls) -> Iterator[int]:
        """
        Iterate over the class.
        """
        cls.__iter_contents__ = [*someValues, ]
        return cls

      @classmethod
      def __class_next__(cls) -> int:
        """
        Get the next item in the iteration.
        """
        return cls.__iter_contents__.pop(0)

    for someValue, item in zip(someValues, Foo):
      self.assertEqual(someValue, item)

  def test_bad_old_fashioned_iteration(self) -> None:
    """
    Testing the old-fashioned iteration method by implementing
    __class_iter__ but neglecting to implement __class_next__.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_iter__(cls) -> Iterator[int]:
        """
        Iterate over the class.
        """
        return cls

    with self.assertRaises(AttributeError) as context:
      _ = list(Foo)
    e = context.exception
    expected = """object has no attribute '__next__'"""
    self.assertIn(expected, str(e))

    with self.assertRaises(TypeError) as context:
      _ = len(Foo)
    e = context.exception
    expected = """object has no len()"""
    self.assertIn(expected, str(e))

  def test_very_bad_old_fashioned_iteration(self) -> None:
    """
    Testing old-fashioned iteration method where the class decides to do a
    bit of trolling during its '__class_next__' method.
    """

    class Trolololololo(Exception):
      pass

    class Derp(metaclass=BaseMeta):
      """
      Derp is a class that appears iterable, but then throws an unexpected
      error when AbstractMetaclass falls back to it when we try to get its
      length.
      """

      @classmethod
      def __class_iter__(cls) -> Self:
        """
        Iterate over the class.
        """
        return cls

      @classmethod
      def __class_next__(cls) -> int:
        """
        Get the next item in the iteration.
        """
        raise Trolololololo

    with self.assertRaises(Trolololololo) as context:
      _ = len(Derp)

  def test_hash(self, ) -> None:
    """
    Test that the metaclass supports hashing.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_hash__(cls) -> int:
        """
        Hash the class.
        """
        return 69420

    self.assertEqual(hash(Foo), 69420)

    class Bar(metaclass=BaseMeta):
      """
      Bar is a class with BaseMeta as its metaclass.
      """

    expectedHash = hash(('Bar', 'object', 'BaseMeta'))
    self.assertEqual(hash(Bar), expectedHash)

  def test_eq(self) -> None:
    """
    Test that the metaclass supports equality checks.
    """

    class Foo(metaclass=BaseMeta):
      """
      Foo is a class with BaseMeta as its metaclass.
      """

      @classmethod
      def __class_eq__(cls, other: Any) -> bool:
        """
        Check equality of the class.
        """
        return cls.__name__ == other.__name__

    space = AbstractNamespace(BaseMeta, 'Foo', (), )
    breh = BaseMeta('Foo', (), space)

    self.assertTrue(Foo == Foo)
    self.assertTrue(Foo == breh)
    self.assertFalse(Foo == object)
    self.assertFalse(Foo == 42)
    eqTest = BaseMeta.__eq__(Foo, """I'm Foo bro, trust!""")
    self.assertIs(eqTest, NotImplemented)

  def test_good_del(self) -> None:
    """
    Test that the metaclass supports deletion.
    """

    class DeleteMe(trustMeBro=True, metaclass=BaseMeta):
      """
      DeleteMe is a class that implements __del__.
      """

      __deleted_objects__ = None

      @classmethod
      def _registerDeletedObject(cls, obj: Any) -> None:
        """
        Register a deleted object.
        """
        existing = cls._getDeletedObjects()
        cls.__deleted_objects__ = [*existing, str(obj)]

      @classmethod
      def _getDeletedObjects(cls) -> list[Any]:
        """
        Get the list of deleted objects.
        """
        return maybe(cls.__deleted_objects__, [])

      def __del__(self, ) -> None:
        """
        Delete the class.
        """
        type(self)._registerDeletedObject(self)

    delMe = DeleteMe()
    delMeStr = str(delMe)
    del delMe
    import gc
    gc.collect()
    self.assertIn(delMeStr, DeleteMe._getDeletedObjects())

  def test_bad_del(self) -> None:
    """
    Test that the metaclass raises an error when deletion is not supported.
    """

    with self.assertRaises(DelException) as context:
      class Sus(metaclass=BaseMeta):
        """
        Tries to implement __del__...
        """

        def __del__(self, ) -> None:
          """
          Trust me bro, I can delete myself!
          """
    e = context.exception
    self.assertIs(e.mcls, BaseMeta)
    self.assertEqual(e.name, 'Sus')
    self.assertEqual(e.bases, ())

  def test_dict_space(self) -> None:
    """
    Test that the metaclass supports creation with a standard 'dict'
    instead of the 'AbstractNamespace' returned from its '__prepare__'
    method.
    """

    Foo = BaseMeta('Foo', (), {})
    self.assertIsInstance(Foo, BaseMeta)
