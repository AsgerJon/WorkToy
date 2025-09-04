"""
TestKeeFlags module tests the KeeFlags class functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlags, KeeFlagsMeta, KeeFlag
from worktoy.waitaminute import MissingVariable, TypeException
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type


class TestKeeFlags(KeeTest):
  """TestKeeFlags class tests the KeeFlags class functionality."""

  exampleFlags: list[Type[KeeFlags]]
  exampleValueTypes: list[type]

  def testIndices(self) -> None:
    """Tests the members of the example KeeFlags classes."""

    for Flags in self.exampleFlags:
      for i, member in enumerate(Flags):
        self.assertEqual(member.index, i)

  def testFlags(self, ) -> None:
    """Tests the 'flags' attribute of the example KeeFlags classes."""
    for cls in self.exampleFlags:
      for flag in cls.flags:
        self.assertTrue(isinstance(flag, KeeFlag))

  def testMemberList(self, ) -> None:
    """
    Tests the availability of the 'memberList' attribute on the
    examples. This attribute is defined on the metaclass.
    """
    for cls in self.exampleFlags:
      self.assertTrue(hasattr(cls, 'memberList'))
      self.assertTrue(isinstance(cls.memberList, list))
      for (i, (foo, bar)) in enumerate(zip(cls.memberList, cls)):
        fromAttr = getattr(cls, bar.name)
        self.assertIs(foo, getattr(cls, bar.name))
        self.assertIs(bar, getattr(cls, foo.name))

  def testMemberDict(self, ) -> None:
    """
    Tests the availability of the 'memberDict' attribute on the
    examples. This attribute is defined on the metaclass.
    """
    for cls in self.exampleFlags:
      self.assertTrue(hasattr(cls, 'memberDict'))
      self.assertTrue(isinstance(cls.memberDict, dict))
      for (i, (key, member)) in enumerate(cls.memberDict.items()):
        fromAttr = getattr(cls, member.name)
        self.assertIs(member, fromAttr)

  def testResolveIndex(self, ) -> None:
    """Tests the '_resolveIndex' method"""
    for cls in self.exampleFlags:
      for index, member in enumerate(cls, ):
        fromIndex = cls._resolveIndex(index)
        fromGeneral = cls._resolveMember(index, )
        fromCall = cls(index)
        fromDict = cls[index]
        self.assertIs(fromDict, member)
        self.assertIs(fromCall, member)
        self.assertIs(fromIndex, member)
        self.assertIs(fromGeneral, member)
        self.assertEqual(member.index, index)

  def testResolveName(self, ) -> None:
    """Tests the '_resolveName' method"""
    for cls in self.exampleFlags:
      for index, member in enumerate(cls, ):
        fromName = cls._resolveName(member.name)
        fromGeneral = cls._resolveMember(member.name, )
        fromCall = cls(member.name)
        fromDict = cls[member.name]
        self.assertIs(fromDict, member)
        self.assertIs(fromCall, member)
        self.assertIs(fromName, member)
        self.assertIs(fromGeneral, member)
        self.assertEqual(fromName.name, member.name)

  def testResolveNames(self, ) -> None:
    """Tests the '_resolveNames' method"""
    for cls in self.exampleFlags:
      for member in cls:
        names = [flag.name for flag in member.highs]
        if not names:
          continue
        fromNames = cls._resolveNames(*names)
        fromGeneral = cls._resolveMember(*names)
        fromCall = cls(*names)
        fromDict = cls.__getitem__(names, )
        self.assertIs(fromDict, member)
        fromSet = cls._resolveMember(set(member.names))
        fromFrozenSet = cls._resolveMember(member.names)
        fromTuple = cls._resolveMember((*names,))
        fromList = cls._resolveMember([*names, ])
        self.assertIs(fromSet, member)
        self.assertIs(fromFrozenSet, member)
        self.assertIs(fromTuple, member)
        self.assertIs(fromList, member)
        self.assertIs(fromCall, member)
        self.assertIs(fromGeneral, member)
        self.assertIs(fromNames, member)

  def testResolveValue(self, ) -> None:
    """Tests the '_resolveValue' method"""
    for cls in self.exampleFlags:
      for member in cls:
        fromValue = cls._resolveValue(member.value)
        self.assertIs(fromValue, member)

  def testMembers(self, ) -> None:
    """Tests the functionality of the 'KeeFlag' class"""
    for cls in self.exampleFlags:
      for flag in cls.flags:
        self.assertIn(cls.__name__, str(flag))
        self.assertIn(cls.__name__, repr(flag))
        self.assertIsInstance(flag, KeeFlag)
        self.assertEqual(flag.index, int(flag))
        self.assertIn(str(flag.index), str(flag))
        self.assertIn(flag.fieldName, str(flag))
        self.assertIn(cls.__name__, str(flag))
        for arg in flag.args:
          self.assertIn(repr(arg), repr(flag))
        for key, val in flag.kwargs.items():
          self.assertIn(key, repr(flag))
          self.assertIn(repr(val), repr(flag))

  def testOrphanedFlags(self, ) -> None:
    """Tests that orphaned flags fall back to 'object' methods."""

    orphanFlag = KeeFlag()

    expected = object.__str__(orphanFlag)
    actual = str(orphanFlag)
    self.assertEqual(expected, actual)

    expected = object.__repr__(orphanFlag)
    actual = repr(orphanFlag)
    self.assertEqual(expected, actual)

    with self.assertRaises(MissingVariable) as context:
      _ = orphanFlag.fieldName
    e = context.exception
    self.assertIs(e.instance, orphanFlag)
    self.assertEqual(e.varName, '__field_name__')
    self.assertIs(e.type_, str)

    with self.assertRaises(MissingVariable) as context:
      _ = orphanFlag.fieldOwner
    e = context.exception
    self.assertIs(e.instance, orphanFlag)
    self.assertEqual(e.varName, '__field_owner__')
    self.assertIs(e.type_, KeeFlagsMeta)

    with self.assertRaises(MissingVariable) as context:
      _ = orphanFlag.index
    e = context.exception
    self.assertIs(e.instance, orphanFlag)
    self.assertEqual(e.varName, '__member_index__')
    self.assertIs(e.type_, int)

    with self.assertRaises(MissingVariable) as context:
      _ = orphanFlag.name
    e = context.exception
    self.assertIs(e.instance, orphanFlag)
    self.assertEqual(e.varName, '__member_name__')
    self.assertIs(e.type_, str)

  def testBadlyTypedFlags(self, ) -> None:
    """Tests that badly typed flags raise 'TypeException'."""

    badlyTypedFlag = KeeFlag()
    badlyTypedFlag.__member_index__ = """bro, i'm an integer, trust!"""
    badlyTypedFlag.__field_name__ = 69
    badlyTypedFlag.__member_name__ = 420
    badlyTypedFlag.__field_owner__ = """bro, i'm a class, trust!"""

    with self.assertRaises(TypeException) as context:
      _ = badlyTypedFlag.index
    e = context.exception
    self.assertEqual(e.varName, '__member_index__')
    self.assertEqual(e.actualObject, badlyTypedFlag.__member_index__)
    self.assertIs(e.actualType, type(badlyTypedFlag.__member_index__))
    self.assertIn(int, e.expectedTypes)

    with self.assertRaises(TypeException) as context:
      _ = badlyTypedFlag.fieldName
    e = context.exception
    self.assertEqual(e.varName, '__field_name__')
    self.assertEqual(e.actualObject, badlyTypedFlag.__field_name__)
    self.assertIs(e.actualType, type(badlyTypedFlag.__field_name__))
    self.assertIn(str, e.expectedTypes)

    with self.assertRaises(TypeException) as context:
      _ = badlyTypedFlag.name
    e = context.exception
    self.assertEqual(e.varName, '__member_name__')
    self.assertEqual(e.actualObject, badlyTypedFlag.__member_name__)
    self.assertIs(e.actualType, type(badlyTypedFlag.__member_name__))
    self.assertIn(str, e.expectedTypes)

    with self.assertRaises(TypeException) as context:
      _ = badlyTypedFlag.fieldOwner
    e = context.exception
    self.assertEqual(e.varName, '__field_owner__')
    self.assertEqual(e.actualObject, badlyTypedFlag.__field_owner__)
    self.assertIs(e.actualType, type(badlyTypedFlag.__field_owner__))
    self.assertIn(KeeFlagsMeta, e.expectedTypes)

    with self.assertRaises(TypeError) as context:
      _ = [*badlyTypedFlag, ]
    e = context.exception
    self.assertIn('iterable', str(e))

    class BadlyTypedFlags(KeeFlags):
      TOM = KeeFlag()
      DICK = KeeFlag()
      HARRY = KeeFlag()

    tom = BadlyTypedFlags(1)
    delattr(tom, '__member_index__')

    with self.assertRaises(MissingVariable) as context:
      _ = tom.index
    e = context.exception
    self.assertIs(e.instance, tom, )
    self.assertEqual(e.varName, '__member_index__')
    self.assertIs(e.type_, int)

    setattr(tom, '__member_index__', """I'm an integer, trust me bro!""")

    with self.assertRaises(TypeException) as context:
      _ = tom.index
    e = context.exception
    self.assertEqual(e.varName, '__member_index__')
    self.assertIs(e.actualObject, tom.__member_index__)
    self.assertIs(e.actualType, type(tom.__member_index__))
    self.assertIn(int, e.expectedTypes)

  def testHighsLows(self) -> None:
    """
    Tests the 'highs' and 'lows' attributes of the example KeeFlags
    classes.
    """
    for cls in self.exampleFlags:
      for member in cls:
        _c = 0
        for flag in cls.flags:
          self.assertIsInstance(flag, KeeFlag)
        for high in member.highs:
          self.assertIsInstance(high, KeeFlag)
          self.assertIn(high, cls.flags)
          self.assertNotIn(high, member.lows)
          _c += 1
        for low in member.lows:
          self.assertIn(low, cls.flags)
          self.assertNotIn(low, member.highs)
          _c += 1
        for flag in cls.flags:
          self.assertIn(flag, [*member.highs, *member.lows])
          _c -= 1
        self.assertFalse(_c, )
        for i, j in zip(member, member.highs):
          self.assertEqual(i, j)

  def testBadResolve(self, ) -> None:
    """Tests that bad resolutions raise the appropriate exceptions."""

    for cls in self.exampleFlags:
      with self.assertRaises(IndexError) as context:
        _ = cls._resolveIndex(len(cls))
      e = context.exception
      self.assertIn(cls.__name__, str(e))
      self.assertIn(str(len(cls)), str(e))

  def testValueTypes(self) -> None:
    """
    Tests that the 'value' attribute is of type 'valueType' on the owning
    class.
    """
    for cls in self.exampleFlags:
      for member in cls:
        self.assertIsInstance(member.value, cls.valueType)

  def testEmptyResolution(self) -> None:
    """
    Tests that '_resolveMember' correctly returns the 'NULL' member when
    called without arguments.
    """
    for cls in self.exampleFlags:
      expectedNull = cls._resolveMember()
      actualNull = cls.NULL
      self.assertIs(expectedNull, actualNull)

  def testResolveBadName(self, ) -> None:
    """
    Tests that '_resolveName' raises 'KeyError' when given a bad name.
    """
    expectedMessage = """has no member with name"""
    for cls in self.exampleFlags:
      with self.assertRaises(KeyError) as context:
        _ = cls._resolveName("""Bro, it's me, lemme in!""")
      self.assertIn(expectedMessage, str(context.exception))

  def testImplementedEqualityOperator(self, ) -> None:
    """
    Tests the equality operator for situations not resulting in
    'NotImplemented'.
    """
    for leftCls in self.exampleFlags:
      for rightCls in self.exampleFlags:
        for i, left in enumerate(leftCls):
          for j, right in enumerate(rightCls):
            if leftCls == rightCls:  # Equal when indices match
              if i == j:
                self.assertTrue(left == right)
              else:
                self.assertFalse(left == right)
            else:  # Not equal, even when indices match
              self.assertFalse(left == right)
