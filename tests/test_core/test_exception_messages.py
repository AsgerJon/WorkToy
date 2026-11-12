"""
TestExceptionMessages renders the messages of the exceptions
'worktoy.core' raises and pins their slots.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core.control_flow import ControlSpace, MetaFlow, ControlFlow
from worktoy.core.sentinels import THIS
from worktoy.waitaminute import MissingVariable, VariableNotNone
from worktoy.waitaminute import DeprecatedPromise
from worktoy.waitaminute import control_flow as flowErrors
from worktoy.waitaminute.desc import RecursiveRead, WithoutException
from worktoy.waitaminute.meta import ControlClassError, DuplicateSentinel
from worktoy.waitaminute.meta import IllegalInstantiation
from . import CoreTest


class TestExceptionMessages(CoreTest):
  """
  An exception the package raises carries a message naming what went
  wrong, and slots holding what it was given, and both are what a
  reader looks for. 'waitaminute' has no tests of its own: each raising
  package renders the messages of the exceptions it raises. The tests
  pin the names each message carries, the branches the rendering
  takes, every slot of each exception, and the moved names of
  'waitaminute.control_flow'.
  """

  def test_missing_variable(self) -> None:
    class Owner:
      """A class whose attribute is missing."""

    owner = Owner()
    bare = MissingVariable(owner, 'x')
    self.assertIs(bare.instance, owner)
    self.assertEqual(bare.varName, 'x')
    self.assertEqual(bare.expectedTypes, ())
    self.assertEqual(str(bare), "Missing 'Owner.x'!")
    one = MissingVariable(Owner, 'x', int)
    self.assertIs(one.instance, Owner)
    self.assertEqual(one.expectedTypes, (int,))
    self.assertEqual(str(one), "Missing 'Owner.x: int'!")
    several = MissingVariable(owner, 'x', int, str)
    self.assertEqual(several.expectedTypes, (int, str))
    self.assertEqual(str(several), "Missing 'Owner.x: Union[int, str]'!")
    self.assertEqual(repr(several), str(several))

  def test_variable_not_none(self) -> None:
    exception = VariableNotNone('x', 5)
    self.assertEqual(exception.name, 'x')
    self.assertEqual(exception.value, 5)
    self.assertIn("'x'", str(exception))
    self.assertIn('5', str(exception))
    self.assertEqual(repr(exception), str(exception))

  def test_recursive_read(self) -> None:
    class Owner:
      d = Object()

    owner = Owner()
    desc = Owner.__dict__['d']
    onGet = RecursiveRead(desc, owner, 'onGet')
    self.assertIs(onGet.desc, desc)
    self.assertIs(onGet.instance, owner)
    self.assertEqual(onGet.phase, 'onGet')
    self.assertIn('Owner.d', str(onGet))
    self.assertIn("'onGet'", str(onGet))
    self.assertIn('second argument', str(onGet))
    preGet = RecursiveRead(desc, owner, 'preGet')
    self.assertEqual(preGet.phase, 'preGet')
    self.assertIn("'preGet'", str(preGet))
    self.assertIn('before the value is read', str(preGet))
    self.assertEqual(repr(preGet), str(preGet))

  def test_without_exception(self) -> None:
    class Owner:
      d = Object()

    placed = WithoutException(Owner.__dict__['d'])
    self.assertIs(placed.desc, Owner.__dict__['d'])
    self.assertIn('Owner', str(placed))
    self.assertIn('d', str(placed))
    desc = Object()
    loose = WithoutException(desc)
    self.assertIs(loose.desc, desc)
    self.assertIn('NO-OWNER', str(loose))
    self.assertIn('NO-FIELD', str(loose))
    self.assertEqual(repr(loose), str(loose))
    expected = "Context-less call detected for descriptor at 'Owner.d'!"
    self.assertEqual(str(placed), expected)
    #  The text passes through 'textFmt', as every message does: a run
    #  of spaces in a quoted name comes out as one.
    gapped = type('Wide  Gap', (), dict(d=Object()))
    wide = WithoutException(gapped.__dict__['d'])
    expected = "Context-less call detected for descriptor at 'Wide Gap.d'!"
    self.assertEqual(str(wide), expected)

  def test_control_class_error(self) -> None:
    space = ControlSpace(MetaFlow, 'Sig', (ControlFlow,))
    with self.assertRaises(ControlClassError) as context:
      space['method'] = 1
    exception = context.exception
    self.assertIs(exception.space, space)
    self.assertEqual(exception.badKey, 'method')
    text = str(exception)
    self.assertIn("'Sig'", text)
    self.assertIn("'method'", text)
    self.assertIn(MetaFlow.getRootClass().__name__, text)
    self.assertIn('docstring', text)
    self.assertEqual(repr(exception), text)

  def test_duplicate_sentinel(self) -> None:
    bare = DuplicateSentinel('THIS', THIS)
    self.assertEqual(bare.sentinelName, 'THIS')
    self.assertIs(bare.existing, THIS)
    self.assertIsNone(bare.module)
    self.assertIn("'THIS'", str(bare))
    self.assertIn(THIS.__module__, str(bare))
    self.assertIn('a class statement', str(bare))
    placed = DuplicateSentinel('THIS', THIS, 'tests.somewhere')
    self.assertEqual(placed.module, 'tests.somewhere')
    self.assertIn("the class statement in 'tests.somewhere'", str(placed))
    self.assertEqual(repr(placed), str(placed))

  def test_illegal_instantiation(self) -> None:
    exception = IllegalInstantiation(THIS)
    self.assertIs(exception.cls, THIS)
    self.assertIn("'THIS'", str(exception))
    self.assertEqual(repr(exception), str(exception))

  def test_moved_names_of_control_flow_errors(self) -> None:
    with self.assertWarns(DeprecatedPromise):
      self.assertIs(flowErrors.ControlClassError, ControlClassError)
    with self.assertWarns(DeprecatedPromise):
      self.assertIs(flowErrors.ControlSpace, ControlSpace)
    with self.assertWarns(DeprecatedPromise):
      self.assertIs(flowErrors.MetaFlow, MetaFlow)
    with self.assertRaises(AttributeError) as context:
      _ = flowErrors.nothing
    text = str(context.exception)
    self.assertIn("'worktoy.waitaminute.control_flow'", text)
    self.assertIn("'nothing'", text)

  def test_random_names(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      instance = object()
      exception = MissingVariable(instance, word)
      with self.subTest(word=word):
        self.assertIs(exception.instance, instance)
        self.assertEqual(exception.varName, word)
        self.assertEqual(exception.expectedTypes, ())
        self.assertEqual(str(exception), "Missing 'object.%s'!" % word)
