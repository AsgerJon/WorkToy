"""
TestManualStamp tests how the release tooling keeps the copy of the
README at the top of 'design/manual.md' up to date.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os

import manual_stamp
import token_stamp
import version_stamp

from . import ReleaseToolingTest


class TestManualStamp(ReleaseToolingTest):
  """
  'design/manual.md' begins with 'README.md', word for word, and goes on
  from the line '# The Manual'. Whenever a release changes the README,
  its heading or its token badge, the copy must follow, and what comes
  after the copy must stay as it was. A manual without the line that ends
  the copy must be refused, since nothing would say where the copy
  stops.
  """

  REST = '# The Manual\n\nThe rest.\n'

  def setUp(self) -> None:
    ReleaseToolingTest.setUp(self)
    self.readmePath = os.path.join(self.root, 'README.md')
    self.manualPath = os.path.join(self.root, 'design', 'manual.md')
    os.makedirs(os.path.dirname(self.manualPath), exist_ok=True)
    badge = '%s old badge' % token_stamp.TOKENS_PREFIX
    readme = '%s\n\n# worktoy v9.9.9\n\nNew.\n' % badge
    self.writeText(self.readmePath, readme)
    manual = '# worktoy v1.0.0\n\nOld.\n\n' + self.REST
    self.writeText(self.manualPath, manual)

  def test_copy_follows_the_readme(self) -> None:
    manual_stamp.stampManual(self.root)
    expected = self.readText(self.readmePath) + '\n' + self.REST
    self.assertEqual(self.readText(self.manualPath), expected)

  def test_unchanged_readme_changes_nothing(self) -> None:
    manual_stamp.stampManual(self.root)
    once = self.readText(self.manualPath)
    manual_stamp.stampManual(self.root)
    self.assertEqual(self.readText(self.manualPath), once)

  def test_manual_without_the_line_refused(self) -> None:
    self.writeText(self.manualPath, '# worktoy v1.0.0\n\nNo such line.\n')
    with self.assertRaises(RuntimeError) as context:
      manual_stamp.stampManual(self.root)
    infoSpec = "Found no line '# The Manual' in file: '%s'!"
    expected = infoSpec % self.manualPath
    self.assertEqual(str(context.exception), expected)
    self.assertEqual(self.readText(self.manualPath),
                     '# worktoy v1.0.0\n\nNo such line.\n')

  def test_version_stamp_refreshes_the_copy(self) -> None:
    packagePath = os.path.join(self.root, 'src', 'worktoy', '__init__.py')
    os.makedirs(os.path.dirname(packagePath), exist_ok=True)
    self.writeText(packagePath, "__version__ = '0'\n")
    self.writeText(os.path.join(self.root, 'pyproject.toml'),
                   'version = "0"\n')
    held = version_stamp._root
    version_stamp._root = lambda: self.root
    try:
      version_stamp._stampAll('9.9.10-dev1')
    finally:
      version_stamp._root = held
    readme = self.readText(self.readmePath)
    self.assertIn('# worktoy v9.9.10-dev1 (development build)', readme)
    self.assertEqual(self.readText(self.manualPath),
                     readme + '\n' + self.REST)

  def test_token_stamp_refreshes_the_copy(self) -> None:
    held = token_stamp._root
    token_stamp._root = lambda: self.root
    try:
      token_stamp._stampBadge('1.5B')
    finally:
      token_stamp._root = held
    readme = self.readText(self.readmePath)
    self.assertIn('1.5B', readme)
    self.assertNotIn('old badge', readme)
    self.assertEqual(self.readText(self.manualPath),
                     readme + '\n' + self.REST)
