"""
PromiseDirectory promises 'Directory' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.utilities import Directory
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class PromiseDirectory(TestCase):
  """
  'Directory()' is a read-only attribute giving the absolute directory
  of the file that defines the class of the instance, so a class finds
  the resources beside its own source. A class defined where no file
  stands behind it, under 'exec', raises 'MissingVariable' naming the
  attribute. Writing raises 'ReadOnlyError' and deleting raises
  'ProtectedError'. Source: the 'Directory' docstring.
  """

  def test_directory_of_source(self) -> None:
    class Resource:
      home = Directory()

    here = os.path.dirname(os.path.abspath(__file__))
    self.assertEqual(Resource().home, here)

  def test_no_source_file(self) -> None:
    namespace = dict()
    source = """from worktoy.utilities import Directory
class Nowhere:
  where = Directory()
"""
    exec(source, namespace)
    nowhere = namespace['Nowhere']()
    with self.assertRaises(MissingVariable) as context:
      _ = nowhere.where
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, nowhere)
    self.assertEqual(e.varName, 'where')
    self.assertEqual(e.expectedTypes, (str,))

  def test_write_and_delete_refused(self) -> None:
    class Resource:
      home = Directory()

    resource = Resource()
    with self.assertRaises(ReadOnlyError) as context:
      resource.home = '/tmp'
    self.assertIs(context.exception.instance, resource)
    self.assertIs(context.exception.desc, vars(Resource)['home'])
    self.assertEqual(context.exception.newVal, '/tmp')
    with self.assertRaises(ProtectedError) as context:
      del resource.home
    self.assertIs(context.exception.instance, resource)
    self.assertIs(context.exception.desc, vars(Resource)['home'])
    #  'oldVal' holds the value only "if known".
    self.assertIn(context.exception.oldVal, (None, resource.home))
