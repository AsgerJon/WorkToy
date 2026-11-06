"""
TestTypeSigValidate tests 'TypeSig.validateTypes' from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core.sentinels import THIS, DELETED, ARGS
from worktoy.dispatch import TypeSig
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, UncheckableType
from . import DispatchTest, Uncheckable


class TestTypeSigValidate(DispatchTest):
  """
  A declared signature no call could match must be refused where it is
  written. The tests pin the entries that pass, the refusal of 'None',
  of anything that is no class, of a sentinel other than 'THIS', of a
  class 'isinstance' refuses, the trailing 'ARGS' with its inner type
  checked, the refusal of an 'ARGS' anywhere else or under
  'variadic=False', and the message naming a box's subscript.
  """

  def test_plain_classes_pass(self) -> None:
    TypeSig.validateTypes(int, str, bytes)
    TypeSig.validateTypes()
    TypeSig.validateTypes(THIS, int)
    TypeSig.validateTypes(BaseObject)
    TypeSig.validateTypes(MetaType('Made', (), {}))

  def test_trailing_args_inner_checked(self) -> None:
    TypeSig.validateTypes(int, ARGS[str])
    TypeSig.validateTypes(ARGS[THIS])
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(int, ARGS[None])
    self.assertIn('position 1', str(context.exception))
    with self.assertRaises(TypeException) as context:
      TypeSig.validateTypes(ARGS[5])
    self.assertEqual(context.exception.varName, 'types[0]')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[0]'", str(context.exception))

  def test_args_not_last_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      TypeSig.validateTypes(ARGS[int], str)
    self.assertEqual(context.exception.varName, 'types[0]')
    self.assertEqual(context.exception.actualObject, ARGS[int])
    self.assertIs(context.exception.actualType, ARGS)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[0]'", str(context.exception))

  def test_args_refused_when_not_variadic(self) -> None:
    with self.assertRaises(TypeException) as context:
      TypeSig.validateTypes(int, ARGS[str], variadic=False)
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertEqual(context.exception.actualObject, ARGS[str])
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[1]'", str(context.exception))

  def test_none_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(int, None)
    self.assertIn("position 1 of the signature is 'None'",
                  str(context.exception))
    self.assertIn("'type(None)'", str(context.exception))
    TypeSig.validateTypes(type(None))

  def test_value_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      TypeSig.validateTypes(int, 'str')
    self.assertEqual(context.exception.varName, 'types[1]')
    self.assertEqual(context.exception.actualObject, 'str')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[1]'", str(context.exception))

  def test_sentinel_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(DELETED)
    self.assertIn("sentinel 'DELETED'", str(context.exception))
    self.assertIn("'THIS' stands for the class", str(context.exception))
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(int, ARGS)
    self.assertIn("position 1 of the signature is the sentinel 'ARGS'",
                  str(context.exception))

  def test_uncheckable_class_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      isinstance(None, Uncheckable)
    self.assertEqual(str(context.exception),
                     'Uncheckable cannot be used with isinstance()')
    with self.assertRaises(UncheckableType) as context:
      TypeSig.validateTypes(int, Uncheckable)
    self.assertIs(context.exception.entry, Uncheckable)
    self.assertEqual(context.exception.position, 1)
    self.assertEqual(context.exception.declaration, '(int, Uncheckable)')
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("'Uncheckable' at position 1", str(context.exception))
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIs(context.exception.__cause__, context.exception.refusal)

  def test_uncheckable_names_box_subscript(self) -> None:
    with self.assertRaises(UncheckableType) as context:
      TypeSig.validateTypes(Uncheckable, declaration='AttriBox[Uncheckable]')
    self.assertEqual(context.exception.declaration, 'AttriBox[Uncheckable]')
    self.assertIsNone(context.exception.position)
    self.assertIs(context.exception.entry, Uncheckable)
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("box 'AttriBox[Uncheckable]'", str(context.exception))

  def test_uncheckable_inner_type(self) -> None:
    with self.assertRaises(UncheckableType) as context:
      TypeSig.validateTypes(ARGS[Uncheckable])
    self.assertIs(context.exception.entry, Uncheckable)
    self.assertEqual(context.exception.position, 0)
    self.assertEqual(context.exception.declaration, '(ARGS[Uncheckable])')
    self.assertIsInstance(context.exception.refusal, TypeError)
    self.assertIn("'Uncheckable' at position 0", str(context.exception))

  def test_trailing_args_after_two_entries(self) -> None:
    TypeSig.validateTypes(int, str, ARGS[float])
    TypeSig.validateTypes(int, str, bytes, ARGS[THIS])

  def test_entries_after_this_still_checked(self) -> None:
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(THIS, None)
    self.assertIn("position 1 of the signature is 'None'",
                  str(context.exception))
    with self.assertRaises(TypeError) as context:
      TypeSig.validateTypes(BaseObject, None)
    self.assertIn("position 1 of the signature is 'None'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      TypeSig.validateTypes(THIS, BaseObject, 'x')
    self.assertEqual(context.exception.varName, 'types[2]')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'types[2]'", str(context.exception))
