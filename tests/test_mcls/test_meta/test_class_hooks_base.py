"""
TestClassHooksBase tests that classes derived from 'AbstractMetaclass' that
implement the '__class_[HOOK]__' methods are called correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import MCLSTest
from worktoy.mcls import AbstractMetaclass
from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


class Name(Object):
  """
  Descriptor class for method names.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __pvt_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def _getPrivateName(self) -> str:
    """
    Get the private name of the descriptor.
    """
    return self.__pvt_name__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def __init__(self, name: str) -> None:
    """
    Initialize the Name descriptor with the given name.
    """
    super().__init__()
    self.__pvt_name__ = name

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, *args, **kwargs, ) -> Any:
    """
    Get the instance of the descriptor.
    """
    pvtName = self._getPrivateName()
    return getattr(self.instance, pvtName)


class ClassLevelCalled(Exception):
  """Raised by __class_...__ hooks to prove they were called."""
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __method_name__ = None

  #  Public Variables
  methodName = Name('__method_name__')

  def __init__(self, functionName: str, *args, **kwargs) -> None:
    """
    Initialize the ClassLevelCalled exception with the function name.
    """
    self.__method_name__ = functionName
    Exception.__init__(self, functionName)


class ClassHooks(metaclass=AbstractMetaclass):
  """
  Class derived from AbstractMetaclass that implements the
  '__class_[HOOK]__' methods to raise ClassLevelCalled exceptions.
  """

  @classmethod
  def __class_call__(cls, *args: Any, **kwargs: Any) -> Any:
    raise ClassLevelCalled("call", args, kwargs)

  @classmethod
  def __class_getattr__(cls, name: str, exc: Exception = None) -> Any:
    raise ClassLevelCalled("getattr", name)

  @classmethod
  def __class_setattr__(cls, name: str, value: Any) -> None:
    raise ClassLevelCalled("setattr", name, value)

  @classmethod
  def __class_delattr__(cls, name: str) -> None:
    raise ClassLevelCalled("delattr", name)

  @classmethod
  def __class_getitem__(cls, key: Any) -> Any:
    raise ClassLevelCalled("getitem", key)

  @classmethod
  def __class_setitem__(cls, key: Any, value: Any) -> None:
    raise ClassLevelCalled("setitem", key, value)

  @classmethod
  def __class_delitem__(cls, key: Any) -> None:
    raise ClassLevelCalled("delitem", key)

  @classmethod
  def __class_str__(cls) -> str:
    raise ClassLevelCalled("str")

  @classmethod
  def __class_repr__(cls) -> str:
    raise ClassLevelCalled("repr")

  @classmethod
  def __class_instancecheck__(cls, obj: Any) -> bool:
    raise ClassLevelCalled("instancecheck", obj)

  @classmethod
  def __class_subclasscheck__(cls, sub: type) -> bool:
    raise ClassLevelCalled("subclasscheck", sub)

  @classmethod
  def __class_iter__(cls) -> Iterator[str]:
    raise ClassLevelCalled("iter")

  @classmethod
  def __class_next__(cls) -> str:
    raise ClassLevelCalled("next")


class TestClassHooks(MCLSTest):
  """
  TestClassHooks tests that classes derived from 'AbstractMetaclass' that
  implement the '__class_[HOOK]__' methods are called correctly.
  """

  def test_call(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      ClassHooks("a", b=2)
    self.assertEqual(cm.exception.methodName, "call")

  def test_getattr(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      _ = ClassHooks.sus
    self.assertEqual(cm.exception.methodName, "getattr")

  def test_setattr(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      ClassHooks.sus = 42
    self.assertEqual(cm.exception.methodName, "setattr")

  def test_delattr(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      del ClassHooks.sus
    self.assertEqual(cm.exception.methodName, "delattr")

  def test_getitem(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      _ = ClassHooks["thing"]
    self.assertEqual(cm.exception.methodName, "getitem")

  def test_setitem(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      ClassHooks["thing"] = 123
    self.assertEqual(cm.exception.methodName, "setitem")

  def test_delitem(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      del ClassHooks["thing"]
    self.assertEqual(cm.exception.methodName, "delitem")

  def test_str(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      str(ClassHooks)
    self.assertEqual(cm.exception.methodName, "str")

  def test_repr(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      repr(ClassHooks)
    self.assertEqual(cm.exception.methodName, "repr")

  def test_instancecheck(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      isinstance("x", ClassHooks)
    self.assertEqual(cm.exception.methodName, "instancecheck")

  def test_subclasscheck(self) -> None:
    class Foo:
      pass

    with self.assertRaises(ClassLevelCalled) as cm:
      issubclass(Foo, ClassHooks)
    self.assertEqual(cm.exception.methodName, "subclasscheck")

  def test_iter(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      iter(ClassHooks)
    self.assertEqual(cm.exception.methodName, "iter")

  def test_next(self) -> None:
    with self.assertRaises(ClassLevelCalled) as cm:
      next(ClassHooks)
    self.assertEqual(cm.exception.methodName, "next")
