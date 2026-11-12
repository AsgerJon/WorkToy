"""
TestEZHookTakeover tests how a subclass of 'EZHook' from 'worktoy.ezdata'
takes the place of the hook a namespace inherits.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZHook, EZMeta, EZSpace
from worktoy.mcls import BaseSpace
from . import EzdataTest


class TestEZHookTakeover(EzdataTest):
  """
  A project building a dataclass base of its own declares a subclass of
  'EZHook' in the body of a subclass of 'EZSpace', at a name of its own,
  and that hook then acts alone: the hook the namespace inherits stands
  down. The tests pin the record of the acting hook, the stand-down of
  both phases, and a family whose hook takes one more spelling of
  'frozen', with its record of generated names, its '__match_args__' and
  its refusal to thaw.
  """

  @staticmethod
  def makeFamily() -> tuple:
    """A hook taking 'readOnly' for 'frozen', wired into a base."""

    class LabHook(EZHook):
      __frozen_keys__ = (*EZHook.__frozen_keys__, 'readOnly')

    class LabSpace(EZSpace):
      labHook = LabHook()

    class LabMeta(EZMeta):
      @classmethod
      def __prepare__(mcls, name: str, bases: tuple, **kw) -> EZSpace:
        return LabSpace(mcls, name, bases, **kw)

    class LabData(EZData, metaclass=LabMeta):
      """The base of the family."""

    return LabSpace, LabMeta, LabData

  def test_acting_hook_recorded(self) -> None:
    LabSpace, LabMeta, LabData = self.makeFamily()
    inherited = EZSpace.__dict__['ezHook']
    declared = LabSpace.__dict__['labHook']
    self.assertIs(EZSpace.__ez_acting_hook__, inherited)
    self.assertIs(LabSpace.__ez_acting_hook__, declared)
    self.assertIs(LabSpace.__dict__['__ez_acting_hook__'], declared)
    self.assertEqual(LabSpace.classGetHooks()[-2:], [inherited, declared])

    class Deeper(LabSpace):
      """Declares no hook and inherits the acting one."""

    self.assertIs(Deeper.__ez_acting_hook__, declared)
    self.assertNotIn('__ez_acting_hook__', Deeper.__dict__)

  def test_inherited_hook_stands_down(self) -> None:
    LabSpace, LabMeta, LabData = self.makeFamily()
    space = LabSpace(LabMeta, 'A', ())
    inherited = EZSpace.__dict__['ezHook'].__get__(space, LabSpace)
    self.assertTrue(inherited._standsDown())
    self.assertFalse(inherited.setItemPhase('x', 1))
    self.assertFalse(inherited.setItemPhase('__init__', len))
    self.assertEqual(space.getEZFields(), {})
    compiled = {'a': 1}
    self.assertIs(inherited.postCompilePhase(compiled), compiled)
    self.assertEqual(compiled, {'a': 1})
    declared = LabSpace.__dict__['labHook'].__get__(space, LabSpace)
    self.assertFalse(declared._standsDown())
    self.assertTrue(declared.setItemPhase('x', 1))
    self.assertEqual([*space.getEZFields()], ['x'])
    plain = EZSpace(EZMeta, 'B', ())
    own = EZSpace.__dict__['ezHook'].__get__(plain, EZSpace)
    self.assertFalse(own._standsDown())

  def test_extra_spelling(self) -> None:
    LabSpace, LabMeta, LabData = self.makeFamily()

    class Sample(LabData, readOnly=True):
      mass = 0.0

    self.assertTrue(Sample.isFrozen)
    with self.assertRaises(AttributeError) as context:
      Sample(2).mass = 3
    self.assertEqual(str(context.exception), "'Sample' is frozen; cannot "
                     "assign to attribute 'mass'!")
    self.assertEqual(hash(Sample(2)), hash((2.0,)))

    class Loose(EZData, readOnly=True):
      mass = 0.0

    self.assertFalse(Loose.isFrozen)
    for key in ('frozen', 'immutable', 'hashable'):
      with self.subTest(key=key):
        cls = LabMeta('F', (LabData,), {'x': 1}, **{key: True})
        self.assertTrue(cls.isFrozen)

  def test_generated_names_and_match_args(self) -> None:
    LabSpace, LabMeta, LabData = self.makeFamily()

    class Sample(LabData):
      mass = 0.0

    class Labelled(Sample):
      label = ''

    expected = frozenset((
      '__field_pairs__', 'asDict', 'asTuple', 'replace', '__repr__',
      '__str__', '__match_args__',
    ))
    self.assertEqual(LabData.__ez_generated__, expected)
    self.assertEqual(Sample.__ez_generated__, expected)
    self.assertEqual(Labelled.__ez_generated__, expected)
    self.assertEqual(Sample.__match_args__, ('mass',))
    self.assertEqual(Labelled.__match_args__, ('mass', 'label'))
    self.assertEqual(Labelled(1, 'a').asTuple(), (1.0, 'a'))

  def test_thawing_judged_by_the_acting_hook(self) -> None:
    LabSpace, LabMeta, LabData = self.makeFamily()

    class Sample(LabData, readOnly=True):
      mass = 0.0

    class Still(Sample, readOnly=True):
      label = ''

    self.assertTrue(Still.isFrozen)
    with self.assertRaises(TypeError) as context:
      class Thawed(Sample):
        """Based on a frozen class and not frozen itself."""

    self.assertIn("'Thawed' is based on the frozen class 'Sample' and "
                  "does not declare 'frozen=True' itself",
                  str(context.exception))

  def test_hook_registered_by_hand_acts(self) -> None:
    class Hand(BaseSpace):
      """A namespace no class body gave a hook."""

    hook = EZHook()
    Hand.addHook(hook)
    self.assertNotIn('__ez_acting_hook__', vars(Hand))
    bound = hook.__get__(Hand(EZMeta, 'A', ()), Hand)
    self.assertFalse(bound._standsDown())
