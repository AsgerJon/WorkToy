"""TestAbstractMetaclass test the AbstractMetaclass class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import QuestionableSyntax

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self


class Integer(metaclass=AbstractMetaclass):
  """Representation of integer."""

  __fallback_value__ = 0
  __number_value__ = None

  __sub_cls__ = []

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, int):
        self.__number_value__ = arg
        break
    else:
      self.__number_value__ = self.__fallback_value__

  @classmethod
  def __class_instancecheck__(cls, obj: object) -> bool:
    """Check if the object is an instance of Integer."""
    if type(obj) is cls:
      return True
    if isinstance(obj, int):
      return True
    if isinstance(obj, float):
      return True if obj.is_integer() else False
    if isinstance(obj, complex):
      if abs(obj) < 1e-12:
        return True
      if obj.real > 1e-12 and obj.imag > 1e-12:
        return False
      return cls.__class_instancecheck__(max(obj.real, obj.imag))
    return False

  @classmethod
  def __class_subclasscheck__(cls, other: type) -> bool:
    """Check if the object is a subclass of Integer."""
    if not isinstance(other, type):
      return False
    return True if cls in other.__mro__ else False

  @classmethod
  def __subclasshook__(cls, __subclass) -> bool:
    """Check if the subclass is an instance of Integer."""
    cls.__sub_cls__.append(__subclass)
    return object.__subclasshook__(__subclass)

  def __int__(self, ) -> int:
    """Convert the object to an integer."""
    return self.__number_value__


class TestAbstractMetaclass(TestCase):
  """Test the AbstractMetaclass class."""

  def setUp(self, ) -> None:
    """Set up the test case."""
    super().setUp()
    AbstractMetaclass._validateNamespace(dict())

  def test_abstract_metaclass(self) -> None:
    """Test the AbstractMetaclass class."""
    expectedName = 'AbstractMetaclass[metaclass=_MetaMetaclass]'
    self.assertEqual(str(AbstractMetaclass), expectedName)

  def test_syntax_error(self, ) -> None:
    """Tests the syntax error in the AbstractMetaclass class."""

    with self.assertRaises(SyntaxError) as context:
      class Breh(metaclass=AbstractMetaclass):
        """Test the AbstractMetaclass class."""

        def __del__(self, *args) -> None:
          """Test the AbstractMetaclass class."""
          print('derp')

  def test_questionable_syntax(self, ) -> None:
    """Tests the syntax error in the AbstractMetaclass class."""

    with self.assertRaises(QuestionableSyntax) as context:
      class Breh(metaclass=AbstractMetaclass):
        """Test the AbstractMetaclass class."""

        def __get_item__(self, *args) -> None:
          """Test the AbstractMetaclass class."""
          print('derp')

      self.assertEqual(context.exception.derpName, '__get_item__')
      self.assertEqual(context.exception.realName, '__getitem__')

  def test_instance_check(self, ) -> None:
    """Tests that the Integer class correctly identifies integers as being
    instance of itself. """
    self.assertIsInstance(69, Integer)
    self.assertIsInstance(420.0, Integer)

  def test_subclasshook(self, ) -> None:
    """Tests that the AbstractMetaclass correctly notifies baseclass
    of subclass creation."""

    class Prime(Integer):
      """Prime class."""

      __iter_contents__ = None
      __member_numbers__ = None

      @classmethod
      def getMembers(cls, **kwargs) -> list[int]:
        """Getter-function for the list of prime members."""
        if cls.__member_numbers__ is None:
          if kwargs.get('_recursion', False):
            raise RecursionError
          cls.__member_numbers__ = cls.loadMembers()
          return cls.getMembers(_recursion=True)
        return cls.__member_numbers__

      @classmethod
      def addMember(cls, p: int) -> None:
        """Add a prime member."""
        if cls.__member_numbers__ is None:
          cls.__member_numbers__ = []
        cls.__member_numbers__.append(p)
        cls.__member_numbers__.sort()

      @classmethod
      def loadMembers(cls, ) -> list[int]:
        """Get the prime members."""
        here = os.path.dirname(__file__)
        fileName = 'primes.txt'
        fid = os.path.join(here, fileName)
        if os.path.exists(fid):
          with open(fid, 'r') as f:
            return [int(line.strip()) for line in f.readlines()]
        return []

      @classmethod
      def saveMembers(cls, ) -> None:
        """Save the prime members."""
        here = os.path.dirname(__file__)
        fileName = 'primes.txt'
        fid = os.path.join(here, fileName)
        with open(fid, 'w') as f:
          for p in cls.getMembers():
            f.write('%d\n' % p)

      @classmethod
      def nextPrime(cls, p: int = None) -> int:
        """Returns the next prime number."""
        if p is None:
          p = (cls.getMembers() or [0])[-1]
        if p in [0, 1]:
          return cls.nextPrime(p + 1)
        if p in cls.getMembers():
          return p
        while (cls.getMembers() or [0])[-1] < p:
          cls.nextPrime()
        for f in cls.getMembers():
          if p % f:
            continue
          break
        else:
          cls.addMember(p)
          cls.saveMembers()
          return p
        return cls.nextPrime(p + 1 + p % 2)

      def __init__(self, *_) -> None:
        """Prime class constructor."""
        Integer.__init__(self, self.nextPrime())

      @classmethod
      def __class_iter__(cls, ) -> Self:
        """Iterate over the prime members."""
        cls.__iter_contents__ = [*cls.getMembers()]
        return cls

      @classmethod
      def __class_next__(cls, ) -> int:
        """Get the next prime member."""
        if cls.__iter_contents__:
          return cls.__iter_contents__.pop(0)
        cls.__iter_contents__ = None
        raise StopIteration

      @classmethod
      def __class_call__(cls, *args) -> Self:
        """Call the class."""
        if args:
          return cls.nextPrime(args[0])
        return cls.nextPrime()

      @classmethod
      def __class_instancecheck__(cls, instance) -> bool:
        """Check if the instance is an instance of Integer."""
        base = cls.__bases__[0]
        if not base.__class_instancecheck__(instance):
          return False
        if isinstance(instance, int):
          return True if int(instance) in cls.getMembers() else False
        return True if int(abs(instance)) in cls.getMembers() else False

    self.assertTrue(issubclass(Prime, Integer))
    self.assertIsInstance(73, Integer)
    self.assertIsInstance(73.0, Integer)
    self.assertIsInstance(0.0 + 73j, Integer)
    self.assertNotIsInstance(1 / 2, Integer)
    self.assertNotIsInstance(69 + 420j, Integer)
    self.assertIsInstance(73, Prime)
    self.assertIsInstance(73.0, Prime)
    self.assertIsInstance(0.0 + 73j, Prime)
    self.assertNotIsInstance(77, Prime)
    self.assertNotIsInstance(0, Prime)
    self.assertNotIsInstance(1, Prime)
    self.assertEqual(73, Prime(72))
