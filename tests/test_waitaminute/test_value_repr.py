"""
TestValueRepr tests how the messages of 'worktoy.waitaminute' show a
value.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from decimal import Decimal

from worktoy.core import Object
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute import WorkToyException, TypeException
from worktoy.waitaminute import VariableNotNone, UnpackException
from worktoy.waitaminute import RiskWarning
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError
from worktoy.waitaminute.desc import WriteOnceError, NotADescriptor
from worktoy.waitaminute.dispatch import TypeCastException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.keenum import KeeResolveError, KeeTypeException
from worktoy.waitaminute.keenum import KeeBoxException, KeeBoxTypeError
from worktoy.waitaminute.keenum import KeeBoxValueError
from worktoy.waitaminute.meta import HookException
from . import WaitaminuteTest


class TestValueRepr(WaitaminuteTest):
  """
  A message that shows a value shows its 'repr', so that the string
  '12', the number 12 and a 'Decimal' of 12 read differently and an
  empty string is seen. The 'repr' brings the quotes of a string
  itself, so the message puts none around a value, and a 'repr' longer
  than 50 characters is cut to 47 and three dots. Names keep their
  quotes. The tests pin the helper and the text of each message that
  shows a value.
  """

  LONG = 'x' * 60
  CUT = """%s...""" % repr('x' * 60)[:47]

  @staticmethod
  def _placed() -> tuple:
    class Owner:
      d = Object()

    return Owner(), Owner.__dict__['d']

  def test_helper(self) -> None:
    reprOf = WorkToyException._reprOf
    self.assertEqual(reprOf('12'), "'12'")
    self.assertEqual(reprOf(12), '12')
    self.assertEqual(reprOf(Decimal(12)), "Decimal('12')")
    self.assertEqual(reprOf(''), "''")
    fits = 'x' * 48  # shown in 50 characters, quotes included
    self.assertEqual(reprOf(fits), repr(fits))
    long = 'x' * 49  # shown in 51 characters
    self.assertEqual(reprOf(long), """%s...""" % repr(long)[:47])
    self.assertEqual(len(reprOf(long)), 50)
    self.assertEqual(len(self.CUT), 50)

  def test_type_cast_exception(self) -> None:
    cases = (
      ('12', "Unable to cast value '12' to type 'int'!"),
      (Decimal(12), "Unable to cast value Decimal('12') to type 'int'!"),
      ('', "Unable to cast value '' to type 'int'!"),
    )
    for value, expected in cases:
      with self.subTest(value=value):
        self.assertEqual(str(TypeCastException(int, value)), expected)

  def test_type_exception(self) -> None:
    expected = """Expected object at name 'pages' to be an instance of
    'int', but received object: '12' of type 'str'!"""
    exception = TypeException('pages', '12', int)
    self.assertEqual(str(exception), str.join(' ', expected.split()))
    self.assertIn(self.CUT, str(TypeException('pages', self.LONG, int)))

  def test_variable_not_none(self) -> None:
    expected = "Unexpected value: 7 at name 'index' expected to be None!"
    self.assertEqual(str(VariableNotNone('index', 7)), expected)
    expected = "Unexpected value: '7' at name 'index' expected to be None!"
    self.assertEqual(str(VariableNotNone('index', '7')), expected)

  def test_unpack_exception(self) -> None:
    lines = str(UnpackException(1, '1')).splitlines()
    self.assertEqual(lines[1:3], ['  1', "  '1'"])

  def test_risk_warning(self) -> None:
    expected = """Received object at name 'price': 'cheap' of type 'str'.
    This is promised to function correctly, but risks a loss!"""
    warning = RiskWarning('price', 'cheap', 'a loss')
    self.assertEqual(str(warning), str.join(' ', expected.split()))

  def test_protected_error(self) -> None:
    owner, desc = self._placed()
    expected = """Attempted to delete protected attribute 'Owner.d' with
    value: %s"""
    for value in (250, '250', Decimal(250)):
      with self.subTest(value=value):
        text = str.join(' ', (expected % repr(value)).split())
        self.assertEqual(str(ProtectedError(owner, desc, value)), text)

  def test_read_only_error(self) -> None:
    owner, desc = self._placed()
    expected = """Attempted to overwrite read-only attribute 'Owner.d'
    with new value: %s!"""
    for value in (69, '69'):
      with self.subTest(value=value):
        text = str.join(' ', (expected % repr(value)).split())
        self.assertEqual(str(ReadOnlyError(owner, desc, value)), text)

  def test_write_once_error(self) -> None:
    _, desc = self._placed()
    expected = """Attempted to overwrite write-once attribute at 'Owner.d'
    having existing value: 1 with new value: '1'!"""
    exception = WriteOnceError(desc, 1, '1')
    self.assertEqual(str(exception), str.join(' ', expected.split()))

  def test_not_a_descriptor(self) -> None:
    text = str(NotADescriptor(object(), 'x', '12'))
    self.assertIn("which holds '12' of type 'str' rather", text)
    self.assertIn(self.CUT, str(NotADescriptor(object(), 'x', self.LONG)))

  def test_kee_resolve_error(self) -> None:
    class Day:
      pass

    expected = """Enumeration 'Day' could not resolve the identifier %s
    to any of its members!"""
    for value in (7, '7'):
      with self.subTest(value=value):
        text = str.join(' ', (expected % repr(value)).split())
        self.assertEqual(str(KeeResolveError(Day, value)), text)

  def test_kee_type_exception(self) -> None:
    expected = """Member 'MON' has value %s of type '%s', but expected
    the value to be an instance of 'int'!"""
    for value in (1.5, '1'):
      with self.subTest(value=value):
        names = (repr(value), type(value).__name__)
        text = str.join(' ', (expected % names).split())
        self.assertEqual(str(KeeTypeException('MON', value, int)), text)

  def test_kee_box_value_error(self) -> None:
    text = str(KeeBoxValueError(object(), object(), '12'))
    self.assertIn("received value of correct type: '12', which", text)

  def test_kee_box_arguments_are_cut(self) -> None:
    for exception in (
        KeeBoxException('box', (self.LONG,)),
        KeeBoxTypeError(object(), self.LONG),
    ):
      with self.subTest(exception=type(exception).__name__):
        self.assertIn("""<str: %s>""" % self.CUT, str(exception))
        self.assertNotIn(repr(self.LONG), str(exception))

  def test_hook_exception(self) -> None:
    expected = """HookException raised from space! Key: 'key', Value:
    '12', Hook: 'hook'! Initial exception: ValueError('no')"""
    exception = HookException(ValueError('no'), 'space', 'key', '12', 'hook')
    self.assertEqual(str(exception), str.join(' ', expected.split()))

  def test_dispatch_exception_cuts_arguments(self) -> None:
    class Scale(BaseObject):
      @overload(int)
      def grow(self, factor: int) -> int:
        return factor

    self.assertEqual(Scale().grow(2), 2)
    with self.assertRaises(DispatchException) as context:
      Scale().grow(self.LONG)
    self.assertIn("""<str %s>""" % self.CUT, str(context.exception))
    self.assertNotIn(repr(self.LONG), str(context.exception))
