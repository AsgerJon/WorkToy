"""
TestOverloadClasses tests 'overload' end to end on classes based on
'BaseObject'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher
from worktoy.waitaminute.dispatch import DispatchException
from . import DispatchTest, Label, Tally, Counter, Shape, Square
from . import Fallbacked, Wide


class TestOverloadClasses(DispatchTest):
  """
  The package serves a class based on 'BaseObject', whose namespace
  turns the records into dispatchers. The tests pin, on the fixtures of
  the folder, a flexible constructor with 'THIS', a concrete signature
  beside variadic ones, a classmethod and a staticmethod, inheritance
  with a redeclared and an added signature, a fallback with a finalizer,
  and a flexible declaration of four classes.
  """

  def test_label(self) -> None:
    first = Label('a', 1)
    self.assertEqual((first.text, first.count), ('a', 1))
    second = Label(2, 'b')
    self.assertEqual((second.text, second.count), ('b', 2))
    copied = Label(first)
    self.assertEqual((copied.text, copied.count), ('a!', 1))
    blank = Label()
    self.assertEqual((blank.text, blank.count), ('', 0))
    self.assertIsInstance(Label.__dict__['__init__'], Dispatcher)
    with self.assertRaises(DispatchException) as context:
      Label(1.5)
    self.assertIs(context.exception.dispatch, Label.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, (1.5,))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'Label.__init__'", str(context.exception))

  def test_tally(self) -> None:
    tally = Tally()
    self.assertEqual(tally.add(1, 2), ('pair', 3))
    self.assertEqual(tally.add(1, 2, 3), ('ints', 6))
    self.assertEqual(tally.add(), ('ints', 0))
    self.assertEqual(tally.add('x', 4, 5), ('x', 9))
    self.assertEqual(tally.add('x'), ('x', 0))
    with self.assertRaises(DispatchException) as context:
      tally.add(1, 'x')
    self.assertIs(context.exception.dispatch, Tally.__dict__['add'])
    self.assertEqual(context.exception.posArgs, (1, 'x'))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("'Tally.add'", str(context.exception))

  def test_counter(self) -> None:
    self.assertEqual(Counter.make(1), ('Counter', 'int', 1))
    self.assertEqual(Counter().make('s'), ('Counter', 'str', 's'))
    self.assertEqual(Counter.add(1, 2), 3)
    self.assertEqual(Counter().add(3, 4), 7)
    self.assertIs(Counter.__dict__['make'].getMethodKind(), classmethod)
    self.assertIs(Counter.__dict__['add'].getMethodKind(), staticmethod)

  def test_shape_and_square(self) -> None:
    square = Square()
    self.assertEqual(square.scale(1), ('square-int', 1))
    self.assertEqual(square.scale(1.5), ('square-float', 1.5))
    self.assertEqual(square.scale(Shape()), ('shape-this', 'Shape'))
    self.assertEqual(square.scale(Square()), ('shape-this', 'Square'))
    self.assertEqual(Shape().scale(2), ('shape-int', 2))
    dispatcher = Square.__dict__['scale']
    self.assertEqual(dispatcher._getSigDistances(), [0, 0, 1])
    declared = [sig.getRawTypes() for sig in dispatcher._getDeclaredSigs()]
    self.assertEqual(declared, [(float,), (int,), (Shape,)])

  def test_fallbacked(self) -> None:
    Fallbacked.log.clear()
    taker = Fallbacked()
    self.assertEqual(taker.take(1), ('int', 1))
    self.assertEqual(taker.take('x', k=2), ('fallback', ('x',), {'k': 2}))
    self.assertEqual(Fallbacked.log, [('final', (1,)), ('final', ('x',))])

  def test_wide(self) -> None:
    wide = Wide()
    self.assertEqual(wide.mix(b'b', 1.5, 1, 's'), ('s', 1, 1.5, b'b'))
    self.assertEqual(wide.mix('s', 1, 1.5, b'b'), ('s', 1, 1.5, b'b'))
    self.assertEqual(len(Wide.__dict__['mix']._getFlexFuncs()), 1)
    self.assertEqual(Wide.__dict__['mix']._getSigFuncList(), [])

  def test_overloaded_name_refuses_this_reference(self) -> None:
    from worktoy.core.sentinels import THIS
    from worktoy.waitaminute.desc import OverloadReference
    self.assertTrue(Dispatcher.__no_this_reference__)
    with self.assertRaises(OverloadReference) as context:
      _ = THIS[Shape].scale
    self.assertEqual(context.exception.parentName, 'Shape')
    self.assertEqual(context.exception.fieldName, 'scale')
    self.assertIn("'THIS[Shape].scale'", str(context.exception))
