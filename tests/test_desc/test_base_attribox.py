"""TestBaseAttriBox tests the basic functionalities of the AttriBox. This
includes the accessor functions, correct use of arguments to construct the
initial values, correct behaviour of field classes in AttriBox that
themselves implement AttriBox fields. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox

# from worktoy.meta import BaseObject

BaseObject = object


class BaseTypes(BaseObject):
  """BaseTypes class"""

  attrStr = AttriBox[str]()
  attrFloat = AttriBox[float]()
  attrInt = AttriBox[int]()
  attrBool = AttriBox[bool]()  # Special behaviour implemented.
  attrList = AttriBox[list]()
  attrDict = AttriBox[dict]()


class SmartList(list):
  """This vastly superior list will instantiate if passed positional
  arguments by putting them in a list. Unstupidly."""

  def __init__(self, *args) -> None:
    """This method instantiates the SmartList."""
    if len(args) == 1:
      list.__init__(self, args[0])
    elif len(args) > 1:
      list.__init__(self, (*args,))
    else:
      list.__init__(self)


class ConstructedValues(BaseObject):
  """BaseTypes class, but with values to be constructed. """

  attrStr = AttriBox[str](type('LOL', (), {}))
  attrFloat = AttriBox[float](69)
  attrInt = AttriBox[int](420.0)
  attrBool = AttriBox[bool](True)
  attrList = AttriBox[list]((69, 420))  # LOL that you can't pass *args
  attrSmartList = AttriBox[SmartList](69, 420)  # Like this
  attrDict = AttriBox[dict](lmao=True, js='trash')


class InitValues(BaseObject):
  """BaseTypes class allowing init function to set values"""

  attrStr = AttriBox[str]()
  attrFloat = AttriBox[float]()
  attrInt = AttriBox[int]()
  attrBool = AttriBox[bool]()
  attrList = AttriBox[list]()
  attrDict = AttriBox[dict]()

  def __init__(self, *args) -> None:
    """This method sets the values of the AttriBox instances. """
    args = [*args, str(), float(), int(), False, list(), dict(), ]
    self.attrStr = args[0]
    self.attrFloat = args[1]
    self.attrInt = args[2]
    self.attrBool = args[3]
    self.attrList = args[4]
    self.attrDict = args[5]


class NestedValues(BaseObject):
  """Class containing AttriBox instances that themselves contain AttriBox
  instances. """

  __default_values__ = ('LOL', 69., 420, True, [1337, ], {'lmao': True, })

  base = AttriBox[BaseTypes]()
  values = AttriBox[ConstructedValues]()
  initVals = AttriBox[InitValues]()  # Empty values
  defVals = AttriBox[InitValues](*__default_values__, )  # First try lol
  setVals = AttriBox[InitValues]()

  def __init__(self, *args) -> None:
    self.setVals = args


class TestBaseAttriBox(TestCase):
  """TestAttriBox tests the AttriBox implementation of the descriptor
  protocol. """

  def setUp(self, ) -> None:
    """Set up the test class."""
    self.sampleValues = ['LOL', 69., 420, True, [1337, ], {'lmao': True, }]
    self.baseTypes = BaseTypes()
    self.values = ConstructedValues()
    self.nested = NestedValues(*self.sampleValues)

  def test_nested_values(self, ) -> None:
    """Testing that nested values nest"""
    self.assertEqual(self.nested.base.attrStr, str())
    self.assertEqual(self.nested.base.attrFloat, float())
    self.assertEqual(self.nested.base.attrInt, int())
    self.assertEqual(self.nested.base.attrBool, bool())
    self.assertEqual(self.nested.base.attrList, list())
    self.assertEqual(self.nested.base.attrDict, dict())
    self.assertEqual(self.nested.values.attrStr, str(type('LOL', (), {})))
    self.assertEqual(self.nested.values.attrFloat, 69)
    self.assertEqual(self.nested.values.attrInt, 420)
    self.assertEqual(self.nested.values.attrBool, True)
    self.assertEqual(self.nested.values.attrList, [69, 420])
    self.assertEqual(self.nested.values.attrDict,
                     {'lmao': True, 'js': 'trash'})
    self.assertEqual(self.nested.initVals.attrStr, str())
    self.assertEqual(self.nested.initVals.attrFloat, float())
    self.assertEqual(self.nested.initVals.attrInt, int())
    self.assertEqual(self.nested.initVals.attrBool, bool())
    self.assertEqual(self.nested.initVals.attrList, list())
    self.assertEqual(self.nested.initVals.attrDict, dict())
    self.assertEqual(self.nested.defVals.attrStr, 'LOL')
    self.assertEqual(self.nested.defVals.attrFloat, 69.)
    self.assertEqual(self.nested.defVals.attrInt, 420)
    self.assertEqual(self.nested.defVals.attrBool, True)
    self.assertEqual(self.nested.defVals.attrList, [1337, ])
    self.assertEqual(self.nested.defVals.attrDict, {'lmao': True, })
    self.assertEqual(self.nested.setVals.attrStr, 'LOL')
    self.assertEqual(self.nested.setVals.attrFloat, 69.)
    self.assertEqual(self.nested.setVals.attrInt, 420)
    self.assertEqual(self.nested.setVals.attrBool, True)
    self.assertEqual(self.nested.setVals.attrList, [1337, ])
    self.assertEqual(self.nested.setVals.attrDict, {'lmao': True, })

  def test_constructed_values(self, ) -> None:
    """Testing that the fields in the 'ConstructedValues' instance correctly
    instantiates. """
    self.assertEqual(self.values.attrStr, str(type('LOL', (), {})))
    self.assertEqual(self.values.attrFloat, 69)
    self.assertEqual(self.values.attrInt, 420)
    self.assertEqual(self.values.attrBool, True)
    self.assertEqual(self.values.attrList, [69, 420])
    self.assertEqual(self.values.attrSmartList, [69, 420])
    self.assertEqual(self.values.attrDict, {'lmao': True, 'js': 'trash'})

  def test_base_values(self) -> None:
    """Testing that the fields in the 'BaseTypes' instance correctly
    instantiates. """
    self.assertEqual(self.baseTypes.attrStr, str())
    self.assertEqual(self.baseTypes.attrFloat, float())
    self.assertEqual(self.baseTypes.attrInt, int())
    self.assertEqual(self.baseTypes.attrBool, bool())
    self.assertEqual(self.baseTypes.attrList, list())
    self.assertEqual(self.baseTypes.attrDict, dict())

  def test_setters(self, ) -> None:
    """Testing that the fields in the 'BaseTypes' instance behave
    correctly when setting values. """
    self.baseTypes.attrStr = 'Hello'
    self.baseTypes.attrFloat = 3.14
    self.baseTypes.attrInt = 42
    self.baseTypes.attrBool = True
    self.baseTypes.attrList = [1, 2, 3]
    self.baseTypes.attrDict = {'a': 1, 'b': 2}
    self.assertEqual(self.baseTypes.attrStr, 'Hello')
    self.assertEqual(self.baseTypes.attrFloat, 3.14)
    self.assertEqual(self.baseTypes.attrInt, 42)
    self.assertEqual(self.baseTypes.attrBool, True)
    self.assertEqual(self.baseTypes.attrList, [1, 2, 3])
    self.assertEqual(self.baseTypes.attrDict, {'a': 1, 'b': 2})

  def test_setter_errors(self) -> None:
    """Testing that the fields in the 'BaseTypes' instance raise the
    correct type errors. """
    with self.assertRaises(TypeError):
      self.baseTypes.attrFloat = 'LMAO'
      self.baseTypes.attrInt = 'LMAO'
      self.baseTypes.attrBool = 'LMAO'
      self.baseTypes.attrList = 'LMAO'
      self.baseTypes.attrDict = 'LMAO'
    with self.assertRaises(TypeError):
      self.baseTypes.attrStr = 69.0
      self.baseTypes.attrBool = 69.0
      self.baseTypes.attrList = 69.0
      self.baseTypes.attrDict = 69.0
    with self.assertRaises(TypeError):
      self.baseTypes.attrStr = 420
      self.baseTypes.attrBool = 420
      self.baseTypes.attrList = 420
      self.baseTypes.attrDict = 420
    with self.assertRaises(TypeError):
      self.baseTypes.attrStr = True
      self.baseTypes.attrFloat = True
      self.baseTypes.attrInt = True
      self.baseTypes.attrList = True
      self.baseTypes.attrDict = True
    with self.assertRaises(TypeError):
      self.baseTypes.attrStr = [69, 420, 1337, 80085]
      self.baseTypes.attrFloat = [69, 420, 1337, 80085]
      self.baseTypes.attrInt = [69, 420, 1337, 80085]
      self.baseTypes.attrBool = [69, 420, 1337, 80085]
      self.baseTypes.attrDict = [69, 420, 1337, 80085]
    with self.assertRaises(TypeError):
      self.baseTypes.attrStr = {'lmao': True, }
      self.baseTypes.attrFloat = {'lmao': True, }
      self.baseTypes.attrInt = {'lmao': True, }
      self.baseTypes.attrBool = {'lmao': True, }
      self.baseTypes.attrList = {'lmao': True, }

  def test_deleters(self) -> None:
    """Testing that the fields in the 'BaseTypes' instance correctly
    raises 'TypeError' when attempting to delete as AttriBox does not
    implement deletion. """
    with self.assertRaises(TypeError):
      del self.baseTypes.attrStr
      del self.baseTypes.attrFloat
      del self.baseTypes.attrInt
      del self.baseTypes.attrBool
      del self.baseTypes.attrList
      del self.baseTypes.attrDict
