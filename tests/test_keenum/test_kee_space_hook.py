"""
TestKeeSpaceHook tests 'KeeSpaceHook' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeSpace, KeeSpaceHook, KeeMeta
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeMemberNameError, KeeCaseException
from worktoy.waitaminute.keenum import KeeDuplicate
from worktoy.waitaminute.meta import UnboundClassHook, ReservedName
from . import KeenumTest


class TestKeeSpaceHook(KeenumTest):
  """
  'KeeSpaceHook' takes every 'Kee' from the class body for the
  namespace's record, refuses a member's name bound twice in either
  order, refuses a '__class_resolve__' that is no classmethod, and holds
  the name of a member to upper case at the line binding it, unless the
  class statement says 'strictCase=False', a keyword it holds to a
  'bool' before the body runs and that a class statement without it
  takes from the nearest class along its resolution order that gave it.
  Whatever the case rule, it refuses a member whose name another member
  has in any case, at the line binding it, and without the case rule a
  member at a name the class or its metaclass holds already. The tests
  pin each on class statements and on the hook called by hand.
  """

  def test_kee_claimed(self) -> None:
    class Local(KeeNum):
      A = Kee[int](1)
      other = 'plain'

    space = Local.__namespace__
    self.assertFalse(dict.__contains__(space, 'A'))
    self.assertIsInstance(space['A'], Kee)
    self.assertTrue(dict.__contains__(space, 'other'))
    self.assertEqual(Local.other, 'plain')
    self.assertIs(KeeSpace.__dict__['keeSpaceHook'],
                  KeeSpace.classGetHooks()[-1])
    self.assertIsInstance(KeeSpace.classGetHooks()[-1], KeeSpaceHook)

  def test_plain_value_at_a_member_name_refused(self) -> None:
    with self.assertRaises(KeeMemberNameError) as context:
      class Local(KeeNum):
        A = Kee[int](1)
        A = 'plain'

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("'A'", str(context.exception))

  def test_member_at_a_plain_name_refused(self) -> None:
    with self.assertRaises(KeeMemberNameError) as context:
      class Local(KeeNum):
        A = 'plain'
        A = Kee[int](1)

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("The class body of enumeration class 'Local' binds 'A'",
                  str(context.exception))

  def test_inherited_member_name_refused(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)

    with self.assertRaises(KeeMemberNameError) as context:
      class Sub(Base):
        A = 'plain'

    self.assertEqual(context.exception.clsName, 'Sub')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("The class body of enumeration class 'Sub' binds 'A'",
                  str(context.exception))

  def test_class_resolve_must_be_a_classmethod(self) -> None:
    def resolve(cls, identifier: object) -> object:
      """Neither a classmethod nor refused by Python."""

    for value in (resolve, staticmethod(resolve)):
      with self.subTest(value=type(value).__name__):
        with self.assertRaises(UnboundClassHook) as context:
          class Local(KeeNum):
            A = Kee[int](1)
            __class_resolve__ = value

        self.assertEqual(context.exception.className, 'Local')
        self.assertEqual(context.exception.hookName, '__class_resolve__')
        self.assertIsNone(context.exception.baseName)
        self.assertIn("The class body of 'Local' binds '__class_resolve__'",
                      str(context.exception))
        self.assertIn("'@classmethod'", str(context.exception))

  def test_by_hand(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(space, KeeSpace)
    self.assertFalse(hook.setItemPhase('plain', 1))
    self.assertTrue(hook.setItemPhase('A', Kee[int](1)))
    self.assertTrue(space.hasNum('A'))
    self.assertFalse(hook.setItemPhase('__class_resolve__', None))
    self.assertFalse(hook.setItemPhase('__class_resolve__',
                                       classmethod(lambda cls, i: i)))

  def test_random_plain_names_pass(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(space, KeeSpace)
    self.randomWord.size = 6
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertFalse(hook.setItemPhase(word, word))

  def test_resolver_name_by_equality_and_its_neighbours(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = [h for h in space.getHooks() if isinstance(h, KeeSpaceHook)][0]

    def plain(cls, identifier) -> None:
      """A resolver written without classmethod."""

    with self.assertRaises(UnboundClassHook) as context:
      hook.setItemPhase(str.join('', ['__class_', 'resolve__']), plain)
    self.assertEqual(context.exception.className, 'Hand')
    self.assertEqual(context.exception.hookName, '__class_resolve__')
    self.assertIsNone(context.exception.baseName)
    self.assertIn("The class body of 'Hand' binds '__class_resolve__'",
                  str(context.exception))
    self.assertFalse(hook.setItemPhase('describe', plain))
    self.assertFalse(hook.setItemPhase('__bool__', plain))
    self.assertFalse(hook.setItemPhase('__str__', plain))

  def test_lower_case_refused_at_its_line(self) -> None:
    reached = []
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeNum):
        red = Kee[int](1)
        reached.append('after')  # pragma: no cover, no mutate

    self.assertEqual(context.exception.name, 'red')
    self.assertIn("must have upper case names, but received: 'red'",
                  str(context.exception))
    self.assertEqual(reached, [])

  def test_strict_case_false_admits_any_case(self) -> None:
    class Unit(KeeNum, strictCase=False):
      mm = Kee[float](0.001)
      Cm = Kee[float](0.01)
      KM = Kee[float](1000.0)

    self.assertEqual([unit.name for unit in Unit], ['mm', 'Cm', 'KM'])
    self.assertEqual(Unit.mm.value, 0.001)
    self.assertIs(Unit('MM'), Unit.mm)

  def test_strict_case_true_refuses(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeNum, strictCase=True):
        red = Kee[int](1)

    self.assertEqual(context.exception.name, 'red')
    self.assertIn("must have upper case names, but received: 'red'",
                  str(context.exception))

  def test_strict_case_must_be_a_bool(self) -> None:
    with self.assertRaises(TypeException) as context:
      class Local(KeeNum, strictCase='no'):
        A = Kee[int](1)  # pragma: no cover, no mutate

    self.assertEqual(context.exception.varName, 'strictCase')
    self.assertEqual(context.exception.actualObject, 'no')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (bool,))
    self.assertIn("'strictCase'", str(context.exception))

  def test_strict_case_checked_before_the_body_runs(self) -> None:
    reached = []
    for value in ('no', None, 0, 1, 1.0):
      with self.subTest(value=value):
        with self.assertRaises(TypeException) as context:
          class Local(KeeNum, strictCase=value):
            reached.append('body')  # pragma: no cover, no mutate

        self.assertEqual(context.exception.varName, 'strictCase')
        self.assertIs(context.exception.actualObject, value)
        self.assertIs(context.exception.actualType, type(value))
        self.assertEqual(context.exception.expectedTypes, (bool,))
        self.assertIn("at name 'strictCase' to be an instance of 'bool'",
                      str(context.exception))
    self.assertEqual(reached, [])

  def test_strict_case_bool_without_members(self) -> None:
    for value in (True, False):
      with self.subTest(value=value):
        class Local(KeeNum, strictCase=value):
          other = 'plain'

        self.assertEqual(len(Local), 0)
        self.assertEqual(Local.other, 'plain')

  def test_strict_case_by_hand_refused_at_construction(self) -> None:
    with self.assertRaises(TypeException) as context:
      KeeSpace(KeeMeta, 'Hand', (), strictCase='no')
    self.assertEqual(context.exception.varName, 'strictCase')
    self.assertEqual(context.exception.actualObject, 'no')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (bool,))
    self.assertIn("at name 'strictCase' to be an instance of 'bool'",
                  str(context.exception))
    hook = KeeSpace.__dict__['keeSpaceHook']
    for kwargs in (dict(), dict(strictCase=True), dict(strictCase=False)):
      with self.subTest(kwargs=kwargs):
        space = KeeSpace(KeeMeta, 'Hand', (), **kwargs)
        bound = hook.__get__(space, KeeSpace)
        self.assertIsNone(bound.preparePhase(space))

  def test_names_differing_by_case_refused_at_the_line(self) -> None:
    reached = []
    with self.assertRaises(KeeDuplicate) as context:
      class Power(KeeNum, strictCase=False):
        mW = Kee[float](0.001)
        kW = Kee[float](1000.0)
        reached.append('between')
        MW = Kee[float](1000000.0)
        reached.append('after')  # pragma: no cover, no mutate

    exception = context.exception
    self.assertEqual(exception.clsName, 'Power')
    self.assertEqual(exception.name, 'MW')
    self.assertEqual(exception.oldMember.name, 'mW')
    self.assertEqual(exception.oldMember.getPosArgs(), (0.001,))
    self.assertEqual(exception.newMember.getPosArgs(), (1000000.0,))
    self.assertEqual(str(exception), str.join(' ', """Enumeration
      'Power' already contains member: '<Kee member: mW>', and cannot
      take another member named 'MW'! The names of the members of an
      enumeration must differ by more than their case, since a lookup by
      name ignores case.""".split()))
    self.assertEqual(reached, ['between'])

  def test_case_refusal_comes_before_the_duplicate(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeNum):
        RED = Kee[int](1)
        red = Kee[int](2)

    self.assertEqual(context.exception.name, 'red')
    self.assertIn("must have upper case names, but received: 'red'",
                  str(context.exception))

  def test_inherited_name_in_another_case_refused(self) -> None:
    class Base(KeeNum, strictCase=False):
      mw = Kee[int](1)

    for keywords in (dict(), dict(strictCase=False)):
      with self.subTest(keywords=keywords):
        with self.assertRaises(KeeDuplicate) as context:
          class Sub(Base, **keywords):
            MW = Kee[int](2)

        self.assertEqual(context.exception.clsName, 'Sub')
        self.assertEqual(context.exception.name, 'MW')
        self.assertEqual(context.exception.oldMember.name, 'mw')
        self.assertEqual(context.exception.oldMember.getPosArgs(), (1,))
        self.assertEqual(context.exception.newMember.getPosArgs(), (2,))
        self.assertIn("Enumeration 'Sub' already contains member: "
                      "'<Kee member: mw>', and cannot take another "
                      "member named 'MW'!", str(context.exception))
        self.assertIn('must differ by more than their case',
                      str(context.exception))

  def test_duplicate_by_hand(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', (), strictCase=False)
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(space, KeeSpace)
    first = Kee[int](1)
    self.assertTrue(hook.setItemPhase('Red', first))
    for name in ('Red', 'RED', 'red', 'rED'):
      with self.subTest(name=name):
        refused = Kee[int](2)
        with self.assertRaises(KeeDuplicate) as context:
          hook.setItemPhase(name, refused)
        self.assertEqual(context.exception.clsName, 'Hand')
        self.assertEqual(context.exception.name, name)
        self.assertIs(context.exception.oldMember, first)
        self.assertIs(context.exception.newMember, refused)
        self.assertIn("Enumeration 'Hand' already contains member: "
                      "'<Kee member: Red>', and cannot take another "
                      "member named '%s'!" % name, str(context.exception))
        self.assertEqual([*space.__enumeration_members__], ['Red'])
    self.assertTrue(hook.setItemPhase('Reds', Kee[int](3)))
    self.assertTrue(hook.setItemPhase('Re', Kee[int](4)))
    self.assertEqual([*space.__enumeration_members__], ['Red', 'Reds', 'Re'])

  def test_name_of_the_class_refused_at_its_line(self) -> None:
    reached = []
    with self.assertRaises(ReservedName) as context:
      class Key(KeeNum, strictCase=False):
        enter = Kee[str]('enter')
        reached.append('between')
        space = Kee[str](' ')
        reached.append('after')  # pragma: no cover, no mutate

    self.assertEqual(context.exception.resName, 'space')
    self.assertEqual(str(context.exception),
                     "Attempted to use reserved name: 'space'!")
    self.assertEqual(reached, ['between'])

  def test_names_of_the_class_refused_without_the_case_rule(self) -> None:
    names = (
      'space', 'members', 'base', 'mroNum', 'namedMembers', 'valueType',
      'valuedMembers', 'fromValue', 'getNamespace', 'getNamespaceClass',
      'mro', 'owners', 'index', '_addOwner', '_computeHash', '_holds',
      '__len__', '__str__',
    )
    for name in names:
      with self.subTest(name=name):
        body = {'first': Kee[int](1), name: Kee[int](2)}
        with self.assertRaises(ReservedName) as context:
          KeeMeta('Key', (KeeNum,), body, strictCase=False)
        self.assertEqual(context.exception.resName, name)
        self.assertEqual(str(context.exception),
                         "Attempted to use reserved name: '%s'!" % name)

  def test_names_of_the_bases_refused_without_the_case_rule(self) -> None:
    class Unit(KeeNum, strictCase=False):
      mm = Kee[int](1)
      label = 'unit'

      def describe(self) -> str:
        """A method every member has."""

    class Mixin:
      def render(self) -> str:
        """A method of a plain base."""

    for name in ('label', 'describe', 'render'):
      with self.subTest(name=name):
        body = {name: Kee[int](2)}
        with self.assertRaises(ReservedName) as context:
          KeeMeta('Imperial', (Unit, Mixin), body, strictCase=False)
        self.assertEqual(context.exception.resName, name)
        self.assertEqual(str(context.exception),
                         "Attempted to use reserved name: '%s'!" % name)

    class Imperial(Unit, Mixin, strictCase=False):
      inch = Kee[int](2)
      name = Kee[int](3)
      value = Kee[int](4)
      kee = Kee[int](5)

    names = [unit.name for unit in Imperial]
    self.assertEqual(names, ['mm', 'inch', 'name', 'value', 'kee'])
    self.assertEqual(Imperial.value.value, 4)
    self.assertEqual(Imperial.name.name, 'name')

  def test_strict_case_keeps_a_member_at_a_name_of_a_base(self) -> None:
    class Base(KeeNum):
      MAX = 3

    class Sub(Base):
      MAX = Kee[int](1)

    self.assertEqual([member.name for member in Sub], ['MAX'])
    self.assertIs(Sub.MAX, Sub('max'))
    self.assertEqual(Base.MAX, 3)
    with self.assertRaises(ReservedName) as context:
      class Loose(Base, strictCase=False):
        MAX = Kee[int](1)

    self.assertEqual(context.exception.resName, 'MAX')
    self.assertEqual(str(context.exception),
                     "Attempted to use reserved name: 'MAX'!")

  def test_reserved_name_by_hand(self) -> None:
    loose = KeeSpace(KeeMeta, 'Hand', (KeeNum,), strictCase=False)
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(loose, KeeSpace)
    for name in ('space', 'owners'):
      with self.subTest(name=name):
        with self.assertRaises(ReservedName) as context:
          hook.setItemPhase(name, Kee[int](1))
        self.assertEqual(context.exception.resName, name)
        self.assertEqual(str(context.exception),
                         "Attempted to use reserved name: '%s'!" % name)
        self.assertFalse(loose.hasNum(name))
    self.assertTrue(hook.setItemPhase('spaces', Kee[int](1)))
    self.assertTrue(loose.hasNum('spaces'))

  def test_subclass_takes_the_case_rule_of_its_base(self) -> None:
    class Base(KeeNum, strictCase=False):
      mm = Kee[int](1)

    class Sub(Base):
      km = Kee[int](2)

    class Leaf(Sub):
      nm = Kee[int](3)

    self.assertEqual([m.name for m in Sub], ['mm', 'km'])
    self.assertEqual([m.name for m in Leaf], ['mm', 'km', 'nm'])
    self.assertIs(Leaf('NM'), Leaf.nm)

  def test_subclass_may_take_the_case_rule_back(self) -> None:
    class Base(KeeNum, strictCase=False):
      mm = Kee[int](1)

    with self.assertRaises(KeeCaseException) as context:
      class Tight(Base, strictCase=True):
        km = Kee[int](2)

    self.assertEqual(context.exception.name, 'km')
    self.assertIn("must have upper case names, but received: 'km'",
                  str(context.exception))

    class Tight(Base, strictCase=True):
      KM = Kee[int](2)

    with self.assertRaises(KeeCaseException) as context:
      class Below(Tight):
        nm = Kee[int](3)

    self.assertEqual(context.exception.name, 'nm')
    self.assertIn("must have upper case names, but received: 'nm'",
                  str(context.exception))

    class Again(Tight, strictCase=False):
      nm = Kee[int](3)

    self.assertEqual([m.name for m in Again], ['mm', 'KM', 'nm'])

  def test_nearest_class_giving_the_keyword_decides(self) -> None:
    class Silent(KeeNum):
      INCH = Kee[int](1)

    class Loose(KeeNum, strictCase=False):
      mm = Kee[int](2)

    class Tight(KeeNum, strictCase=True):
      YARD = Kee[int](3)

    class Plain:
      """A base that no worktoy namespace built."""

    class SilentFirst(Silent, Loose):
      ft = Kee[int](4)

    class PlainFirst(Plain, Loose):
      ft = Kee[int](4)

    class LooseFirst(Loose, Tight):
      ft = Kee[int](4)

    self.assertEqual([m.name for m in SilentFirst], ['INCH', 'mm', 'ft'])
    self.assertEqual([m.name for m in PlainFirst], ['mm', 'ft'])
    self.assertEqual([m.name for m in LooseFirst], ['mm', 'YARD', 'ft'])
    with self.assertRaises(KeeCaseException) as context:
      class TightFirst(Tight, Loose):
        ft = Kee[int](4)

    self.assertEqual(context.exception.name, 'ft')
    self.assertIn("must have upper case names, but received: 'ft'",
                  str(context.exception))

  def test_case_rule_of_the_bases_by_hand(self) -> None:
    class Loose(KeeNum, strictCase=False):
      mm = Kee[int](1)

    hook = KeeSpace.__dict__['keeSpaceHook']
    inherited = KeeSpace(KeeMeta, 'Hand', (Loose,))
    self.assertTrue(
        hook.__get__(inherited, KeeSpace).setItemPhase('km', Kee[int](2)))
    tight = KeeSpace(KeeMeta, 'Hand', (Loose,), strictCase=True)
    with self.assertRaises(KeeCaseException) as context:
      hook.__get__(tight, KeeSpace).setItemPhase('km', Kee[int](2))
    self.assertEqual(context.exception.name, 'km')
    self.assertIn("must have upper case names, but received: 'km'",
                  str(context.exception))

  def test_case_by_hand(self) -> None:
    names = ('red', 'Red', 'rED', 'red_one')
    strict = KeeSpace(KeeMeta, 'Hand', ())
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(strict, KeeSpace)
    for name in names:
      with self.subTest(name=name, strictCase=True):
        with self.assertRaises(KeeCaseException) as context:
          hook.setItemPhase(name, Kee[int](1))
        self.assertEqual(context.exception.name, name)
        self.assertIn(name, str(context.exception))
        self.assertFalse(strict.hasNum(name))
    self.assertTrue(hook.setItemPhase('RED_ONE', Kee[int](1)))
    for name in names:
      with self.subTest(name=name, strictCase=False):
        loose = KeeSpace(KeeMeta, 'Hand', (), strictCase=False)
        hook = KeeSpace.__dict__['keeSpaceHook'].__get__(loose, KeeSpace)
        self.assertTrue(hook.setItemPhase(name, Kee[int](1)))
        self.assertTrue(loose.hasNum(name))
