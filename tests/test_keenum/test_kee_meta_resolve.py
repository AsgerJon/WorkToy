"""
TestKeeMetaResolve tests the member resolution of 'KeeMeta' from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeResolveError
from . import KeenumTest, WeekDay, Shade, Bag


class TestKeeMetaResolve(KeenumTest):
  """
  A call or a subscript of an enumeration resolves one identifier by
  identity, name, the class hook, position for a subscript, and value,
  and raises 'KeeResolveError' when every step misses. The tests pin
  each step, the order of the steps, the refusals of the call, and
  'fromValue'.
  """

  def test_identity(self) -> None:
    self.assertIs(WeekDay(WeekDay.MONDAY), WeekDay.MONDAY)
    self.assertIs(WeekDay[WeekDay.SUNDAY], WeekDay.SUNDAY)

  def test_name_ignores_case(self) -> None:
    for name in ('MONDAY', 'monday', 'Monday', 'mOnDaY'):
      with self.subTest(name=name):
        self.assertIs(WeekDay(name), WeekDay.MONDAY)
        self.assertIs(WeekDay[name], WeekDay.MONDAY)
    self.assertIs(WeekDay._resolveFromName('tuesday'), WeekDay.TUESDAY)
    self.assertIs(WeekDay._resolveFromName('nope'), NotImplemented)

  def test_value(self) -> None:
    self.assertIs(WeekDay('tirsdag'), WeekDay.TUESDAY)
    self.assertIs(WeekDay['tirsdag'], WeekDay.TUESDAY)
    self.assertIs(Shade(9), Shade.DARK)
    self.assertIs(Bag([1, 2, 3]), Bag.MANY)
    self.assertIs(Bag([1]), Bag.FEW)
    with self.assertRaises(KeeResolveError) as context:
      WeekDay('nothing')
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.identifier, 'nothing')
    self.assertIn("'WeekDay' could not resolve the identifier 'nothing'",
                  str(context.exception))

  def test_index_only_by_subscript(self) -> None:
    self.assertIs(Shade[0], Shade.LIGHT)
    self.assertIs(Shade[1], Shade.MID)
    self.assertIs(Shade[-1], Shade.DARK)
    self.assertIs(Shade(1), Shade.LIGHT)
    self.assertIs(Shade[5], Shade.MID)
    self.assertIs(Shade[9], Shade.DARK)
    with self.assertRaises(KeeResolveError) as context:
      Shade[99]
    self.assertIs(context.exception.keeNum, Shade)
    self.assertEqual(context.exception.identifier, 99)
    self.assertIn("'Shade' could not resolve the identifier 99",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Shade(2)
    self.assertIs(context.exception.keeNum, Shade)
    self.assertEqual(context.exception.identifier, 2)
    self.assertIn('the identifier 2 to', str(context.exception))

  def test_bool_is_no_identifier_of_ints(self) -> None:
    class Bits(KeeNum):
      ZERO = Kee[int](0)
      ONE = Kee[int](1)

    with self.assertRaises(KeeResolveError) as context:
      Bits(True)
    self.assertIs(context.exception.keeNum, Bits)
    self.assertIs(context.exception.identifier, True)
    self.assertIn("'Bits' could not resolve the identifier True",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Bits[False]
    self.assertIs(context.exception.keeNum, Bits)
    self.assertIs(context.exception.identifier, False)
    self.assertIn('the identifier False to', str(context.exception))
    self.assertIs(Bits._resolveFromValue(True, int), NotImplemented)
    self.assertIs(Bits(0), Bits.ZERO)
    self.assertIs(Bits[1], Bits.ONE)

  def test_class_hook(self) -> None:
    self.assertIs(Shade(5.5), Shade.MID)
    self.assertIs(Shade[9.0], Shade.DARK)
    self.assertIs(Shade(1.0), Shade.LIGHT)
    with self.assertRaises(KeeResolveError) as context:
      Shade(0.5)
    self.assertIs(context.exception.keeNum, Shade)
    self.assertEqual(context.exception.identifier, 0.5)
    self.assertIn("'Shade' could not resolve the identifier 0.5",
                  str(context.exception))
    self.assertIs(Shade('mid'), Shade.MID)
    self.assertIs(Shade.__class_resolve__(0.5), NotImplemented)

  def test_values_that_do_not_hash(self) -> None:
    self.assertIs(Bag._resolveFromValue([1, 2, 3], list), Bag.MANY)
    self.assertIs(Bag._resolveFromValue([9], list), NotImplemented)
    self.assertIs(Bag._scanValues([1]), Bag.FEW)
    self.assertIs(Bag._scanValues([2]), NotImplemented)

    class Loose(KeeNum):
      A = Kee[object]('a')
      B = Kee[object]([1])
      C = Kee[object](3)

    self.assertIs(Loose([1]), Loose.B)
    self.assertIs(Loose('a'), Loose.A)
    #  A hashable identifier is compared with each value too, once one
    #  value of the enumeration does not hash.
    self.assertIs(Loose(3), Loose.C)
    self.assertIs(Loose._resolveFromValue([2], object), NotImplemented)
    self.assertIs(Loose._resolveFromValue('z', object), NotImplemented)

    class Hashed(KeeNum):
      A = Kee[object]('a')
      B = Kee[object](2)

    self.assertNotIn('__unhashable__', Hashed.valuedMembers)
    self.assertIs(Hashed._resolveFromValue([1], object), NotImplemented)
    with self.assertRaises(KeeResolveError) as context:
      Hashed([1])
    self.assertIs(context.exception.keeNum, Hashed)
    self.assertEqual(context.exception.identifier, [1])
    self.assertIn("'Hashed' could not resolve the identifier [1]",
                  str(context.exception))
    self.assertIs(Hashed(2), Hashed.B)

  def test_empty_enumeration(self) -> None:
    class Empty(KeeNum):
      pass

    with self.assertRaises(KeeResolveError) as context:
      Empty('anything')
    self.assertIs(context.exception.keeNum, Empty)
    self.assertEqual(context.exception.identifier, 'anything')
    self.assertIn("'Empty' could not resolve the identifier 'anything'",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Empty[0]
    self.assertIs(context.exception.keeNum, Empty)
    self.assertEqual(context.exception.identifier, 0)
    self.assertIn('the identifier 0 to', str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Empty.fromValue(1)
    self.assertIs(context.exception.keeNum, Empty)
    self.assertEqual(context.exception.identifier, 1)
    self.assertIn('the identifier 1 to', str(context.exception))

  def test_call_takes_one_identifier(self) -> None:
    spec = 'WeekDay() takes exactly one argument, the identifier of a '
    with self.assertRaises(TypeError) as context:
      WeekDay()
    self.assertEqual(str(context.exception),
                     spec + 'member, but received 0.')
    with self.assertRaises(TypeError) as context:
      WeekDay('monday', 'tuesday')
    self.assertEqual(str(context.exception),
                     spec + 'member, but received 2.')
    with self.assertRaises(TypeError) as context:
      WeekDay(name='monday')
    self.assertEqual(str(context.exception),
                     "WeekDay() takes no keyword arguments, "
                     "but received 'name'.")

  def test_from_value(self) -> None:
    self.assertIs(WeekDay.fromValue('onsdag'), WeekDay.WEDNESDAY)
    self.assertIs(Bag.fromValue([1]), Bag.FEW)
    with self.assertRaises(TypeException) as context:
      WeekDay.fromValue(3)
    self.assertEqual(context.exception.varName, 'value')
    self.assertEqual(context.exception.actualObject, 3)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'value'", str(context.exception))
    self.assertIn("'str'", str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      WeekDay.fromValue('nothing')
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.identifier, 'nothing')
    self.assertIn("'WeekDay' could not resolve the identifier 'nothing'",
                  str(context.exception))

  def test_random_lookups(self) -> None:
    self.randomInteger.size = 7
    for number in self.randomInteger.row:
      index = number % len(WeekDay)
      member = WeekDay.members[index]
      with self.subTest(index=index):
        self.assertIs(WeekDay[index], member)
        self.assertIs(WeekDay(member.name.lower()), member)
        self.assertIs(WeekDay(member.value), member)

  def test_bool_is_no_index(self) -> None:
    with self.assertRaises(KeeResolveError) as context:
      _ = Shade[True]
    self.assertIs(context.exception.keeNum, Shade)
    self.assertIs(context.exception.identifier, True)
    self.assertIn("'Shade' could not resolve the identifier True",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      _ = Shade[False]
    self.assertIs(context.exception.keeNum, Shade)
    self.assertIs(context.exception.identifier, False)
    self.assertIn('the identifier False to', str(context.exception))
    self.assertIs(Shade[1], Shade.MID)
