"""
TestPlainDictNewClassPhase subclasses 'MCLSTest' and pins that calling a
worktoy metaclass directly with a plain dict runs the 'newClassPhase' of
the hooks, as a class statement does. 'AbstractMetaclass.__new__' builds
a namespace of its own for a plain dict, but asked the dict it was given
for the hooks, so the phase never ran.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass, AbstractNamespace
from worktoy.mcls.space_hooks import AbstractSpaceHook

from .. import MCLSTest

created = []


class RecordHook(AbstractSpaceHook):
  """RecordHook records every class its namespace creates."""

  def newClassPhase(self, cls: type) -> type:
    created.append(cls.__name__)
    return cls


class RecordSpace(AbstractNamespace):
  """RecordSpace declares 'RecordHook'."""

  recordHook = RecordHook()


class RecordMeta(AbstractMetaclass):
  """RecordMeta prepares a 'RecordSpace'."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> RecordSpace:
    return RecordSpace(mcls, name, bases, **kwargs)


class TestPlainDictNewClassPhase(MCLSTest):
  """
  TestPlainDictNewClassPhase provides tests for calling a worktoy
  metaclass with a plain dict.
  """

  def test_plain_dict(self) -> None:
    """A plain dict runs 'newClassPhase' and keeps its entries."""
    Foo = RecordMeta('Foo', (), {'x': 1})
    self.assertIn('Foo', created)
    self.assertEqual(Foo.x, 1)

  def test_class_statement(self) -> None:
    """A class statement runs it as before."""

    class Bar(metaclass=RecordMeta):
      pass

    self.assertIn('Bar', created)
