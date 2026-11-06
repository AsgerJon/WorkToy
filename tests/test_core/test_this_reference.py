"""
TestThisReference tests '_SetDescriptorName' from
'worktoy.core.sentinels._this', the reference 'THIS[Parent].x' gives.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest import skipIf

from worktoy.core.sentinels import THIS
from worktoy.core.sentinels._this import _SetDescriptorName
from worktoy.desc import AttriBox
from worktoy.waitaminute import MissingVariable
from . import CoreTest, Grand, Agreeable

if sys.version_info >= (3, 9):  # pragma: no branch
  from ._this_sugar_helpers import decorateEveryHook


class TestThisReference(CoreTest):
  """
  The reference 'THIS[Parent].x' takes a clone of the descriptor at once
  and offers the seven notification decorators and every other name of
  the clone, so decorating through the reference works as decorating the
  descriptor itself would, while the base keeps its 'x' untouched. The
  tests pin the clone, the seven decorators acting on it, the pass-through
  of other names, the refusals of a reference without parent or name,
  the peek at the clone, and the rule deciding whether a subclass body
  declares the name itself. The decorator spelling is syntax from 3.9
  on, so the class using it is built by a helper module imported only
  there, and its test is skipped below.
  """

  @staticmethod
  def _consume(holder: type) -> type:
    """A throwaway subclass that takes any clones pending on the holder."""
    return type('Consumer', (holder,), {'__module__': __name__})

  def test_clone_taken_at_once(self) -> None:
    self.addCleanup(self._consume, Grand)
    reference = THIS[Grand].x
    clone = reference.getNewDescriptor()
    self.assertIsInstance(clone, AttriBox)
    self.assertIsNot(clone, Grand.__dict__['x'])
    self.assertIs(reference.getParentDescriptor(), Grand.__dict__['x'])
    self.assertIs(reference.getNewDescriptor(), clone)

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_decorators_act_on_clone(self) -> None:
    log = []
    Child = decorateEveryHook(Grand, log)
    self.assertEqual(log, [('setName', 'Child', 'x')])
    child = Child()
    self.assertEqual(child.x, 1)
    child.x = 5
    del child.x
    self.assertEqual(log, [
      ('setName', 'Child', 'x'), 'preGet', ('onGet', 1), ('preSet', 5),
      ('onSet', 5), 'preDelete', 'onDelete',
    ])
    log.clear()
    grand = Grand()
    self.assertEqual(grand.x, 1)
    grand.x = 2
    del grand.x
    self.assertEqual(log, [])
    for name in ('_a', '_b', '_c', '_d', '_e', '_f', '_g'):
      with self.subTest(name=name):
        self.assertTrue(callable(Child.__dict__[name]))

  def test_other_names_read_off_clone(self) -> None:
    self.addCleanup(self._consume, Grand)
    reference = THIS[Grand].x
    clone = reference.getNewDescriptor()
    self.assertEqual(reference.getFieldName(), clone.getFieldName())
    self.assertIs(reference.getFieldOwner(), clone.getFieldOwner())
    with self.assertRaises(AttributeError) as context:
      _ = reference.nothing
    self.assertEqual(str(context.exception),
                     "'AttriBox' has no attribute 'nothing'")

  def test_reference_without_parent_or_name(self) -> None:
    blank = _SetDescriptorName.__new__(_SetDescriptorName)
    with self.assertRaises(MissingVariable) as context:
      blank._getParent()
    self.assertEqual(context.exception.varName, '__parent_class__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'_SetDescriptorName.__parent_class__: type'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      blank._getDescriptorName()
    self.assertEqual(context.exception.varName, '__descriptor_name__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'_SetDescriptorName.__descriptor_name__: str'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      blank.getParentDescriptor()
    self.assertEqual(context.exception.varName, '__parent_class__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (type,))

  def test_clone_peek(self) -> None:
    blank = _SetDescriptorName.__new__(_SetDescriptorName)
    blank.__parent_class__ = Grand
    blank.__descriptor_name__ = 'x'
    with self.assertRaises(RecursionError) as context:
      blank.getNewDescriptor(_recursion=True)
    self.assertEqual(context.exception.args, ())
    clone = blank.getNewDescriptor()
    self.assertIsInstance(clone, AttriBox)
    self.assertIs(blank.getNewDescriptor(_recursion=True), clone)

  def test_is_declared_by(self) -> None:
    self.addCleanup(self._consume, Grand)
    reference = THIS[Grand].x
    clone = reference.getNewDescriptor()
    self.assertFalse(reference.isDeclaredBy(SimpleNamespace()))
    self.assertTrue(reference.isDeclaredBy(SimpleNamespace(x=1)))
    self.assertTrue(reference.isDeclaredBy(SimpleNamespace(x=Agreeable())))
    self.assertFalse(reference.isDeclaredBy(SimpleNamespace(x=clone)))
    bound = SimpleNamespace(__namespace__={'x': 1}, x=1)
    self.assertTrue(reference.isDeclaredBy(bound))
    added = SimpleNamespace(__namespace__={}, x=1)
    self.assertFalse(reference.isDeclaredBy(added))
    kept = SimpleNamespace(__namespace__={'x': clone}, x=clone)
    self.assertFalse(reference.isDeclaredBy(kept))
