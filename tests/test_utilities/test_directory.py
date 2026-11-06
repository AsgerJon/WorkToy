"""
TestDirectory tests 'Directory' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from types import ModuleType

from worktoy.utilities import Directory
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import UtilitiesTest, DirOwner, Fallback


class TestDirectory(UtilitiesTest):
  """
  'Directory' gives a class the directory of its own source file, so a
  class can find resources beside itself. The tests pin that the read
  through an instance is the absolute directory of the file defining
  the class, that a read through the class gives the descriptor, that
  a class whose module has no file is refused with 'MissingVariable'
  naming the attribute, and that writes and deletions are refused.
  """

  def test_instance_read_is_source_directory(self) -> None:
    from . import _dir_owner
    expected = os.path.dirname(os.path.abspath(_dir_owner.__file__))
    self.assertEqual(DirOwner().here, expected)
    self.assertTrue(os.path.isabs(DirOwner().here))

  def test_class_read_is_descriptor(self) -> None:
    self.assertIsInstance(DirOwner.here, Directory)

  def test_module_without_file(self) -> None:
    sys.modules['fallback_module'] = ModuleType('fallback_module')
    self.addCleanup(sys.modules.pop, 'fallback_module', None)
    with self.assertRaises(MissingVariable) as context:
      _ = Fallback().here
    self.assertEqual(context.exception.varName, 'here')
    self.assertIsInstance(context.exception.instance, Fallback)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Fallback.here: str'", str(context.exception))
    self.assertIsInstance(context.exception.__cause__, AttributeError)

  def test_module_not_registered(self) -> None:
    sys.modules.pop('fallback_module', None)
    with self.assertRaises(MissingVariable) as context:
      _ = Fallback().here
    self.assertEqual(context.exception.varName, 'here')
    self.assertIsInstance(context.exception.instance, Fallback)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Fallback.here: str'", str(context.exception))

  def test_nameless_descriptor_reports_directory(self) -> None:
    #  A descriptor never bound by '__set_name__' has no field name and
    #  falls back to 'directory' in the refusal.
    sys.modules.pop('fallback_module', None)
    with self.assertRaises(MissingVariable) as context:
      Directory().__get__(Fallback(), Fallback)
    self.assertEqual(context.exception.varName, 'directory')
    self.assertIsInstance(context.exception.instance, Fallback)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Fallback.directory: str'", str(context.exception))

  def test_set_refused(self) -> None:
    owner = DirOwner()
    with self.assertRaises(ReadOnlyError) as context:
      owner.here = 'elsewhere'
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, DirOwner.here)
    self.assertEqual(context.exception.newVal, 'elsewhere')
    self.assertIn("'DirOwner.here'", str(context.exception))
    self.assertIn("'elsewhere'", str(context.exception))

  def test_delete_refused(self) -> None:
    owner = DirOwner()
    with self.assertRaises(ProtectedError) as context:
      del owner.here
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, DirOwner.here)
    self.assertIsNone(context.exception.oldVal)
    self.assertIn("'DirOwner.here'", str(context.exception))
