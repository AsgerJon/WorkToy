"""
TestWorkToyException subclasses 'WaitAMinuteTest' and pins that every
exception of 'worktoy.waitaminute' is a 'WorkToyException' and survives
'pickle' and 'copy': the common base captures the constructor call and
rebuilds the exception from it, whatever the builtin it is based on.
Every exception used to hand its base no arguments, so unpickling called
the class with nothing and an exception raised in a process-pool worker
broke the pool. An argument that cannot be pickled travels as a
'Detached' stand-in, so the rebuilt exception keeps its type and renders
its message, where a copy keeps the argument itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle
import pkgutil
import importlib

from worktoy import waitaminute
from worktoy.core.sentinels import THIS
from worktoy.waitaminute import WorkToyException, Detached
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.core.control_flow import ControlFlow, SkipSet
from worktoy.waitaminute.desc import ReadOnlyError, DescriptorException
from worktoy.waitaminute.meta import ClaimedName, DuplicateSentinel

from . import WaitAMinuteTest


def _roundTrip(exception: BaseException) -> BaseException:
  return pickle.loads(pickle.dumps(exception))


def _exceptionClasses() -> list:
  """Every exception class defined in a module of 'worktoy.waitaminute'
  outside the control-flow package."""
  out = []
  prefix = waitaminute.__name__ + '.'
  for info in pkgutil.walk_packages(waitaminute.__path__, prefix):
    if '.control_flow' in info.name:
      continue
    module = importlib.import_module(info.name)
    for value in vars(module).values():
      if not isinstance(value, type):
        continue
      if not issubclass(value, BaseException):
        continue
      if value.__module__ != module.__name__:
        continue
      if value not in out:
        out.append(value)
  return out


class TestWorkToyException(WaitAMinuteTest):
  """
  TestWorkToyException provides tests for the common exception base.
  """

  def test_every_exception_joins(self) -> None:
    """Every exception of the package, the control-flow signals aside,
    is a 'WorkToyException' and keeps the builtin it is based on."""
    classes = _exceptionClasses()
    self.assertGreater(len(classes), 40)
    for cls in classes:
      with self.subTest(cls=cls.__name__):
        self.assertTrue(issubclass(cls, WorkToyException))
        self.assertTrue(issubclass(cls, Exception))
    self.assertFalse(issubclass(ControlFlow, WorkToyException))
    self.assertFalse(issubclass(SkipSet, WorkToyException))
    self.assertTrue(issubclass(DescriptorException, WorkToyException))

  def test_type_error_family(self) -> None:
    """A 'TypeException' round-trips with every slot, is still a
    'TypeError', and renders the same message."""
    original = TypeException('n', 1, int, str)
    rebuilt = _roundTrip(original)
    self.assertIsInstance(rebuilt, TypeException)
    self.assertIsInstance(rebuilt, TypeError)
    self.assertEqual(rebuilt.varName, 'n')
    self.assertEqual(rebuilt.actualObject, 1)
    self.assertIs(rebuilt.actualType, int)
    self.assertEqual(rebuilt.expectedTypes, (int, str))
    self.assertEqual(str(rebuilt), str(original))

  def test_attribute_error_family(self) -> None:
    """'MissingVariable' and 'ReadOnlyError' round-trip and are still
    'AttributeError's, so 'hasattr' semantics survive a process
    boundary."""
    missing = _roundTrip(MissingVariable(3, 'v', int))
    self.assertIsInstance(missing, AttributeError)
    self.assertEqual(missing.varName, 'v')
    self.assertEqual(missing.expectedTypes, (int,))
    readOnly = _roundTrip(ReadOnlyError(3, 'desc', 4))
    self.assertIsInstance(readOnly, DescriptorException)
    self.assertIsInstance(readOnly, AttributeError)
    self.assertEqual((readOnly.instance, readOnly.newVal), (3, 4))

  def test_syntax_error_family(self) -> None:
    """A class-body refusal based on 'SyntaxError' round-trips with its
    slots and its 'msg', which the base's own argument parsing used to
    make impossible."""
    rebuilt = _roundTrip(ClaimedName('Foo', 'x'))
    self.assertIsInstance(rebuilt, SyntaxError)
    self.assertEqual(rebuilt.className, 'Foo')
    self.assertEqual(rebuilt.keyName, 'x')
    self.assertEqual(rebuilt.msg, str(rebuilt))
    self.assertIn("'Foo'", str(rebuilt))

  def test_class_argument(self) -> None:
    """A class among the arguments travels by reference and comes back
    as the same object."""
    rebuilt = _roundTrip(DuplicateSentinel('THIS', THIS, 'elsewhere'))
    self.assertIs(rebuilt.existing, THIS)
    self.assertEqual(rebuilt.module, 'elsewhere')

  def test_caught_by_builtin_after_round_trip(self) -> None:
    """The rebuilt exception is caught by the builtin it is based on."""
    with self.assertRaises(TypeError):
      raise _roundTrip(TypeException('n', 1, int))

  def test_detached_argument(self) -> None:
    """An argument that cannot be pickled travels as a 'Detached'
    stand-in: the type is kept and the message still renders."""
    original = TypeException('f', lambda: 0, int)
    rebuilt = _roundTrip(original)
    self.assertIsInstance(rebuilt, TypeException)
    self.assertIsInstance(rebuilt.actualObject, Detached)
    self.assertEqual(rebuilt.actualObject.typeName, 'function')
    self.assertIn('<lambda>', rebuilt.actualObject.text)
    self.assertIn("'f'", str(rebuilt))
    self.assertEqual(rebuilt.varName, 'f')

  def test_detached_answers_attributes(self) -> None:
    """A stand-in answers any plain attribute with itself, so a message
    that reads through the argument renders rather than raises, while a
    dunder is refused, so the protocols of 'pickle' and 'copy' do not
    mistake it for an object implementing them."""
    stub = Detached(lambda: 0)
    self.assertIs(stub.fieldName, stub)
    self.assertIs(stub.anything.deeper, stub)
    with self.assertRaises(AttributeError):
      _ = stub.__deepcopy__
    self.assertIn('detached', str(stub))
    self.assertIn('function', str(stub))
    self.assertEqual(str(stub), repr(stub))

  def test_detached_travels(self) -> None:
    """A stand-in itself pickles and copies, keeping its two parts."""
    stub = Detached(lambda: 0)
    for rebuilt in (_roundTrip(stub), copy.copy(stub), copy.deepcopy(stub)):
      self.assertIsInstance(rebuilt, Detached)
      self.assertEqual(rebuilt.typeName, 'function')
      self.assertEqual(rebuilt.text, stub.text)

  def test_copy_keeps_arguments(self) -> None:
    """'copy.copy' and 'copy.deepcopy' rebuild in process, so an
    argument that cannot be pickled is kept as it is."""
    func = lambda: 0  # noqa: E731
    original = TypeException('f', func, int)
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    self.assertIsNot(shallow, original)
    self.assertIs(shallow.actualObject, func)
    self.assertIs(deep.actualObject, func)
    self.assertEqual(deep.expectedTypes, (int,))
    self.assertIsInstance(copy.copy(ClaimedName('A', 'b')), SyntaxError)

  def test_captured_call(self) -> None:
    """The base records the constructor call as it was made."""
    exception = TypeException('n', 1, int)
    self.assertEqual(exception.__init_args__, ('n', 1, int))
    self.assertEqual(exception.__init_kwargs__, {})
