"""
TestKeeFlagsMeta tests the KeeFlagsMeta metaclass functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute.keenum import KeeFlagDuplicate
from worktoy.keenum import KeeFlags, KeeFlag, KeeFlagsMeta, KeeNum
from worktoy.desc import Field
from worktoy.utilities import perm
from .examples import SubclassExample, FlagsExample, MouseButton, PrimeValued
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeFlagsMeta(KeeTest):
  """
  TestKeeFlagsMeta tests the KeeFlagsMeta metaclass functionality.
  """

  def testExamples(self, ) -> None:
    """Tests the existence of example KeeFlags classes."""
    for Flags in self.exampleFlags:
      self.assertTrue(issubclass(Flags, KeeFlags))
      self.assertTrue(isinstance(Flags, KeeFlagsMeta))

  def testMeta(self) -> None:
    """
    Tests that 'KeeFlagsMeta' correctly implements the 'valueType' field.
    """
    metaAttributes = dict(
      flags=Field,
      memberList=Field,
      memberDict=Field,
      valueType=Field,
      )
    for key, value in metaAttributes.items():
      self.assertTrue(hasattr(KeeFlagsMeta, key))
      self.assertIsInstance(getattr(KeeFlagsMeta, key), value)

  def testLen(self, ) -> None:
    """Tests that '__len__' correctly returns the number of members."""
    for cls in self.exampleFlags:
      self.assertEqual(len(cls), 2 ** len(cls.flags))

  def testContains(self, ) -> None:
    """Tests that '__contains__' correctly identifies members."""

    for cls in self.exampleFlags:
      for i, p in enumerate(perm(*cls.flags, )):
        key = frozenset((p.name for p in p))
        index = sum(1 << f.index for f in p)
        name = '_'.join(f.name for f in p) or 'NULL'
        self.assertIn(key, cls)
        self.assertIn(index, cls)
        self.assertIn(name, cls)
      for sus in self.exampleFlags:
        if issubclass(sus, cls) or issubclass(cls, sus) or cls is sus:
          continue
        for member in sus:
          if member.name == 'NULL':
            continue
          self.assertNotIn(member, cls)

  def testBasicSubclassCheck(self, ) -> None:
    """
    Tests that KeeFlagsMeta derived classes correctly identify themselves
    as subclasses of themselves.
    """
    for cls in self.exampleFlags:
      self.assertIsSubclass(cls, cls)

  def testIsSubclassCheck(self, ) -> None:
    """
    Tests that KeeFlagsMeta derived classes correctly identify subclasses.
    """
    self.assertIsSubclass(SubclassExample, FlagsExample)
    self.assertIsNotSubclass(FlagsExample, SubclassExample)

    class Base(KeeFlags):
      A = KeeFlag()

    class SubB(Base):
      B = KeeFlag()

    class SubC(SubB):
      C = KeeFlag()

    class SubD(SubC):
      D = KeeFlag()

    subception = [SubB, SubC, SubD]
    for sub in subception:
      self.assertIsSubclass(sub, Base)

  def testNotSubclassCheck(self, ) -> None:
    """
    Tests that KeeFlagsMeta derived classes correctly rejects unrelated
    classes as subclasses.
    """

    susClasses = [type(self), type('Sus', (), {}), KeeFlags, KeeNum]
    for cls in self.exampleFlags:
      for sus in susClasses:
        self.assertNotIsSubclass(sus, cls)

  def testAdvancedSubclassCheck(self, ) -> None:
    """
    Tests more advanced subclass checks with two separate hierarchies.
    """

    class Base(KeeFlags):
      Z = KeeFlag()

    class Sus1A(Base):
      A = KeeFlag()

    class Sus1B(Sus1A):
      B = KeeFlag()

    class Sus1C(Sus1B):
      C = KeeFlag()

    class Sus1D(Sus1C):
      D = KeeFlag()

    class Sus2A(KeeFlags):
      A = KeeFlag()

    class Sus2B(Sus2A):
      B = KeeFlag()

    class Sus2C(Sus2B):
      C = KeeFlag()

    class Sus2D(Sus2C):
      D = KeeFlag()

    sus1 = [Sus1A, Sus1B, Sus1C, Sus1D]
    sus2 = [Sus2A, Sus2B, Sus2C, Sus2D]

    s1, s2 = [*reversed(sus1), ], [*reversed(sus2), ]
    while s1:
      b = s1.pop()
      for s in s1:
        self.assertIsSubclass(s, b)
      for s in sus2:
        self.assertNotIsSubclass(s, b)
    s1, s2 = [*reversed(sus1), ], [*reversed(sus2), ]
    while s2:
      b = s2.pop()
      for s in s2:
        self.assertIsSubclass(s, b)
      for s in sus1:
        self.assertNotIsSubclass(s, b)

  def testBadSubclass(self, ) -> None:
    """Tests error handling when subclass checking with a non-class."""
    expectedMessage = 'issubclass() arg 1 must be a class'

    for cls in self.exampleFlags:
      with self.assertRaises(TypeError) as context:
        _ = issubclass("""Bro, I'm a class, trust!""", cls)
      actualMessage = str(context.exception)
      self.assertIn(expectedMessage, actualMessage)

  def testEqualityOperatorTrue(self, ) -> None:
    """Tests that the equality operator works as intended."""
    for left in self.exampleFlags:
      for right in self.exampleFlags:
        if not issubclass(left, right):
          self.assertIsNot(KeeFlagsMeta.__eq__(left, right), NotImplemented)

  def testBaseDuplicateFlag(self, ) -> None:
    """Tests that defining a duplicate flag raises an error."""
    a = KeeFlag()
    b = KeeFlag()
    with self.assertRaises(KeeFlagDuplicate) as context:
      class StackedOverflow(KeeFlags):
        BREH = a
        BREH = b
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'BREH')
    self.assertIs(e.oldFlag, a)
    self.assertIs(e.newFlag, b)

  def testCustomGetValue(self) -> None:
    """Tests that defining a custom 'getValue' method works as intended."""

    class Offset(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()
      C = KeeFlag()

      def _getValue(self) -> int:
        return self.index + 69420

    for member in Offset:
      self.assertEqual(member.value, member.index + 69420)

  def testSubclassGetValue(self) -> None:
    """
    Tests that a subclass of a class providing a custom '_getValue'
    method correctly inherits the method.
    """

    class Offset(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()
      C = KeeFlag()

      def _getValue(self) -> int:
        return self.index + 69420

    class SubOffset(Offset):
      D = KeeFlag()
      E = KeeFlag()

    for member in SubOffset:
      self.assertEqual(member.value, member.index + 69420)

  def testSuper(self, ) -> None:
    """
    Tests that custom metaclass implementation preserves conventional
    behaviour of 'super()'.
    """

    class Base(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

      def _getValue(self) -> int:
        return self.index + 69420

    class Sub(Base):
      C = KeeFlag()
      D = KeeFlag()

      def _getValue(self) -> int:
        return super()._getValue() * 2

    for member in Sub:
      self.assertAlmostEqual(member.value / 2, member.index + 69420)

  def testImplementedEqualOperator(self, ) -> None:
    """
    Tests that the '__eq__' operator correctly identifies equal members.
    """
    for left in self.exampleFlags:
      for right in self.exampleFlags:
        if left is right:
          self.assertEqual(left, right)
        else:
          self.assertNotEqual(left, right)

  def testNotImplementedEqualOperator(self, ) -> None:
    """
    Tests that the '__eq__' operator correctly returns NotImplemented
    when comparing with an object of a different type allowing it a chance
    to provide an implementation.
    """

    class OtherNotImplemented:
      __hash_value__ = None

      def __init__(self, hashValue: int) -> None:
        self.__hash_value__ = hashValue

      def __hash__(self, ) -> int:
        return self.__hash_value__

    class OtherImplemented(OtherNotImplemented):
      def __eq__(self, other: object) -> bool:
        return True

      __hash__ = None

    class Breh(OtherImplemented):
      def __hash__(self, ) -> int:
        raise TypeError('all your base are belong to us')

    for cls in self.exampleFlags:
      self.assertEqual(cls, OtherImplemented(hash(cls)))
      self.assertNotEqual(cls, OtherNotImplemented(hash(cls)))
      with self.assertRaises(TypeError) as context:
        _ = cls == Breh(69)
      self.assertIn('all your base are belong to us', str(context.exception))

  def testPrimeValued(self, ) -> None:
    """
    The 'PrimeValued' example class provides a custom '_getValue'
    implementation that associates each flag with a prime number beginning
    with 2. Then the value of each member is the product of the primes
    associated with the flags that are HIGH for that member. Thus, it
    provides a practical demonstration of custom '_getValue' behaviour.

    'MouseButton' subclasses 'PrimeValued' with flags: 'LEFT', 'RIGHT' and
    'MIDDLE' associated with 2, 3 and 5 respectively. Thus, the 8 possible
    members and their values are:

    - index 0: NULL with value 1
    - index 1: LEFT with value 2
    - index 2: RIGHT with value 3
    - index 3: LEFT_RIGHT with value 6
    - index 4: MIDDLE with value 5  # Note ordering by index, not value
    - index 5: LEFT_MIDDLE with value 10
    - index 6: RIGHT_MIDDLE with value 15
    - index 7: LEFT_RIGHT_MIDDLE with value 30

    """

    for member in MouseButton:
      for high in member.highs:
        self.assertFalse(member.value % PrimeValued.indexPrime(high.index))

  def testMultipleInheritance(self, ) -> None:
    """
    Tests that multiple inheritance correctly merges the flags of bases
    with the conventional precedence order. This includes the flags and
    the '_getValue' method. This implements the use case of creating a new
    class with the flags of an existing class, but with a '_getValue' from
    a separate class, such as the 'PrimeValued' class.

    Please note that since the '_getValue' method of 'PrimeValued' should
    replace the '_getValue' provided by the other base class, it is the
    first base class. Otherwise, any custom '_getValue' method of the
    other parent would take precedence.
    """

    class PrimeRoll(PrimeValued, FlagsExample):
      pass

    for a, b in zip(FlagsExample, PrimeRoll):
      for high in a.highs:
        prime = PrimeValued.indexPrime(high.index)
        self.assertFalse(b.value % prime)

  def testCoverageGymnastics(self, ) -> None:
    """
    While this method appears to 'test' the function of a helper class,
    it actually tests the preservation of overloading functionality in a
    subclass of a 'KeeFlags' class.
    """

    class PrimeRoll(PrimeValued, FlagsExample):
      pass

    for p in PrimeRoll:
      self.assertEqual(p.coverageGymnastics(69, 420), 69 + 420)
      self.assertEqual(p.coverageGymnastics('1337', '80085'), 1337 + 80085)
