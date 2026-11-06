"""
TestObjectContext tests the frame stack of 'Object' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import WithoutException
from . import CoreTest, Holder, Liar


class TestObjectContext(CoreTest):
  """
  The code of a descriptor asks for the instance and owner of the access
  in progress instead of being handed them. 'Object' keeps a stack of
  frames for that. The tests pin the stack driven by hand, the refusal
  of a pop without a push, and each answer 'getContextInstance' and
  'getContextOwner' give outside an access: a plain 'AttributeError' for
  a value no class holds, 'WithoutException' for a placed descriptor,
  the instance through the box for a value a box built while the box
  reads, and the guard against a 'hasContext' answering wrongly.
  """

  def test_stack_by_hand(self) -> None:
    desc = Object()
    self.assertFalse(desc.hasContext())
    self.assertIs(desc.createContext(1, int), desc)
    self.assertTrue(desc.hasContext())
    self.assertEqual((desc.getContextInstance(), desc.getContextOwner()),
                     (1, int))
    desc.createContext('a', str)
    self.assertEqual((desc.getContextInstance(), desc.getContextOwner()),
                     ('a', str))
    self.assertIs(desc.exitContext(), desc)
    self.assertEqual((desc.getContextInstance(), desc.getContextOwner()),
                     (1, int))
    desc.exitContext()
    self.assertFalse(desc.hasContext())

  def test_exit_without_frame_refused(self) -> None:
    desc = Object()
    with self.assertRaises(WithoutException) as context:
      desc.exitContext()
    self.assertIs(context.exception.desc, desc)
    self.assertIsInstance(context.exception, RuntimeError)
    self.assertIn("'NO-OWNER.NO-FIELD'", str(context.exception))

  def test_unplaced_object_has_no_instance(self) -> None:
    desc = Object()
    with self.assertRaises(AttributeError) as context:
      desc.getContextInstance()
    self.assertEqual(str(context.exception),
                     "'Object' object has no attribute 'instance'")
    with self.assertRaises(AttributeError) as context:
      desc.getContextOwner()
    self.assertEqual(str(context.exception),
                     "'Object' object has no attribute 'owner'")
    self.assertFalse(hasattr(desc, 'instance'))
    self.assertFalse(hasattr(desc, 'owner'))

  def test_placed_descriptor_outside_access_refused(self) -> None:
    class Owner:
      d = Object()

    with self.assertRaises(WithoutException) as context:
      Owner.d.getContextInstance()
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIn("'Owner.d'", str(context.exception))
    with self.assertRaises(WithoutException) as context:
      Owner.d.getContextOwner()
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIn("'Owner.d'", str(context.exception))
    with self.assertRaises(WithoutException) as context:
      hasattr(Owner.d, 'instance')
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIn('Context-less call', str(context.exception))
    with self.assertRaises(WithoutException) as context:
      hasattr(Owner.d, 'owner')
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIn('Context-less call', str(context.exception))

  def test_box_built_value_asks_through_box(self) -> None:
    holder = Holder()
    item = holder.item
    self.assertIs(holder.seenInstance, holder)
    self.assertIs(holder.seenOwner, Holder)
    self.assertIs(item.__field_box__, Holder.item)
    with self.assertRaises(AttributeError) as context:
      item.getContextInstance()
    self.assertEqual(str(context.exception),
                     "'Item' object has no attribute 'instance'")
    with self.assertRaises(AttributeError) as context:
      item.getContextOwner()
    self.assertEqual(str(context.exception),
                     "'Item' object has no attribute 'owner'")
    self.assertFalse(hasattr(item, 'instance'))
    self.assertFalse(hasattr(item, 'owner'))

  def test_lying_has_context_caught(self) -> None:
    liar = Liar.__new__(Liar)
    self.assertTrue(liar.hasContext())
    with self.assertRaises(MissingVariable) as context:
      liar.getContextInstance()
    self.assertEqual(context.exception.varName, '__call_chain__')
    self.assertIs(context.exception.instance, liar)
    self.assertEqual(context.exception.expectedTypes, (list,))
    self.assertIn("'Liar.__call_chain__: list'", str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      liar.getContextOwner()
    self.assertEqual(context.exception.varName, '__call_chain__')
    self.assertIs(context.exception.instance, liar)
    self.assertEqual(context.exception.expectedTypes, (list,))
    self.assertIn("'Liar.__call_chain__: list'", str(context.exception))
