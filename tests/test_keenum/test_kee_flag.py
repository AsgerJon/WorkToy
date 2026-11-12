"""
TestKeeFlag tests 'KeeFlag' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import warnings

from worktoy.keenum import KeeFlag, KeeFlagsMeta, KeeFlags
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import DeprecatedPromise
from . import KeenumTest, Permission

HERE = sys._getframe().f_code.co_filename


class TestKeeFlag(KeenumTest):
  """
  A 'KeeFlag' declares one flag. It is deprecated: each one made gives a
  'DeprecatedPromise' at the line that made it, and declares the flag as
  before, a 'Kee' declaring it instead. It keeps the constructor
  arguments, receives its name from the namespace and its owner and its
  bit from the class built. The tests pin the notice, and, with the
  notice silenced, the getters and their refusals before and after
  placement, the placement outside a flags class, the texts, the
  integer, the equality, the hash and the clone.
  """

  def setUp(self) -> None:
    super().setUp()
    catcher = warnings.catch_warnings()
    catcher.__enter__()
    self.addCleanup(catcher.__exit__, None, None, None)
    warnings.simplefilter('ignore', DeprecatedPromise)

  def test_deprecation_notice(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      line = sys._getframe().f_lineno + 1
      flag = KeeFlag(1)
      clone = flag.clone(Permission, 0)
    self.assertEqual(len(log), 1)
    entry = log[0]
    self.assertIs(entry.category, DeprecatedPromise)
    self.assertEqual(entry.filename, HERE)
    self.assertEqual(entry.lineno, line)
    self.assertIs(entry.message.feature, KeeFlag)
    self.assertEqual(entry.message.description, str.join(' ', """Declare
      the flag with 'Kee' instead, as 'READ = Kee[str]()'.""".split()))
    self.assertEqual(clone.args, (1,))

  def test_fresh_flag(self) -> None:
    flag = KeeFlag(1, two=2)
    self.assertEqual(flag.args, (1,))
    self.assertEqual(flag.kwargs, {'two': 2})
    self.assertEqual(KeeFlag().args, ())
    self.assertEqual(KeeFlag().kwargs, {})
    for field, slot, type_ in (('fieldName', '__field_name__', str),
                               ('fieldOwner', '__field_owner__',
                                KeeFlagsMeta),
                               ('index', '__member_index__', int),
                               ('name', '__member_name__', str)):
      with self.subTest(field=field):
        with self.assertRaises(MissingVariable) as context:
          getattr(flag, field)
        self.assertIs(context.exception.instance, flag)
        self.assertEqual(context.exception.varName, slot)
        self.assertEqual(context.exception.expectedTypes, (type_,))
        expected = "Missing 'KeeFlag.%s: %s'!" % (slot, type_.__name__)
        self.assertEqual(str(context.exception), expected)
    self.assertEqual(str(flag), object.__str__(flag))
    self.assertEqual(repr(flag), object.__repr__(flag))
    with self.assertRaises(TypeError) as context:
      iter(flag)
    self.assertEqual(str(context.exception), 'KeeFlag is not iterable!')

  def test_placed_flag(self) -> None:
    class Local(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()
      EXEC = KeeFlag()

    read = Local.READ.kee
    self.assertIsInstance(read, KeeFlag)
    self.assertIs(read.fieldOwner, Local)
    self.assertEqual(read.fieldName, 'READ')
    self.assertEqual(read.name, 'READ')
    self.assertEqual(read.index, 0)
    self.assertEqual(int(read), 0)
    self.assertEqual(['first', 'second'][read], 'first')
    self.assertEqual(['a', 'b', 'c'][Local.EXEC.kee], 'c')
    self.assertEqual(str(read), 'Local.READ [0]')
    self.assertEqual(repr(read), 'Local.READ [0]: KeeFlag()')
    self.assertEqual(Local.READ.value, 'READ')
    self.assertIs(Local.READ | Local.WRITE, Local.READ_WRITE)

  def test_text_with_arguments(self) -> None:
    flag = KeeFlag(1, 'b', k=3)
    flag.__field_name__ = 'MIX'
    flag.__member_name__ = 'MIX'
    placed = flag.clone(Permission, 4)
    self.assertEqual(repr(placed),
                     "Permission.MIX [4]: KeeFlag(1, 'b', k=3)")
    self.assertEqual(str(placed), 'Permission.MIX [4]')
    keyed = KeeFlag(k=3)
    keyed.__member_name__ = 'KEYED'
    keyed.__field_name__ = 'KEYED'
    self.assertEqual(repr(keyed.clone(Permission, 1)),
                     'Permission.KEYED [1]: KeeFlag(k=3)')

  def test_settings_of_wrong_type_refused(self) -> None:
    flag = KeeFlag()
    flag.__field_name__ = 5
    flag.__field_owner__ = 'owner'
    flag.__member_index__ = 'x'
    flag.__member_name__ = 7
    for field, slot, value in (('fieldName', '__field_name__', 5),
                               ('fieldOwner', '__field_owner__', 'owner'),
                               ('index', '__member_index__', 'x'),
                               ('name', '__member_name__', 7)):
      with self.subTest(field=field):
        with self.assertRaises(TypeException) as context:
          getattr(flag, field)
        self.assertEqual(context.exception.varName, slot)
        self.assertEqual(context.exception.actualObject, value)
        self.assertIs(context.exception.actualType, type(value))
        self.assertEqual(len(context.exception.expectedTypes), 1)
        self.assertIn("'%s'" % slot, str(context.exception))
        self.assertIn("'%s'" % type(value).__name__,
                      str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      _ = KeeFlag().fieldOwner
    self.assertIsInstance(context.exception.instance, KeeFlag)
    self.assertEqual(context.exception.varName, '__field_owner__')
    self.assertEqual(context.exception.expectedTypes, (KeeFlagsMeta,))
    self.assertEqual(str(context.exception),
                     "Missing 'KeeFlag.__field_owner__: KeeFlagsMeta'!")

  def test_placed_only_in_a_flags_class(self) -> None:
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Plain:
        READ = KeeFlag()

    exception = context.exception.__cause__ or context.exception
    self.assertIn("'Plain' is no flags class", str(exception))
    self.assertIn("'READ'", str(exception))
    with self.assertRaises(TypeError) as context:
      KeeFlag().__set_name__(int, 'READ')
    self.assertIn("'int' is no flags class", str(context.exception))
    self.assertIn("'READ'", str(context.exception))

  def test_equality_and_hash(self) -> None:
    class Local(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

    class Other(KeeFlags):
      READ = KeeFlag()

    read, write = Local.READ.kee, Local.WRITE.kee
    self.assertEqual(read, Local.READ.kee)
    self.assertNotEqual(read, write)
    self.assertNotEqual(write, read)
    self.assertIs(read.__eq__(1), NotImplemented)
    self.assertFalse(read == 1)
    self.assertIs(read.__eq__(Other.READ.kee), NotImplemented)
    self.assertFalse(read == Other.READ.kee)
    self.assertEqual(hash(read), hash((Local, 'READ', 0)))
    self.assertEqual({read: 1}[Local.READ.kee], 1)

  def test_clone(self) -> None:
    flag = KeeFlag(1, k=2)
    flag.__member_name__ = 'READ'
    flag.__field_name__ = 'READ'
    flag.__member_index__ = 3
    cloned = flag.clone(Permission)
    self.assertIsNot(cloned, flag)
    self.assertEqual(cloned.args, (1,))
    self.assertEqual(cloned.kwargs, {'k': 2})
    self.assertEqual(cloned.name, 'READ')
    self.assertEqual(cloned.fieldName, 'READ')
    self.assertIs(cloned.fieldOwner, Permission)
    self.assertEqual(cloned.index, 3)
    self.assertEqual(flag.clone(Permission, 5).index, 5)
    self.assertEqual(flag.clone(Permission, 0).index, 0)

  def test_random_arguments(self) -> None:
    self.randomInteger.size = 5
    self.randomWord.size = 5
    for number, word in zip(self.randomInteger.row, self.randomWord.row):
      flag = KeeFlag(number, word=word)
      with self.subTest(number=number):
        self.assertEqual(flag.args, (number,))
        self.assertEqual(flag.kwargs, {'word': word})
        self.assertEqual(flag.clone(Permission, 0).args, (number,))
