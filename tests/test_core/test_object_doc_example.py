"""
TestObjectDocExample lifts the worked example out of the 'Object' class
docstring and runs it, so the published example stays honest. The example
defines a 'Counted' descriptor; the test executes that source verbatim
and exercises the get, set and del paths through a host class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from . import CoreTest
from worktoy.core import Object
from worktoy.core.sentinels import DELETED


def _liftDocExample() -> str:
  """Collects the doctest-style lines from the 'Object' class docstring
  and returns them joined as a single block of source code. Lines opening
  with the '>>> ' prompt or the '... ' continuation marker contribute
  their code; everything else in the docstring is ignored."""
  lines = []
  for rawLine in (Object.__doc__ or '').splitlines():
    line = rawLine.strip()
    if line.startswith('>>> '):
      lines.append(line[4:])
      continue
    if line.startswith('... '):
      lines.append(line[4:])
  return '\n'.join(lines)


class TestObjectDocExample(CoreTest):
  """
  TestObjectDocExample executes the example published in the 'Object'
  class docstring, confirming that a reader copying it gets a descriptor
  whose get, set and del operations work as shown.
  """

  def test_example_del_path(self) -> None:
    """
    The 'Counted' class defined in the docstring example supports
    reading, writing and deleting through a host class. In particular,
    'del' must not raise 'TypeError': '__delete__' passes the old value
    to '__instance_delete__', so the example signature has to accept it.
    """
    source = _liftDocExample()
    self.assertIn('class Counted', source)
    namespace = dict(Object=Object, DELETED=DELETED, Any=Any)
    exec(compile(source, '<Object docstring example>', 'exec'), namespace)
    Counted = namespace['Counted']

    class Host:
      count = Counted()

    host = Host()
    self.assertEqual(host.count, 0)
    host.count = 7
    self.assertEqual(host.count, 7)
    del host.count
    with self.assertRaises(AttributeError):
      _ = host.count
