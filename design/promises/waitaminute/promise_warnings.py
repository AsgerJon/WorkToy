"""
PromiseWarnings promises the warnings of 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import types
import warnings
from typing import TYPE_CHECKING
from unittest import TestCase

from worktoy.utilities import textFmt, joinWords, wordWrap, stringList
from worktoy.utilities import unpack, resolveMRO
from worktoy.waitaminute import WorkToyWarning, DeprecatedPromise
from worktoy.waitaminute import RiskWarning, AlternativeWarning
from worktoy.waitaminute import RedundantKeyword

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Callable

#  Each warning with the builtin category it keeps.
FAMILY = {
  DeprecatedPromise: FutureWarning,
  RedundantKeyword: UserWarning,
  RiskWarning: RuntimeWarning,
  AlternativeWarning: UserWarning,
}

#  A project package, made up for 'test_project_package_stepped_over'.
_PROJECT = 'promise_warnings_project'
_PROJECT_ROOT = os.path.join(os.sep, 'nowhere', _PROJECT)
_PROJECT_SOURCE = """
from worktoy.waitaminute import RiskWarning


class ProjectRisk(RiskWarning):
  pass


def check(price):
  ProjectRisk('price', price, 'a loss').warn()
"""


def _record(func: Callable, *args, **kwargs) -> tuple:
  """Call 'func' and give its result and the warnings it gave."""
  with warnings.catch_warnings(record=True) as notices:
    warnings.simplefilter('always')
    result = func(*args, **kwargs)
  return result, notices


class PromiseWarnings(TestCase):
  """
  From 1.3.0, a warning of worktoy stops nothing: what it warns about is
  carried out as promised. Every warning is a 'WorkToyWarning' and the
  builtin category it keeps, so Python's warning filters treat it as any
  warning of that category, and one filter on 'WorkToyWarning' covers
  them all: 'DeprecatedPromise' a 'FutureWarning', 'RedundantKeyword' and
  'AlternativeWarning' a 'UserWarning', 'RiskWarning' a 'RuntimeWarning'.
  'textFmt', 'joinWords', 'wordWrap', 'stringList', 'unpack' and
  'resolveMRO' give 'RedundantKeyword' for a keyword they do not read and
  go on without it. 'warn()' gives a warning at the line that called
  into worktoy, and, for the warning class of a project, into the
  package of that class as well. Each warning keeps what it was given as
  attributes: 'RiskWarning(name, value, risk)' as 'varName',
  'actualObject' and 'risk'; 'AlternativeWarning(behaviour, alternative,
  reason)' as 'behaviour', 'alternative' and 'reason';
  'DeprecatedPromise(feature, description)' as 'feature' and
  'description'; 'RedundantKeyword(receiver, keyword, *options)' as
  'receiver', 'keyword' and 'options'. The wording of a warning is not
  promised. Source: the docstrings of these warnings and section 6 of
  the waitaminute part of 'design/manual.md'.
  """

  def test_family(self) -> None:
    for warningClass, category in FAMILY.items():
      with self.subTest(warning=warningClass.__name__):
        self.assertTrue(issubclass(warningClass, WorkToyWarning))
        self.assertTrue(issubclass(warningClass, category))
    self.assertTrue(issubclass(WorkToyWarning, Warning))

  def test_one_filter_covers_them_all(self) -> None:
    with warnings.catch_warnings(record=True) as notices:
      warnings.simplefilter('always')
      warnings.simplefilter('ignore', WorkToyWarning)
      RiskWarning('price', -5, 'a loss').warn()
      AlternativeWarning('old', 'new', 'it is better').warn()
      joinWords('tea', 'coffee', seperator='or')
    self.assertEqual(notices, [])

  def test_redundant_keyword(self) -> None:
    calls = {
      'textFmt': (textFmt, ('a  b',), 'a b'),
      'joinWords': (joinWords, ('tea', 'coffee'), 'tea and coffee'),
      'wordWrap': (wordWrap, (20, 'a b'), 'a b'),
      'stringList': (stringList, ('a, b',), ['a', 'b']),
      'unpack': (unpack, ([1, 2],), (1, 2)),
      'resolveMRO': (resolveMRO, (int,), [int, object]),
    }
    for name, (func, args, expected) in calls.items():
      with self.subTest(helper=name):
        result, notices = _record(func, *args, misspelled=True)
        self.assertEqual(result, expected)
        self.assertEqual(len(notices), 1)
        self.assertIsInstance(notices[0].message, RedundantKeyword)
        self.assertEqual(notices[0].message.keyword, 'misspelled')

  def test_redundant_keyword_attributes(self) -> None:
    _, notices = _record(joinWords, 'tea', 'coffee', seperator='or')
    notice = notices[0].message
    self.assertIs(notice.receiver, joinWords)
    self.assertEqual(notice.keyword, 'seperator')
    self.assertEqual(notice.options, ('sep',))

  def test_given_at_the_calling_line(self) -> None:
    _, notices = _record(joinWords, 'tea', 'coffee', seperator='or')
    self.assertEqual(
        os.path.abspath(notices[0].filename),
        os.path.abspath(__file__),
    )

  def test_attributes(self) -> None:
    risk = RiskWarning('price', -5, 'a loss')
    self.assertEqual(
        (risk.varName, risk.actualObject, risk.risk),
        ('price', -5, 'a loss'),
    )
    other = AlternativeWarning('old', 'new', 'it is better')
    self.assertEqual(
        (other.behaviour, other.alternative, other.reason),
        ('old', 'new', 'it is better'),
    )
    deprecated = DeprecatedPromise('feature', 'use the other')
    self.assertEqual(
        (deprecated.feature, deprecated.description),
        ('feature', 'use the other'),
    )
    redundant = RedundantKeyword('helper', 'typo', 'size', 'width')
    self.assertEqual(
        (redundant.receiver, redundant.keyword, redundant.options),
        ('helper', 'typo', ('size', 'width')),
    )

  def test_warn_gives_the_warning(self) -> None:
    _, notices = _record(RiskWarning('price', -5, 'a loss').warn)
    self.assertEqual(len(notices), 1)
    self.assertIsInstance(notices[0].message, RiskWarning)
    self.assertEqual(notices[0].message.varName, 'price')

  def test_project_package_stepped_over(self) -> None:
    package = types.ModuleType(_PROJECT)
    package.__path__ = [_PROJECT_ROOT]
    space = {'__name__': '%s.warns' % _PROJECT}
    fileName = os.path.join(_PROJECT_ROOT, 'warns.py')
    sys.modules[_PROJECT] = package
    try:
      exec(compile(_PROJECT_SOURCE, fileName, 'exec'), space)
      _, notices = _record(space['check'], -5)
    finally:
      del sys.modules[_PROJECT]
    self.assertEqual(len(notices), 1)
    self.assertIsInstance(notices[0].message, space['ProjectRisk'])
    self.assertEqual(
        os.path.abspath(notices[0].filename),
        os.path.abspath(__file__),
    )
