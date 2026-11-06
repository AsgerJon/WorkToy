"""
TestThisSubscript tests 'THIS[Parent]' and 'THIS[Parent].name' from
'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.core.sentinels._this import _SetParent, _SetDescriptorName
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.waitaminute.desc import DanglingAlias, OverloadReference
from . import CoreTest, Grand, Parent


class TestThisSubscript(CoreTest):
  """
  'THIS[Parent]' names a base whose descriptors a class body expands on,
  and 'THIS[Parent].x' is the reference to 'x' as the subclass will hold
  it, found on the first class along the resolution order of 'Parent'
  that holds 'x' itself. The tests pin the subscript and its refusals,
  the hook installed once on the holder, the refusal of a name no class
  holds and of a name holding an overloaded method, the one reference
  shared by 'THIS[Parent].x' and 'THIS[Grand].x', and the record kept on
  the holder until its next subclass.
  """

  @staticmethod
  def _consume(holder: type) -> type:
    """A throwaway subclass that takes any clones pending on the holder."""
    return type('Consumer', (holder,), {'__module__': __name__})

  def test_subscript_gives_reference_root(self) -> None:
    root = THIS[Grand]
    self.assertIsInstance(root, _SetParent)
    self.assertIs(root._getParent(), Grand)

  def test_non_class_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      _ = THIS[5]
    self.assertEqual(context.exception.varName, 'parent')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'parent'", str(context.exception))

  def test_builtin_refused_by_python(self) -> None:
    with self.assertRaises(TypeError):
      _ = THIS[int]

  def test_root_without_parent(self) -> None:
    blank = _SetParent.__new__(_SetParent)
    with self.assertRaises(MissingVariable) as context:
      blank._getParent()
    self.assertEqual(context.exception.varName, '__parent_class__')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'_SetParent.__parent_class__: type'",
                  str(context.exception))

  def test_hook_installed_once(self) -> None:
    _ = THIS[Grand]
    hook = Grand.__dict__['__init_subclass__']
    self.assertTrue(object.__getattribute__(hook, '__this_new_desc__'))
    _ = THIS[Grand]
    self.assertIs(Grand.__dict__['__init_subclass__'], hook)

  def test_name_no_class_holds_refused(self) -> None:
    with self.assertRaises(DanglingAlias) as context:
      _ = THIS[Grand].nothing
    self.assertEqual(context.exception.realName, 'nothing')
    self.assertIs(context.exception.owner, Grand)
    self.assertIsInstance(context.exception.alias, _SetParent)
    self.assertIn("'nothing'", str(context.exception))
    self.assertIn("'Grand'", str(context.exception))
    self.assertIsInstance(context.exception, SyntaxError)
    with self.assertRaises(DanglingAlias) as context:
      hasattr(THIS[Parent], 'nothing')
    self.assertEqual(context.exception.realName, 'nothing')
    self.assertIs(context.exception.owner, Parent)
    self.assertIsInstance(context.exception.alias, _SetParent)
    self.assertIn("'Parent'", str(context.exception))
    with self.assertRaises(DanglingAlias) as context:
      getattr(THIS[Parent], 'nothing', None)
    self.assertEqual(context.exception.realName, 'nothing')
    self.assertIs(context.exception.owner, Parent)
    self.assertIn("'nothing'", str(context.exception))

  def test_overloaded_name_refused(self) -> None:
    with self.assertRaises(OverloadReference) as context:
      _ = THIS[Grand].blocked
    self.assertEqual(context.exception.parentName, 'Grand')
    self.assertEqual(context.exception.fieldName, 'blocked')
    self.assertIsInstance(context.exception, SyntaxError)
    self.assertIn("'THIS[Grand].blocked'", str(context.exception))
    with self.assertRaises(OverloadReference) as context:
      _ = THIS[Parent].blocked
    self.assertEqual(context.exception.parentName, 'Parent')
    self.assertEqual(context.exception.fieldName, 'blocked')
    self.assertIn("'THIS[Parent].blocked'", str(context.exception))
    self.assertNotIn('blocked',
                     _SetDescriptorName.newDescriptorsOnParent(Grand))

  def test_value_without_clone_refused(self) -> None:
    with self.assertRaises(AttributeError) as context:
      _ = THIS[Grand].plain
    self.assertIn('clone', str(context.exception))
    self.assertNotIn('plain',
                     _SetDescriptorName.newDescriptorsOnParent(Grand))

  def test_one_reference_along_resolution_order(self) -> None:
    self.addCleanup(self._consume, Parent)
    inherited = THIS[Parent].x
    self.assertIs(inherited, THIS[Grand].x)
    self.assertIs(inherited, THIS[Parent].x)
    self.assertIsInstance(inherited, _SetDescriptorName)
    self.assertIs(inherited._getParent(), Grand)
    self.assertEqual(inherited._getDescriptorName(), 'x')
    own = THIS[Parent].y
    self.assertIs(own._getParent(), Parent)
    self.assertIs(THIS[Parent].y, own)
    self.assertIsNot(own, inherited)

  def test_record_kept_until_next_subclass(self) -> None:
    reference = THIS[Grand].x
    record = Grand.__dict__['__new_descriptors__']
    self.assertIs(record['x'], reference)
    self.assertIs(_SetDescriptorName.newDescriptorsOnParent(Grand), record)
    consumer = self._consume(Grand)
    self.assertNotIn('__new_descriptors__', Grand.__dict__)
    self.assertIs(consumer.__dict__['x'], reference.getNewDescriptor())

  def test_record_peek(self) -> None:
    class Fresh:
      pass

    with self.assertRaises(RecursionError) as context:
      _SetDescriptorName.newDescriptorsOnParent(Fresh, _recursion=True)
    self.assertEqual(context.exception.args, ())
    record = _SetDescriptorName.newDescriptorsOnParent(Fresh)
    self.assertEqual(record, {})
    self.assertIs(Fresh.__dict__['__new_descriptors__'], record)
    peeked = _SetDescriptorName.newDescriptorsOnParent(Fresh,
                                                       _recursion=True)
    self.assertIs(peeked, record)
