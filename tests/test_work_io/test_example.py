"""
TestPlayerScore tests the canonical 'PlayerScore' demonstration class,
exercising its overloaded constructors, JSON persistence via 'FidGen',
and dispatch behaviour on invalid signatures.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING
from unittest.mock import patch

from worktoy.waitaminute.dispatch import DispatchException
from . import WorkIOTest, PlayerScore

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestPlayerScore(WorkIOTest):
  """Tests for the canonical 'PlayerScore' demo class."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  __sample_rows__ = (
    ('Alice', 100, 1),
    ('Bob', 0, 0),
    ('Carol', 9999, 99),
    ('', 0, 0),
  )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    """Redirect PlayerScore's FidGen to the per-class temp directory."""
    super().setUp()
    PlayerScore.fidGen.fileDirectory = self.tempDir

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTOR TESTS    # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_default_construction(self) -> None:
    """Bare construction yields AttriBox defaults."""
    p = PlayerScore()
    self.assertEqual(p.name, '')
    self.assertEqual(p.score, 0)
    self.assertEqual(p.level, 0)

  def test_name_only_construction(self) -> None:
    """The 'str' overload leaves score and level at defaults."""
    for name in ('Alice', 'Bob', 'Carol'):
      with self.subTest(name=name):
        p = PlayerScore(name)
        self.assertEqual(p.name, name)
        self.assertEqual(p.score, 0)
        self.assertEqual(p.level, 0)

  def test_name_and_score_construction(self) -> None:
    """The '(str, int)' overload sets name and score, level defaults."""
    cases = (('Alice', 100), ('Bob', 0), ('Carol', 9999))
    for name, score in cases:
      with self.subTest(name=name, score=score):
        p = PlayerScore(name, score)
        self.assertEqual(p.name, name)
        self.assertEqual(p.score, score)
        self.assertEqual(p.level, 0)

  def test_full_construction(self) -> None:
    """Full '(str, int, int)' overload sets all three fields."""
    for name, score, level in self.__sample_rows__:
      with self.subTest(name=name, score=score, level=level):
        p = PlayerScore(name, score, level)
        self.assertEqual(p.name, name)
        self.assertEqual(p.score, score)
        self.assertEqual(p.level, level)

  def test_copy_construction(self) -> None:
    """Copy overload reproduces source instance fields."""
    for name, score, level in self.__sample_rows__:
      with self.subTest(name=name, score=score, level=level):
        original = PlayerScore(name, score, level)
        copy = PlayerScore(original)
        self.assertEqual(copy.name, original.name)
        self.assertEqual(copy.score, original.score)
        self.assertEqual(copy.level, original.level)

  def test_payload_construction(self) -> None:
    """Dict overload inflates from a JSON-style payload."""
    for name, score, level in self.__sample_rows__:
      payload = dict(name=name, score=score, level=level)
      with self.subTest(name=name, score=score, level=level):
        p = PlayerScore(payload)
        self.assertEqual(p.name, name)
        self.assertEqual(p.score, score)
        self.assertEqual(p.level, level)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PERSISTENCE TESTS    # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_save_returns_existing_path(self) -> None:
    """save() returns a path that exists on disk after the call."""
    p = PlayerScore('Alice', 100, 1)
    path = p.save()
    self.assertTrue(os.path.isfile(path))

  def test_save_writes_correct_payload(self) -> None:
    """save() writes a JSON payload matching the instance fields."""
    p = PlayerScore('Alice', 100, 1)
    path = p.save()
    f = None
    payload = None
    try:
      f = open(path, 'r')
    except Exception as exception:  # pragma: no cover
      raise exception
    else:
      payload = json.loads(f.read())
    finally:
      try:
        f.close()
      except AttributeError:  # pragma: no cover
        pass
    self.assertEqual(payload['name'], 'Alice')
    self.assertEqual(payload['score'], 100)
    self.assertEqual(payload['level'], 1)

  def test_save_allocates_distinct_paths(self) -> None:
    """Two successive saves write to two different files."""
    p1 = PlayerScore('Alice', 100, 1)
    p2 = PlayerScore('Bob', 50, 2)
    path1 = p1.save()
    path2 = p2.save()
    self.assertNotEqual(path1, path2)
    self.assertTrue(os.path.isfile(path1))
    self.assertTrue(os.path.isfile(path2))

  def test_save_propagates_open_failure(self) -> None:
    """save() re-raises when 'open' fails to acquire a handle."""
    p = PlayerScore('Alice', 100, 1)
    with patch('builtins.open', side_effect=OSError('disk full')):
      with self.assertRaises(OSError):
        p.save()

  def test_save_load_roundtrip(self) -> None:
    """save() followed by load() preserves all fields."""
    for name, score, level in self.__sample_rows__:
      with self.subTest(name=name, score=score, level=level):
        original = PlayerScore(name, score, level)
        path = original.save()
        restored = PlayerScore.load(path)
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.score, original.score)
        self.assertEqual(restored.level, original.level)

  def test_load_missing_file_raises(self) -> None:
    """load() raises when the path does not exist."""
    missing = os.path.join(self.tempDir, 'definitely_missing.json')
    with self.assertRaises(Exception):
      PlayerScore.load(missing)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DISPATCH TESTS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_dispatch_rejects_invalid_signatures(self) -> None:
    """Construction with unsupported arg types raises DispatchException."""
    invalidCases = (
      (123,),
      (None,),
      ('Alice', 'not_an_int'),
      ('Alice', 100, 'not_an_int'),
      (1.5,),
    )
    for args in invalidCases:
      with self.subTest(args=args):
        with self.assertRaises(DispatchException):
          PlayerScore(*args)
