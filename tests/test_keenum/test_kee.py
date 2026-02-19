"""
TestKee tests the 'Kee' class. The addition of this dedicated test case
comes *after* reimplement 'Kee' as a subclass of 'AttriBox'. It is
sufficiently different from 'AttriBox' to not be covered by the same test
case as it. Further, 'Kee' now implements certain functionalities not used
by 'KeeNum' classes directly after class creation.

To avoid contrived or pedantic test coverage gymnastic as much as possible
the test case centers on the example class 'Ugedag' (weekday in Danish).
This class uses a custom class as the value type for the purpose of
testing the lazy instantiation.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from tests.test_keenum import KeeTest
from tests.test_keenum.examples import Ugedag, Dag, _MetaDag  # noqa
from worktoy.keenum import Kee, KeeNum
from worktoy.utilities import ExceptionInfo
from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.keenum import KeeNameConflict, KeeDuplicate

if TYPE_CHECKING:  # pragma: no cover
  pass

ic.configureOutput(includeContext=True)


class TestKee(KeeTest):
  """TestKee tests the 'Kee' class. The addition of this dedicated test case
  comes *after* reimplement 'Kee' as a subclass of 'AttriBox'. It is
  sufficiently different from 'AttriBox' to not be covered by the same test
  case as it. Further, 'Kee' now implements certain functionalities not used
  by 'KeeNum' classes directly after class creation.

  To avoid contrived or pedantic test coverage gymnastic as much as possible
  the test case centers on the example class 'Ugedag' (weekday in Danish).
  This class uses a custom class as the value type for the purpose of
  testing the lazy instantiation.
  """

  def tearDown(self) -> None:
    """
    Cleaning up after each test method.
    """
    super().tearDown()
    Dag.resetRegistry()

  def test_init(self, ) -> None:
    """
    Testing 'Ugedag' as a valid enumeration.
    """
    self.assertFalse((*(_ for _ in Dag),))
    for i, dag in enumerate(Ugedag):
      self.assertEqual(i, int(Dag))
      self.assertIn(dag.name, Ugedag)
      self.assertIsInstance(dag.value, Dag)
      self.assertEqual(i, dag.index)
    i = 0
    for i, _ in enumerate(Dag):
      pass
    else:
      self.assertTrue(i)

  def test_index_bad_get(self) -> None:
    """
    Testing exceptions raised when getting 'index'.
    """
    kee = Kee[str]('')
    with self.assertRaises(MissingVariable) as context:
      _ = kee.index
    e = context.exception
    self.assertEqual(e.varName, '__num_index__')
    self.assertIs(e.instance, kee)
    self.assertIs(e.type_, int)

    setattr(kee, '__num_index__', 'sixty-nine')
    with self.assertRaises(TypeException) as context:
      _ = kee.index
    e = context.exception
    self.assertEqual(e.varName, '__num_index__')
    self.assertIs(e.actualObject, getattr(kee, '__num_index__'))
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)

  def test_index_bad_set(self, ) -> None:
    """
    Testing exceptions raised when setting 'index'.
    """
    kee = Kee[str]('')
    with self.assertRaises(VariableNotNone) as context:
      kee.index = 69
      kee.index = 420
    e = context.exception
    self.assertEqual(e.name, 'index')
    self.assertIs(e.value, 69)

    kee = Kee[str]('')
    with self.assertRaises(TypeException) as context:
      kee.index = 'sixty-nine'
    e = context.exception
    self.assertEqual(e.varName, 'index')
    self.assertIs(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)

  def test_value_bad_get(self, ) -> None:
    """
    Testing exceptions raised when getting 'value'.
    """
    kee = Kee[str]('')
    with self.assertRaises(RecursionError):
      _ = kee.getValue(_recursion=True)
    setattr(kee, '__field_value__', 69)
    with self.assertRaises(TypeException) as context:
      _ = kee.getValue()
    e = context.exception
    self.assertEqual(e.varName, '__field_value__')
    self.assertIs(e.actualObject, getattr(kee, '__field_value__'))
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)

  def test_name_bad_type_get(self, ) -> None:
    """
    Testing exception when '__num_name__' is not 'None' and not 'str'.
    """
    kee = Kee[str]('')
    setattr(kee, '__num_name__', 69)
    with self.assertRaises(TypeException) as context:
      _ = kee.name
    e = context.exception
    self.assertEqual(e.varName, '__num_name__')
    self.assertEqual(e.actualObject, getattr(kee, '__num_name__'))
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)

  def test_good_int(self, ) -> None:
    """
    Testing that 'int' conversion works as expected.
    """
    for i, dag in enumerate(Ugedag):
      self.assertEqual(i, int(dag.kee))

  def test_kee_name_conflict(self) -> None:
    """
    Tests behaviour where a 'member' stored under one name has its
    internal name set to a different name.
    """

    class ABCD(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)
      C = Kee[int](3)
      D = Kee[int](4)
      E = Kee[int](5)

    with self.assertRaises(KeeNameConflict) as context:
      class L(ABCD):
        F = ABCD.A.kee  # Is present but at different name
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.member, ABCD.A.kee)
    self.assertEqual(e.oldName, 'A')
    self.assertEqual(e.newName, 'F')

  def test_inheritance_from_non_keenum(self, ) -> None:
    """
    Tests that inheriting from a non-'KeeNum' class raises the
    appropriate exception.
    """

    class Space:
      __member_type__ = int
      __overload_map__ = dict()
      __fallback_map__ = dict()
      __finalizer_map__ = dict()
      __compiled_space__ = dict()

    class Base:
      __namespace__ = Space()

    class ABCD(KeeNum, Base):
      A = Kee[int](1)
      B = Kee[int](2)
      C = Kee[int](3)
      D = Kee[int](4)

    for letter, member in zip('ABCD', ABCD):
      self.assertEqual(getattr(ABCD, letter), member)

  def test_kee_duplicate_in_bases(self, ) -> None:
    """
    Tests that having the same 'Kee' member in multiple base
    classes raises the appropriate exception.
    """

    class A(KeeNum):
      X = Kee[int](1)

    class B(KeeNum):
      X = Kee[int](1)

    with self.assertRaises(KeeDuplicate) as context:
      class C(A, B):
        """
        If it just says 'pass', then sometimes when the class fails to
        create, the 'pass' line will not be considered covered.
        """
    e = context.exception
    self.assertEqual(e.name, 'X')

  def test_dag_example(self) -> None:
    """
    Coverage gymnastics for the 'Dag' example used in 'Ugedag'.
    """
    with self.assertRaises(RecursionError):
      _ = Dag.getInstanceRegistry(_recursion=True)
    setattr(Dag, '__instance_registry__', 'sixty-nine')
    with self.assertRaises(TypeException):
      _ = Dag.getInstanceRegistry()
    setattr(Dag, '__instance_registry__', (69, 420, 1337, 80085))
    with self.assertRaises(TypeException):
      _ = Dag.getInstanceRegistry()
    Dag.resetRegistry()
    dag = Dag('Badedag')
    self.assertEqual(dag.name, 'Badedag')
    self.assertIn(dag, Dag)
    self.assertEqual(len(Dag), 1)
    Dag.registerInstance(dag)
    self.assertEqual(len(Dag), 1)
    self.assertNotIn(object(), Dag)
    self.assertEqual("""<Dag: name='Badedag'>""", str(dag))
    self.assertEqual(repr(dag), """Dag('Badedag')""")
    dage = {dag, }
    self.assertIn(dag, dage)
    self.assertEqual(hash(dag), hash(('Dag', 'Badedag',)))
    breh = Dag()
    with self.assertRaises(MissingVariable) as context:
      _ = breh.name
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, '__name_str__')
    self.assertIs(e.instance, breh)
    self.assertIs(e.type_, str)
    setattr(breh, '__name_str__', 69)
    with self.assertRaises(TypeException) as context:
      _ = breh.name
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, '__name_str__')
    self.assertIs(e.actualObject, getattr(breh, '__name_str__'))
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)

    class Foo(metaclass=_MetaDag):
      pass
