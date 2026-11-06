"""
TestQuickDesc tests 'QuickDesc' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import QuickDesc
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import UtilitiesTest, QuickOwner


class TestQuickDesc(UtilitiesTest):
  """
  'QuickDesc' exposes a private slot under a public name, read-only,
  for the foundation packages that cannot use the descriptors of
  'worktoy.desc'. The tests pin the read through the instance and
  through the class, that a slot never set is read past the owner's
  '__getattr__' so that it is asked for the public name, that writes and
  deletions are refused, that a descriptor without a key is refused
  with 'MissingVariable', and that a key equal to the field name is a
  'ValueError'.
  """

  def test_instance_read(self) -> None:
    self.assertEqual(QuickOwner().value, 42)

  def test_class_read_is_descriptor(self) -> None:
    self.assertIsInstance(QuickOwner.value, QuickDesc)

  def test_set_name_records_name_and_owner(self) -> None:
    desc = QuickOwner.value
    self.assertEqual(desc.__field_name__, 'value')
    self.assertIs(desc.__field_owner__, QuickOwner)

  def test_missing_slot_asks_getattr_for_public_name(self) -> None:
    #  The descriptor reads the slot past '__getattr__', so the owner is
    #  never asked for the private key; the 'AttributeError' leaving the
    #  descriptor makes Python ask it for the public name instead.
    owner = QuickOwner()
    self.assertEqual(owner.anything, 'anything')
    self.assertEqual(owner.missing, 'missing')
    with self.assertRaises(AttributeError):
      QuickOwner.missing.__get__(owner, QuickOwner)

  def test_keyless_descriptor_refused(self) -> None:
    desc = QuickDesc.__new__(QuickDesc)
    with self.assertRaises(MissingVariable) as context:
      desc.__get__(QuickOwner(), QuickOwner)
    self.assertIs(context.exception.instance, desc)
    self.assertEqual(context.exception.varName, '__private_key__')
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'QuickDesc.__private_key__: str'", str(context.exception))

  def test_set_refused(self) -> None:
    owner = QuickOwner()
    with self.assertRaises(ReadOnlyError) as context:
      owner.value = 69
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, QuickOwner.value)
    self.assertEqual(context.exception.newVal, 69)
    self.assertIn("'QuickOwner.value'", str(context.exception))
    self.assertIn("'69'", str(context.exception))
    self.assertEqual(owner.value, 42)

  def test_delete_refused(self) -> None:
    owner = QuickOwner()
    with self.assertRaises(ProtectedError) as context:
      del owner.value
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, QuickOwner.value)
    self.assertIsNone(context.exception.oldVal)
    self.assertIn("'QuickOwner.value'", str(context.exception))
    self.assertIn("'None'", str(context.exception))
    self.assertEqual(owner.value, 42)

  def test_key_equal_to_name_refused(self) -> None:
    desc = QuickDesc('value')
    with self.assertRaises(ValueError) as context:
      desc.__set_name__(QuickOwner, 'value')
    self.assertIn("both being: 'value'", str(context.exception))
    self.assertIsNone(desc.__field_name__)
    #  Equal by value is enough; the key need not be the same object.
    desc = QuickDesc(str.join('', ('val', 'ue')))
    with self.assertRaises(ValueError) as context:
      desc.__set_name__(QuickOwner, 'value')
    self.assertIn("both being: 'value'", str(context.exception))

  def test_other_key_accepted_whatever_its_order(self) -> None:
    for key in ('aaa', 'zzz'):
      desc = QuickDesc(key)
      desc.__set_name__(QuickOwner, 'mmm')
      with self.subTest(key=key):
        self.assertEqual(desc.__field_name__, 'mmm')
        self.assertIs(desc.__field_owner__, QuickOwner)
