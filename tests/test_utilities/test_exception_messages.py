"""
TestExceptionMessages renders the messages of the exceptions
'worktoy.utilities' raises and pins their slots.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.waitaminute import TypeException, UnpackException
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError
from . import UtilitiesTest


class TestExceptionMessages(UtilitiesTest):
  """
  An exception the package raises carries a message naming what went
  wrong, and slots holding what it was given, and both are what a
  reader looks for. 'waitaminute' has no tests of its own: each raising
  package renders the messages of the exceptions it raises. The tests
  pin the names each message carries, the branches the rendering
  takes, and every slot of each exception.
  """

  def test_type_exception(self) -> None:
    short = TypeException('count', 'seven', int, float)
    self.assertEqual(short.varName, 'count')
    self.assertEqual(short.actualObject, 'seven')
    self.assertIs(short.actualType, str)
    self.assertEqual(short.expectedTypes, (int, float))
    text = str(short)
    self.assertIn("'count'", text)
    self.assertIn("'int' or 'float'", text)
    self.assertIn("'seven'", text)
    self.assertIn("'str'", text)
    self.assertNotIn('...', text)
    self.assertEqual(repr(short), text)
    value = 'x' * 60
    long = TypeException('count', value, int)
    self.assertIs(long.actualObject, value)
    self.assertEqual(long.expectedTypes, (int,))
    text = str(long)
    self.assertIn('...', text)
    self.assertNotIn('x' * 50, text)
    self.assertIn("'int'", text)

  def test_unpack_exception(self) -> None:
    exception = UnpackException(1, 'two', None)
    text = str(exception)
    self.assertEqual(exception.posArgs, (1, 'two', None))
    for part in ('1', 'two', 'None'):
      with self.subTest(part=part):
        self.assertIn(part, text)
    self.assertEqual(repr(exception), text)

  def test_descriptor_messages(self) -> None:
    class Owner:
      d = Object()

    owner = Owner()
    desc = Owner.__dict__['d']
    protected = ProtectedError(owner, desc, 'old')
    self.assertIs(protected.instance, owner)
    self.assertIs(protected.desc, desc)
    self.assertEqual(protected.oldVal, 'old')
    self.assertIn("'Owner.d'", str(protected))
    self.assertIn("'old'", str(protected))
    readOnly = ReadOnlyError(owner, desc, 'new')
    self.assertIs(readOnly.instance, owner)
    self.assertIs(readOnly.desc, desc)
    self.assertEqual(readOnly.newVal, 'new')
    self.assertIn('Owner.d', str(readOnly))
    self.assertIn('new', str(readOnly))
    self.assertEqual(repr(readOnly), str(readOnly))

  def test_random_names(self) -> None:
    self.randomWord.size = 5
    for word in self.randomWord.row:
      exception = TypeException(word, 0, str)
      with self.subTest(word=word):
        self.assertEqual(exception.varName, word)
        self.assertEqual(exception.actualObject, 0)
        self.assertIs(exception.actualType, int)
        self.assertEqual(exception.expectedTypes, (str,))
        self.assertIn("'%s'" % word, str(exception))
