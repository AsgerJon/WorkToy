"""
TestAlias tests 'Alias' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Alias, AttriBox
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import DanglingAlias, NotADescriptor
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import DescTest, Geometry, Shrunk


class TestAlias(DescTest):
  """
  An 'Alias' is a second name for an attribute: the same value, the same
  hooks, following a subclass that redeclares the attribute, and usable
  for a method of any kind. The tests pin the three accesses through
  the alias, the subclass, the methods and the overloads a subclass
  adds, the refusals of writing or deleting a method, and the three
  mistakes refused as the class is created.
  """

  def test_reads_writes_deletes_the_real_name(self) -> None:
    geometry = Geometry()
    self.assertEqual(geometry.w, 240)
    geometry.w = 300
    self.assertEqual(geometry.width, 300)
    del geometry.w
    with self.assertRaises(MissingVariable) as context:
      _ = geometry.width
    self.assertEqual(context.exception.varName, 'width')
    self.assertIs(context.exception.instance, geometry)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Geometry.width: object'", str(context.exception))
    self.assertIsInstance(Geometry.w, Alias)
    self.assertEqual(Geometry.w.getPosArgs(), ('width',))

  def test_follows_subclass(self) -> None:
    self.assertEqual(Shrunk().w, 10)
    shrunk = Shrunk()
    shrunk.w = 11
    self.assertEqual(shrunk.width, 11)

  def test_methods_of_every_kind(self) -> None:
    geometry = Geometry()
    self.assertEqual(geometry.size(), 240 * 240)
    self.assertEqual(geometry.u(), 'px')
    self.assertEqual(geometry.k(), 'Geometry')
    self.assertEqual(Shrunk().k(), 'Shrunk')
    self.assertEqual(geometry.s(2), 480)
    self.assertEqual(geometry.s(0.5), 120.0)
    self.assertEqual(Shrunk().s('ab'), 'ab' * 10)
    self.assertEqual(Shrunk().s(3), 30)

  def test_method_alias_refuses_write_and_delete(self) -> None:
    geometry = Geometry()
    with self.assertRaises(ReadOnlyError) as context:
      geometry.size = 5
    self.assertIs(context.exception.desc, Geometry.size)
    self.assertIs(context.exception.instance, geometry)
    self.assertEqual(context.exception.newVal, 5)
    self.assertIn("'Geometry.size'", str(context.exception))
    with self.assertRaises(ProtectedError) as context:
      del geometry.u
    self.assertIs(context.exception.desc, Geometry.u)
    self.assertIs(context.exception.instance, geometry)
    self.assertIsNone(context.exception.oldVal)
    self.assertIn("'Geometry.u'", str(context.exception))
    self.assertEqual(geometry.size(), 240 * 240)

  def test_name_no_class_holds_refused(self) -> None:
    alias = Alias('nothing')
    with self.assertRaises(DanglingAlias) as context:
      alias.__set_name__(int, 'a')
    self.assertIs(context.exception.alias, alias)
    self.assertEqual(context.exception.realName, 'nothing')
    self.assertIs(context.exception.owner, int)
    self.assertIn("'int.a' stands for 'nothing'", str(context.exception))
    with self.assertRaises((DanglingAlias, RuntimeError)) as context:
      class Bad:
        a = Alias('nothing')
    exception = context.exception.__cause__ or context.exception
    self.assertIsInstance(exception.alias, Alias)
    self.assertEqual(exception.realName, 'nothing')
    self.assertEqual(exception.owner.__name__, 'Bad')
    self.assertIn("'Bad.a' stands for 'nothing'", str(exception))

  def test_own_name_refused(self) -> None:
    alias = Alias('a')

    class Holder:
      pass

    Holder.a = alias
    with self.assertRaises(DanglingAlias) as context:
      alias.__set_name__(Holder, 'a')
    self.assertEqual(context.exception.realName, 'a')
    self.assertIs(context.exception.alias, alias)
    self.assertIs(context.exception.owner, Holder)
    self.assertIn("'Holder.a' stands for 'a'", str(context.exception))

  def test_plain_value_refused(self) -> None:
    alias = Alias('v')

    class Holder:
      v = 1

    with self.assertRaises(NotADescriptor) as context:
      alias.__set_name__(Holder, 'a')
    self.assertIs(context.exception.alias, alias)
    self.assertEqual(context.exception.realName, 'v')
    self.assertEqual(context.exception.found, 1)
    self.assertIn("'Holder.a' stands for 'v', which holds 1 of type 'int'",
                  str(context.exception))
    with self.assertRaises((NotADescriptor, RuntimeError)) as context:
      class Bad:
        v = 1
        a = Alias('v')
    exception = context.exception.__cause__ or context.exception
    self.assertIsInstance(exception.alias, Alias)
    self.assertEqual(exception.realName, 'v')
    self.assertEqual(exception.found, 1)
    self.assertIn("'Bad.a' stands for 'v'", str(exception))

  def test_proxy_answering_get_is_no_descriptor(self) -> None:
    class Proxy:
      def __getattr__(self, key: str) -> object:
        return lambda *args: None

    class Holder:
      v = Proxy()

    self.assertTrue(callable(Holder.v.__get__))
    with self.assertRaises(NotADescriptor) as context:
      Alias('v').__set_name__(Holder, 'a')
    self.assertIsInstance(context.exception.alias, Alias)
    self.assertEqual(context.exception.realName, 'v')
    self.assertIs(context.exception.found, Holder.__dict__['v'])
    self.assertIn("of type 'Proxy'", str(context.exception))

  def test_constructor(self) -> None:
    with self.assertRaises(TypeException) as context:
      Alias(5)
    self.assertEqual(context.exception.varName, 'realName')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'realName'", str(context.exception))
    blank = Alias.__new__(Alias)
    with self.assertRaises(MissingVariable) as context:
      blank._getRealName()
    self.assertEqual(context.exception.varName, '__real_name__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(str(context.exception),
                     "Missing 'Alias.__real_name__: str'!")

  def test_plain_class_alias(self) -> None:
    class Plain:
      n = AttriBox[int](4)
      m = Alias('n')

    plain = Plain()
    self.assertEqual(plain.m, 4)
    plain.m = 6
    self.assertEqual(plain.n, 6)

  def test_random_writes_through_alias(self) -> None:
    geometry = Geometry()
    for value in self.randomInteger.row:
      geometry.w = value
      with self.subTest(value=value):
        self.assertEqual(geometry.width, value)
        self.assertEqual(geometry.size(), value * value)
