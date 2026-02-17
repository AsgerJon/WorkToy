"""
TestFunction tests the 'Function' sentinel object.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import Function
from worktoy.core.sentinels._function import _MetaFunction
from worktoy.waitaminute.meta import IllegalInstantiation
from . import CoreTest, FuncLoad


class TestFunction(CoreTest):
  """
  TestFunction tests the 'Function' sentinel object.
  """

  def setUp(self) -> None:
    super().setUp()

    def func() -> None:
      """If you just put 'pass', it is not considered covered lmao"""

    self.funcExamples = [
      func, lambda: None,
      self.tearDownClass,
      type(self).tearDownClass,
      self.setUp,
      type(self).setUp,
      print,
      ]
    self.funcTypes = [type(func) for func in self.funcExamples]
    self.notFuncExamples = [
      69, 420, 'ur mom', None, True, [1337, ], (80085,), type,
      ]
    self.notFuncTypes = [type(notFunc) for notFunc in self.notFuncExamples]

  def testExistence(self, ) -> None:
    """
    Tests the existence of the 'Function' sentinel object.
    """
    self.assertIsInstance(Function, type)

  def testBadInstantiation(self, ) -> None:
    """
    Tests that only the one 'Function' object can exist.
    """

    with self.assertRaises(IllegalInstantiation) as context:
      class Sus(metaclass=_MetaFunction, ):
        pass
    e = context.exception
    self.assertIn('Illegal instantiation of class', str(e))
    self.assertEqual(str(e), repr(e))

  def testBadFuncTypes(self) -> None:
    """
    Tests that the function type list used by the 'Function' sentinel runs
    only once.
    """
    setattr(_MetaFunction, '__func_types__', None)
    with self.assertRaises(RecursionError) as context:
      _ = _MetaFunction._getFuncTypes(_recursion=True)
    self.assertIsInstance(_MetaFunction._getFuncTypes(), list)

  def testIsInstance(self, ) -> None:
    """
    Tests that function like objects are correctly recognized by
    'isinstance'.
    """
    for func in self.funcExamples:
      self.assertIsInstance(func, Function)

  def testIsSubclass(self, ) -> None:
    """
    Tests that function like objects are correctly recognized by
    'issubclass'.
    """
    for type_ in self.funcTypes:
      self.assertIsSubclass(type_, Function)

  def testNotInstance(self, ) -> None:
    """
    Tests that non-function like objects are correctly not recognized by
    'isinstance'.
    """
    for notFunc in self.notFuncExamples:
      self.assertNotIsInstance(notFunc, Function)

  def testNotSubclass(self, ) -> None:
    """
    Tests that non-function like objects are correctly not recognized by
    'issubclass'.
    """
    for type_ in self.notFuncTypes:
      self.assertNotIsSubclass(type_, Function)

  def testBadSubclassCheck(self, ) -> None:
    """
    Tests that a bad argument to 'issubclass' raises a 'TypeError'.
    """

    with self.assertRaises(TypeError) as context:
      _ = issubclass(69, Function)
    e = context.exception
    self.assertIn('issubclass() arg 1 must be a class', str(e))

  def testOverload(self) -> None:
    """
    Tests that the overloads of the 'Function' sentinel work as intended.
    """
    for func in self.funcExamples:
      funcLoad = FuncLoad(func)
      self.assertIs(funcLoad.init, func)
      self.assertTrue(funcLoad.load)

  def testNotOverload(self) -> None:
    """
    Tests that the overloads of the 'Function' sentinel work as intended.
    """
    notFuncs = [69, '420', .1337]
    for notFunc in notFuncs:
      funcLoad = FuncLoad(notFunc)
      self.assertIs(funcLoad.init, notFunc)
      self.assertFalse(funcLoad.load)
