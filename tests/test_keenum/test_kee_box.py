"""
TestKeeBox tests 'KeeBox' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeBox, KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.keenum import KeeBoxException, KeeBoxTypeError
from worktoy.waitaminute.keenum import KeeBoxValueError
from . import KeenumTest, WeekDay, Shade, Permission, Extended, KeyBind

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Tone(KeeNum):
  """An enumeration of complex values, for the constructor route."""

  LOW = Kee[complex](complex(1, 2))
  HIGH = Kee[complex](complex(3, 4))


#  Every identifier 'Rank.__class_resolve__' is asked, in order.
ASKED: list = []


class Rank(KeeNum):
  """
  An enumeration of 'int' values whose '__class_resolve__' answers
  'True' with 'MID', 'top' with 'HIGH' and 2 with 'LOW', declines
  anything else, and records every identifier it is asked in 'ASKED'.
  """

  LOW = Kee[int](10)
  MID = Kee[int](20)
  HIGH = Kee[int](30)

  @classmethod
  def __class_resolve__(cls, identifier: Any) -> Any:
    ASKED.append(identifier)
    if identifier is True:
      return cls.MID
    if identifier == 'top':
      return cls.HIGH
    if identifier == 2:
      return cls.LOW
    return NotImplemented


class TestKeeBox(KeenumTest):
  """
  A 'KeeBox' is an 'AttriBox' over an enumeration whose parentheses
  take whatever identifies a member: a member, a name in any case, what
  the enumeration's '__class_resolve__' answers, a position, a value,
  the arguments of a value, or the flags of a flags member. The tests
  pin the subscript, every route of the resolution with its refusal,
  the place of the hook among the routes, the fixtures, and assignment
  through the enumeration's conversion.
  """

  def test_subscript(self) -> None:
    self.assertIsInstance(KeeBox[WeekDay], KeeBox)
    self.assertIsInstance(KeeBox[Permission], KeeBox)
    self.assertIs(KeeBox[Shade].getFieldType(), Shade)
    with self.assertRaises(TypeException) as context:
      KeeBox[int]
    self.assertEqual(context.exception.varName, 'fieldType')
    self.assertIs(context.exception.actualObject, int)
    self.assertIs(context.exception.actualType, type)
    self.assertEqual(context.exception.expectedTypes[0].__name__, 'KeeMeta')
    self.assertEqual(len(context.exception.expectedTypes), 2)
    self.assertIn("'fieldType'", str(context.exception))
    self.assertIn("'KeeMeta' or 'KeeFlagsMeta'", str(context.exception))

  def test_fixture(self) -> None:
    bind = KeyBind()
    self.assertIs(bind.day, WeekDay.TUESDAY)
    self.assertIs(bind.access, Permission.READ_EXEC)
    self.assertIs(bind.level, Shade.MID)
    self.assertNotIn('__field_box__', WeekDay.TUESDAY.__dict__)
    bind.day = 'friday'
    self.assertIs(bind.day, WeekDay.FRIDAY)
    bind.day = WeekDay.SUNDAY
    self.assertIs(bind.day, WeekDay.SUNDAY)
    bind.access = ('read', 'write')
    self.assertIs(bind.access, Permission.READ_WRITE)
    bind.level = 9
    self.assertIs(bind.level, Shade.DARK)
    with self.assertRaises(TypeException) as context:
      bind.day = 'nothing'
    self.assertEqual(context.exception.varName, 'day')
    self.assertEqual(context.exception.actualObject, 'nothing')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (WeekDay,))
    self.assertIn("'day'", str(context.exception))
    self.assertIn("'WeekDay'", str(context.exception))
    del bind.day
    with self.assertRaises(MissingVariable) as context:
      _ = bind.day
    self.assertIs(context.exception.instance, bind)
    self.assertEqual(context.exception.varName, 'day')
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertEqual(str(context.exception),
                     "Missing 'KeyBind.day: object'!")

  def test_num_routes(self) -> None:
    class Holder(BaseObject):
      member = KeeBox[WeekDay](WeekDay.FRIDAY)
      exact = KeeBox[WeekDay]('SATURDAY')
      loose = KeeBox[WeekDay]('sUnDaY')
      position = KeeBox[Shade](2)
      value = KeeBox[WeekDay]('onsdag')
      number = KeeBox[Shade](9)
      built = KeeBox[Tone](3, 4)
      keyed = KeeBox[Tone](real=1, imag=2)
      fractional = KeeBox[Shade](1.5)
      #  'Shade.__class_resolve__' takes a 'float' to the nearest member
      #  below it, as 'Shade(8.5)' does; 'int(8.5)' carries no member.
      nearest = KeeBox[Shade](8.5)
      #  A lone argument of another type is built into a value.
      parsed = KeeBox[Tone]('3+4j')

    holder = Holder()
    self.assertIs(holder.parsed, Tone.HIGH)
    self.assertIs(holder.fractional, Shade.LIGHT)
    self.assertIs(holder.nearest, Shade.MID)
    self.assertIs(Shade(8.5), Shade.MID)
    self.assertIs(holder.member, WeekDay.FRIDAY)
    self.assertIs(holder.exact, WeekDay.SATURDAY)
    self.assertIs(holder.loose, WeekDay.SUNDAY)
    self.assertIs(holder.position, Shade.DARK)
    self.assertIs(holder.value, WeekDay.WEDNESDAY)
    self.assertIs(holder.number, Shade.DARK)
    self.assertIs(holder.built, Tone.HIGH)
    self.assertIs(holder.keyed, Tone.LOW)

  def test_num_refusals(self) -> None:
    class Holder(BaseObject):
      noValue = KeeBox[Shade](4)
      noBool = KeeBox[Shade](True)
      noName = KeeBox[WeekDay]('nothing')
      noBuild = KeeBox[Shade]('x', 'y')
      noMatch = KeeBox[Tone](7, 7)

    holder = Holder()
    with self.assertRaises(KeeBoxValueError) as context:
      _ = holder.noValue
    exception = context.exception
    self.assertIs(exception.desc, Holder.__dict__['noValue'])
    self.assertIs(exception.num, Shade)
    self.assertEqual(exception.value, 4)
    self.assertIn("'Holder.noValue: Shade'", str(exception))
    with self.assertRaises(KeeBoxValueError) as context:
      _ = holder.noBool
    self.assertIs(context.exception.desc, Holder.__dict__['noBool'])
    self.assertIs(context.exception.num, Shade)
    self.assertIs(context.exception.value, True)
    self.assertIn("'Holder.noBool: Shade'", str(context.exception))
    self.assertIn("'True'", str(context.exception))
    with self.assertRaises(KeeBoxValueError) as context:
      _ = holder.noName
    self.assertIs(context.exception.desc, Holder.__dict__['noName'])
    self.assertIs(context.exception.num, WeekDay)
    self.assertEqual(context.exception.value, 'nothing')
    self.assertIn("'Holder.noName: WeekDay'", str(context.exception))
    with self.assertRaises(KeeBoxTypeError) as context:
      _ = holder.noBuild
    exception = context.exception
    self.assertIs(exception.box, Holder.__dict__['noBuild'])
    self.assertEqual(exception.posArgs, ('x', 'y'))
    self.assertIsInstance(exception.__cause__, TypeError)
    self.assertIn("'Holder.noBuild: Shade'", str(exception))
    with self.assertRaises(KeeBoxValueError) as context:
      _ = holder.noMatch
    self.assertIs(context.exception.desc, Holder.__dict__['noMatch'])
    self.assertIs(context.exception.num, Tone)
    self.assertEqual(context.exception.value, complex(7, 7))
    self.assertIn("'Holder.noMatch: Tone'", str(context.exception))
    self.assertIn("'(7+7j)'", str(context.exception))

  def test_class_resolve_order(self) -> None:
    class Holder(BaseObject):
      member = KeeBox[Rank](Rank.HIGH)
      named = KeeBox[Rank]('mid')
      built = KeeBox[Rank]('30', base=10)
      hooked = KeeBox[Rank]('top')
      flag = KeeBox[Rank](True)
      before = KeeBox[Rank](2)
      position = KeeBox[Rank](1)
      value = KeeBox[Rank](20)

    ASKED.clear()
    holder = Holder()
    #  A member, a name and the arguments of a value never reach the hook.
    self.assertIs(holder.member, Rank.HIGH)
    self.assertIs(holder.named, Rank.MID)
    self.assertIs(holder.built, Rank.HIGH)
    self.assertEqual(ASKED, [])
    #  The hook answers before the refusal of a 'bool' and before a
    #  position, and a declined identifier goes on to position and value.
    self.assertIs(holder.hooked, Rank.HIGH)
    self.assertIs(holder.flag, Rank.MID)
    self.assertIs(holder.before, Rank.LOW)
    self.assertIs(holder.position, Rank.MID)
    self.assertIs(holder.value, Rank.MID)
    self.assertEqual(ASKED, ['top', True, 2, 1, 20])
    self.assertIs(ASKED[1], True)
    #  An assignment resolves through the class as the declaration did.
    holder.member = 'top'
    self.assertIs(holder.member, Rank.HIGH)

  def test_flags_routes(self) -> None:
    class Holder(BaseObject):
      names = KeeBox[Permission]('read', 'WRITE')
      listed = KeeBox[Permission](['exec'])
      frozen = KeeBox[Permission](frozenset(('READ',)))
      indexed = KeeBox[Permission](6)
      member = KeeBox[Permission](Extended.READ_WRITE)
      none = KeeBox[Permission]()
      #  A container among several arguments is one argument.
      mixed = KeeBox[Permission](('read',), 'exec')

    holder = Holder()
    self.assertIs(holder.mixed, Permission.READ_EXEC)
    self.assertIs(holder.names, Permission.READ_WRITE)
    self.assertIs(holder.listed, Permission.EXEC)
    self.assertIs(holder.frozen, Permission.READ)
    self.assertIs(holder.indexed, Permission.WRITE_EXEC)
    self.assertIs(holder.member, Permission.READ_WRITE)
    self.assertIs(holder.none, Permission.NULL)

  def test_neither_kind(self) -> None:
    box = KeeBox[WeekDay]('monday')
    object.__setattr__(box, '__field_type__', int)
    with self.assertRaises(KeeBoxException) as context:
      box._resolve('monday')
    self.assertIs(context.exception.box, box)
    self.assertEqual(context.exception.posArgs, ('monday',))
    self.assertIn("'monday'", str(context.exception))

  def test_is_member(self) -> None:
    box = KeeBox[Permission]()
    self.assertTrue(box._isMember(Permission.READ))
    self.assertTrue(box._isMember(Extended.READ))
    self.assertFalse(box._isMember('READ'))

  def test_random_names(self) -> None:
    self.randomInteger.size = 6
    for number in self.randomInteger.row:
      member = WeekDay.members[number % 7]
      space = {'day': KeeBox[WeekDay](member.name.lower())}
      Holder = type(BaseObject)('Holder', (BaseObject,), space)
      with self.subTest(member=member.name):
        self.assertIs(Holder().day, member)

  def test_argument_shapes_and_index_edges(self) -> None:
    class Owner(BaseObject):
      two = KeeBox[Shade](1, 2)
      none = KeeBox[Shade]()
      first = KeeBox[Shade](0)
      last = KeeBox[Shade](2)
      negative = KeeBox[Shade](-1)
      past = KeeBox[Shade](3)
      built = KeeBox[WeekDay](str.join('', ['fre', 'dag']))

    owner = Owner()
    with self.assertRaises(KeeBoxTypeError) as context:
      _ = owner.two
    self.assertIs(context.exception.box, Owner.__dict__['two'])
    self.assertEqual(context.exception.posArgs, (1, 2))
    self.assertIn("'Owner.two: Shade'", str(context.exception))
    self.assertIn('<int: 1>', str(context.exception))
    with self.assertRaises(KeeBoxValueError) as context:
      _ = owner.none
    self.assertIs(context.exception.desc, Owner.__dict__['none'])
    self.assertIs(context.exception.num, Shade)
    self.assertEqual(context.exception.value, 0)
    self.assertIn("'Owner.none: Shade'", str(context.exception))
    self.assertIs(owner.first, Shade.LIGHT)
    self.assertIs(owner.last, Shade.DARK)
    with self.assertRaises(KeeBoxValueError) as context:
      _ = owner.negative
    self.assertIs(context.exception.desc, Owner.__dict__['negative'])
    self.assertIs(context.exception.num, Shade)
    self.assertEqual(context.exception.value, -1)
    self.assertIn("'-1'", str(context.exception))
    with self.assertRaises(KeeBoxValueError) as context:
      _ = owner.past
    self.assertIs(context.exception.desc, Owner.__dict__['past'])
    self.assertIs(context.exception.num, Shade)
    self.assertEqual(context.exception.value, 3)
    self.assertIn("'3'", str(context.exception))
    self.assertIs(owner.built, WeekDay.FRIDAY)
