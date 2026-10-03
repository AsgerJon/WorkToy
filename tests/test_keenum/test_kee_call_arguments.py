"""
TestKeeCallArguments subclasses 'KeeTest' and pins that calling an
enumeration refuses arguments it has no use for. Calling a 'KeeNum'
class resolves one member from one identifier, so a second positional
argument or any keyword raises Python's own 'TypeError', and so does a
call without an identifier, whose message says that one is required.
Calling a 'KeeFlags' class combines its positional identifiers and
refuses keywords. Both used to drop what they had no use for without a
word, returning the member of the first identifier.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag

from . import KeeTest


class Color(KeeNum):
  """Color is a small value enumeration."""

  RED = Kee[int](10)
  BLUE = Kee[int](20)


class Perm(KeeFlags):
  """Perm is a small flags enumeration."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class TestKeeCallArguments(KeeTest):
  """
  TestKeeCallArguments provides tests for the arguments of a call to an
  enumeration.
  """

  def test_num_one_identifier(self) -> None:
    """A call with one identifier resolves the member."""
    self.assertIs(Color('RED'), Color.RED)
    self.assertIs(Color(20), Color.BLUE)

  def test_num_second_argument(self) -> None:
    """A second positional argument raises 'TypeError'."""
    with self.assertRaises(TypeError) as context:
      Color(10, 20)
    self.assertIs(type(context.exception), TypeError)
    self.assertIn('exactly one argument', str(context.exception))
    self.assertIn('2', str(context.exception))

  def test_num_keyword(self) -> None:
    """A keyword argument raises 'TypeError' naming it."""
    with self.assertRaises(TypeError) as context:
      Color('RED', x=1)
    self.assertIs(type(context.exception), TypeError)
    self.assertIn('keyword', str(context.exception))
    self.assertIn("'x'", str(context.exception))

  def test_num_no_identifier(self) -> None:
    """A call without an identifier raises 'TypeError' saying one is
    required."""
    with self.assertRaises(TypeError) as context:
      Color()
    self.assertIs(type(context.exception), TypeError)
    self.assertIn('exactly one argument', str(context.exception))
    self.assertIn('0', str(context.exception))

  def test_flags_keyword(self) -> None:
    """A keyword argument to a flags class raises 'TypeError', with or
    without positional identifiers."""
    with self.assertRaises(TypeError) as context:
      Perm('READ', bogus=2)
    self.assertIs(type(context.exception), TypeError)
    self.assertIn("'bogus'", str(context.exception))
    with self.assertRaises(TypeError):
      Perm(read=True)

  def test_flags_positional(self) -> None:
    """A flags class still combines several positional identifiers, and
    gives the empty member for none."""
    self.assertIs(Perm('READ', 'WRITE'), Perm.READ_WRITE)
    self.assertIs(Perm(), Perm.NULL)
