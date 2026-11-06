"""
TestThisHandover tests the hook 'THIS' installs on a holder, which
places the clones on the next subclass created.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from unittest import skipIf

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import ReferenceConflict
from . import CoreTest, Grand, Parent, Hooked, Boxed

if sys.version_info >= (3, 9):  # pragma: no branch
  from ._this_sugar_helpers import hookedChild, boxedChild, twoHolders


class TestThisHandover(CoreTest):
  """
  The clones taken through 'THIS[Parent].x' reach the next subclass of
  the holder as it is created, placed and named, and no later subclass.
  A body declaring the name itself is refused with 'ReferenceConflict',
  the record going first so a refused body leaves nothing behind, while
  a body binding the clone itself is no conflict. The holder's own
  '__init_subclass__' still runs with every keyword. The tests pin each
  of these on a plain holder, a holder with a hook of its own, a worktoy
  holder, and a chain of two holders. The decorator spelling is syntax
  from 3.9 on, so the classes using it are built by a helper module
  imported only there, and their tests are skipped below.
  """

  def test_clone_placed_on_next_subclass_only(self) -> None:
    reference = THIS[Grand].x

    class Child(Grand):
      pass

    class Later(Grand):
      pass

    self.assertIs(Child.__dict__['x'], reference.getNewDescriptor())
    self.assertIs(Child.x.getFieldOwner(), Child)
    self.assertEqual(Child.x.getFieldName(), 'x')
    self.assertIsNot(Child.__dict__['x'], Grand.__dict__['x'])
    self.assertNotIn('__new_descriptors__', Grand.__dict__)
    self.assertNotIn('x', Later.__dict__)
    self.assertEqual(Child().x, 1)
    self.assertEqual(Later().x, 1)

  def test_declared_name_refused_and_record_dropped(self) -> None:
    _ = THIS[Grand].x
    with self.assertRaises(ReferenceConflict) as context:
      class Bad(Grand):
        x = AttriBox[int](9)
    self.assertEqual(context.exception.className, 'Bad')
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertEqual(context.exception.holderName, 'Grand')
    self.assertIn("'Bad'", str(context.exception))
    self.assertIn("'THIS[Grand].x'", str(context.exception))
    self.assertEqual(context.exception.holderName, 'Grand')
    self.assertIsInstance(context.exception, SyntaxError)
    self.assertNotIn('__new_descriptors__', Grand.__dict__)

    class Next(Grand):
      pass

    self.assertNotIn('x', Next.__dict__)

  def test_binding_the_clone_is_no_conflict(self) -> None:
    reference = THIS[Grand].x

    class Child(Grand):
      x = THIS[Grand].x.getNewDescriptor()

    self.assertIs(Child.__dict__['x'], reference.getNewDescriptor())
    self.assertIs(Child.x.getFieldOwner(), Child)
    self.assertEqual(Child().x, 1)

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_own_init_subclass_still_called_with_keywords(self) -> None:
    Hooked.records.clear()
    reference = THIS[Hooked].x
    log = []
    Child = hookedChild(Hooked, log)
    self.assertEqual(Hooked.records, [('Child', {'flag': True})])
    self.assertIs(Child.__dict__['x'], reference.getNewDescriptor())
    Child().x = 3
    self.assertEqual(log, [3])

    class Plain(Hooked):
      pass

    self.assertEqual(Hooked.records[-1], ('Plain', {}))
    self.assertNotIn('x', Plain.__dict__)

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_worktoy_holder(self) -> None:
    _ = THIS[Boxed].x
    with self.assertRaises(ReferenceConflict) as context:
      class Bad(Boxed):
        x = AttriBox[int](2)
    self.assertEqual(context.exception.holderName, 'Boxed')
    self.assertEqual(context.exception.className, 'Bad')
    self.assertEqual(context.exception.fieldName, 'x')
    self.assertIn("'THIS[Boxed].x'", str(context.exception))
    self.assertNotIn('__new_descriptors__', Boxed.__dict__)
    log = []
    reference = THIS[Boxed].x
    Child = boxedChild(Boxed, log)
    self.assertIs(Child.__dict__['x'], reference.getNewDescriptor())
    self.assertEqual(Child().x, 1)
    self.assertEqual(log, [1])
    self.assertEqual(Boxed().x, 1)
    self.assertEqual(log, [1])

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_two_holders_in_one_body(self) -> None:
    inherited = THIS[Parent].x
    own = THIS[Parent].y
    log = []
    Child = twoHolders(Parent, log)
    self.assertIs(Child.__dict__['x'], inherited.getNewDescriptor())
    self.assertIs(Child.__dict__['y'], own.getNewDescriptor())
    self.assertNotIn('__new_descriptors__', Grand.__dict__)
    self.assertNotIn('__new_descriptors__', Parent.__dict__)
    child = Child()
    self.assertEqual((child.x, child.y), (1, 'a'))
    self.assertEqual(log, [('x', 1), ('y', 'a')])
