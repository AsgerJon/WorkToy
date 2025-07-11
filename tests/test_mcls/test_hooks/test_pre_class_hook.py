"""
TestPreClassHook tests the 'PreClassHook' from the 'worktoy.mcls.hooks'
module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from .. import MCLSTest
from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import PreClassSpaceHook
from worktoy.static import PreClass, TypeSig
from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestPreClassHook(MCLSTest):
  """
  TestPreClassHook tests the 'PreClassHook' from the 'worktoy.mcls.hooks'
  module.
  """

  def test_recursion(self) -> None:
    """
    Tests that the 'PreClassHook' raises a 'RecursionError' if the hook
    is called recursively.
    """

    preClassHook = PreClassSpaceHook()
    with self.assertRaises(RecursionError):
      _ = preClassHook._getPreClass(_recursion=True)

  def test_bad_pre_class_type(self) -> None:
    """
    Tests that the 'PreClassHook' raises a 'QuestionableSyntax' if the
    pre-class is not a class.
    """
    susClass = """Imma PreClass, trust me bro!"""
    preClassHook = PreClassSpaceHook()
    setattr(preClassHook, '__pre_class__', susClass)
    with self.assertRaises(TypeException) as context:
      preClassHook._getPreClass()
    e = context.exception
    self.assertEqual(e.varName, '__pre_class__')
    self.assertIs(e.actualObject, susClass)
    self.assertIs(e.actualType, str)
    self.assertIs(e.expectedTypes[0], PreClass, )

  def test_bad_type_sig(self) -> None:
    """
    Tests that the 'PreClassHook' raises a 'TypeException' if the
    pre-class has a bad type signature.
    """
    preClassHook = PreClassSpaceHook()
    setattr(preClassHook, '__pre_class__', PreClass('breh', 69420, ()))
    susTypeSigs = stringList("""yo, we be your TypeSigs, trust!""")
    setattr(preClassHook, '__type_sigs__', susTypeSigs)

    class Sus:
      __type_sigs__ = 'never', 'gonna', 'give', 'you', 'up'

    key = 'breh'
    val = Sus()
    oldValue = 'urMom'

    with self.assertRaises(TypeException) as context:
      preClassHook.setItemPhase(key, val, oldValue)
    e = context.exception
    self.assertEqual(e.varName, 'sig')
    self.assertEqual(e.actualObject, 'never')
    self.assertIs(e.actualType, str)
    self.assertIs(e.expectedTypes[0], TypeSig)
