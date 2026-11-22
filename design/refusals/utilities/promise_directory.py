"""
RefusedDirectory holds the refusals that belong with
'design.promises.utilities.promise_directory'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import Directory
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class RefusedDirectory(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A class defined where no file stands behind it, under 'exec',
  raises 'MissingVariable' naming the attribute. Writing raises
  'ReadOnlyError' and deleting raises 'ProtectedError'. Source: the
  'Directory' docstring.
  """

  def test_no_source_file(self) -> None:
    namespace = dict()
    source = """from worktoy.utilities import Directory
class Nowhere:
  where = Directory()
"""
    exec(source, namespace)
    nowhere = namespace['Nowhere']()
    with self.assertRaises(Exception) as refused:
      _ = nowhere.where
    self.assertIsInstance(refused.exception, MissingVariable)

  def test_write_and_delete_refused_1(self) -> None:
    class Resource:
      home = Directory()

    resource = Resource()
    with self.assertRaises(Exception) as refused:
      resource.home = '/tmp'
    self.assertIsInstance(refused.exception, ReadOnlyError)

  def test_write_and_delete_refused_2(self) -> None:
    class Resource:
      home = Directory()

    resource = Resource()
    with self.assertRaises(Exception) as refused:
      del resource.home
    self.assertIsInstance(refused.exception, ProtectedError)
