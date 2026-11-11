"""
TestWorkToyWarning tests 'WorkToyWarning' from 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import warnings
from types import ModuleType
from unittest.mock import patch

import worktoy
from worktoy.desc import AttriBox
from worktoy.utilities import textFmt
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import WorkToyWarning, RiskWarning, TypeException
from . import WaitaminuteTest, Till, ShopRisk, ring

HERE = sys._getframe().f_code.co_filename
#  The name of this folder as a package: 'tests.test_waitaminute' under
#  pytest, 'test_waitaminute' when 'unittest' discovers from 'tests'.
HOME = __name__.rsplit('.', 1)[0]
SHOP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_shop')


class TestWorkToyWarning(WaitaminuteTest):
  """
  'WorkToyWarning' is the common base of the warnings of worktoy and
  the one place a warning is given: its 'warn' method finds the nearest
  line that is no line of the library, nor of a project whose warning
  class it is, and gives the warning there, through the filters of the
  'warnings' package. The tests pin the base and its slots, the line a
  warning lands on from a test, from a project built upon worktoy, from
  text run by 'exec' and from the bottom of the stack, the filters
  (once per line, raised as an error, ignored by the base), what
  'warn' hands to 'warnings.warn_explicit', the packages stepped over,
  and the name each kind of thing is given.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(WorkToyWarning.__bases__, (Warning,))
    self.assertEqual(WorkToyWarning.__slots__, ())

  def test_lands_on_the_calling_line(self) -> None:
    warning = RiskWarning('price', -5, 'a loss')
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      line = sys._getframe().f_lineno + 1
      warning.warn()
    self.assertEqual(len(log), 1)
    self.assertIs(log[0].message, warning)
    self.assertIs(log[0].category, RiskWarning)
    self.assertEqual(log[0].filename, HERE)
    self.assertEqual(log[0].lineno, line)

  def test_steps_over_a_project_built_upon_worktoy(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      line = sys._getframe().f_lineno + 1
      self.assertEqual(ring(-5), 'sold')
    self.assertEqual(len(log), 1)
    self.assertIsInstance(log[0].message, ShopRisk)
    self.assertEqual(log[0].message.actualObject, -5)
    self.assertEqual(log[0].filename, HERE)
    self.assertEqual(log[0].lineno, line)

  def test_bottom_of_the_stack(self) -> None:
    space = dict(_isInternal=classmethod(lambda cls, frame: True))
    Deep = type('Deep', (RiskWarning,), space)
    bottom = sys._getframe()
    while bottom.f_back is not None:
      bottom = bottom.f_back
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      Deep('price', -5, 'a loss').warn()
    self.assertEqual(len(log), 1)
    self.assertEqual(log[0].filename, bottom.f_code.co_filename)
    self.assertEqual(log[0].lineno, bottom.f_lineno)

  def test_once_per_line(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('default')
      for _ in range(3):
        RiskWarning('price', -5, 'a loss').warn()
    self.assertEqual(len(log), 1)

  def test_raised_as_an_error(self) -> None:
    warning = RiskWarning('price', -5, 'a loss')
    with warnings.catch_warnings():
      warnings.simplefilter('error')
      with self.assertRaises(RiskWarning) as context:
        warning.warn()
    self.assertIs(context.exception, warning)

  def test_ignored_by_the_base(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      warnings.simplefilter('ignore', WorkToyWarning)
      RiskWarning('price', -5, 'a loss').warn()
    self.assertEqual(log, [])

  def test_handed_to_warn_explicit(self) -> None:
    warning = RiskWarning('price', -5, 'a loss')
    with patch('warnings.warn_explicit') as explicit:
      line = sys._getframe().f_lineno + 1
      warning.warn()
    space = globals()
    explicit.assert_called_once_with(warning, RiskWarning, HERE, line,
      __name__, space['__warningregistry__'], space)

  def test_text_run_by_exec(self) -> None:
    warning = RiskWarning('price', -5, 'a loss')
    code = compile('warning.warn()', 'till.txt', 'exec')
    #  No registry and no name in the globals of the text.
    bare = dict(warning=warning)
    with patch('warnings.warn_explicit') as explicit:
      exec(code, bare)
    self.assertEqual(bare['__warningregistry__'], dict())
    explicit.assert_called_once_with(warning, RiskWarning, 'till.txt', 1,
      '<string>', bare['__warningregistry__'], bare)
    #  A registry already there is the one used.
    registry = dict()
    kept = dict(warning=warning, __warningregistry__=registry)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('default')
      exec(code, kept)
    self.assertEqual(len(log), 1)
    self.assertEqual(log[0].filename, 'till.txt')
    self.assertIs(kept['__warningregistry__'], registry)
    self.assertTrue(registry)

  def test_packages_stepped_over(self) -> None:
    home = os.path.dirname(os.path.abspath(worktoy.__file__)) + os.sep
    self.assertEqual(WorkToyWarning._roots(), (home,))
    self.assertEqual(RiskWarning._roots(), (home,))
    self.assertEqual(ShopRisk._roots(), (SHOP + os.sep, home))
    #  A class at home in a lone file adds nothing.
    sys.modules['worktoy_lone'] = ModuleType('worktoy_lone')
    self.addCleanup(sys.modules.pop, 'worktoy_lone')
    space = dict(__module__='worktoy_lone.till', __slots__=())
    Lone = type('Lone', (RiskWarning,), space)
    self.assertEqual(Lone._roots(), (home,))
    #  Neither does a class whose home was never imported.
    space = dict(__module__='worktoy_nowhere', __slots__=())
    Nowhere = type('Nowhere', (RiskWarning,), space)
    self.assertEqual(Nowhere._roots(), (home,))
    #  A base that is no warning of the family, listed first, is passed
    #  over and the bases after it still count.
    space = dict(__module__='worktoy_nowhere')
    Foreign = type('Foreign', (RuntimeWarning,), space)
    Mixed = type('Mixed', (Foreign, RiskWarning), space)
    self.assertEqual(Mixed._roots(), (home,))

  def test_internal_frames(self) -> None:
    def frameOf(fileName: str) -> object:
      space = dict()
      code = 'import sys\nframe = sys._getframe()'
      exec(compile(code, fileName, 'exec'), space)
      return space['frame']

    home = os.path.dirname(os.path.abspath(worktoy.__file__))
    inside = os.path.join(home, 'keenum', '_kee_box.py')
    self.assertIs(RiskWarning._isInternal(frameOf(inside)), True)
    self.assertIs(RiskWarning._isInternal(frameOf(HERE)), False)
    #  The folder beside the package is not the package.
    beside = frameOf(home + '_shop.py')
    self.assertIs(RiskWarning._isInternal(beside), False)
    frozen = '<frozen importlib._bootstrap>'
    self.assertIs(RiskWarning._isInternal(frameOf(frozen)), True)
    shop = os.path.join(SHOP, '_ring.py')
    self.assertIs(RiskWarning._isInternal(frameOf(shop)), False)
    self.assertIs(ShopRisk._isInternal(frameOf(shop)), True)

  def test_names(self) -> None:
    nameOf = WorkToyWarning._nameOf
    self.assertEqual(nameOf('shop.Till.ring'), 'shop.Till.ring')
    #  The private file a class lives in is left out.
    self.assertEqual(TypeException.__module__,
      'worktoy.waitaminute._type_exception')
    self.assertEqual(nameOf(TypeException),
      'worktoy.waitaminute.TypeException')
    self.assertEqual(nameOf(textFmt), 'worktoy.utilities.textFmt')
    self.assertEqual(nameOf(Arrangement.applyTo),
      'worktoy.utilities.combinatorics.Arrangement.applyTo')
    self.assertEqual(nameOf(Till.recount), '%s.Till.recount' % HOME)
    self.assertEqual(Till().recount(), 0)
    #  A placed descriptor is named after its owner and its field.
    self.assertEqual(nameOf(Till.cash), '%s.Till.cash' % HOME)
    #  Anything else is shown as it shows itself.
    self.assertEqual(nameOf(3), '3')
    self.assertEqual(nameOf(str.join), repr(str.join))
    unplaced = AttriBox[int](0)
    self.assertEqual(nameOf(unplaced), repr(unplaced))
    #  The question is asked of a warning as of its class.
    warning = RiskWarning('price', -5, 'a loss')
    self.assertIs(warning._isPlaced(Till.cash), True)
    self.assertIs(warning._isPlaced(unplaced), False)
    OwnerOnly = type('OwnerOnly', (), dict(__field_owner__=Till))
    ownerOnly = OwnerOnly()
    self.assertEqual(nameOf(ownerOnly), repr(ownerOnly))
    NameOnly = type('NameOnly', (), dict(__field_name__='cash'))
    nameOnly = NameOnly()
    self.assertEqual(nameOf(nameOnly), repr(nameOnly))
