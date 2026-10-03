"""
TestDirectoryWithoutFile subclasses 'UtilitiesTest' and pins how
'Directory' answers for a class without a source file, as in the REPL or
under 'exec', and how its refusals name the field. Such a class used to
make 'directory' raise a bare 'AttributeError' about the module, and the
refusals of a write or a deletion named the field 'object', since the
descriptor recorded no name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import Directory
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError

from . import UtilitiesTest


class TestDirectoryWithoutFile(UtilitiesTest):
  """
  TestDirectoryWithoutFile provides tests for 'Directory' on a class
  without a source file.
  """

  def test_no_file(self) -> None:
    """A class from 'exec' raises 'MissingVariable' naming the field."""
    space = {'Directory': Directory}
    exec('class Loose:\n  where = Directory()\n', space)
    loose = space['Loose']()
    with self.assertRaises(MissingVariable) as context:
      _ = loose.where
    self.assertEqual(context.exception.varName, 'where')
    self.assertIn('Loose.where', str(context.exception))

  def test_refusals_name_field(self) -> None:
    """A write and a deletion are refused naming the field."""

    class Located:
      where = Directory()

    located = Located()
    with self.assertRaises(ReadOnlyError) as context:
      located.where = 'elsewhere'
    self.assertIn('Located.where', str(context.exception))
    with self.assertRaises(ProtectedError) as context:
      del located.where
    self.assertIn('Located.where', str(context.exception))

  def test_with_file(self) -> None:
    """A class from a file still reads the directory of the file."""

    class Located:
      where = Directory()

    self.assertTrue(Located().where.endswith('test_utilities'))
