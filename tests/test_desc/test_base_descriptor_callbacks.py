"""
TestBaseDescriptorCallbacks tests the notification decorators of
'BaseDescriptor' from 'worktoy.desc' and the lookup of their callbacks.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from functools import partial
from types import FunctionType

from worktoy.desc import AttriBox, BaseDescriptor
from worktoy.dispatch import isFlex
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import NamelessCallback
from . import DescTest, Watched, Listener


def __loose(self: object) -> None:
  """A private function of the module, which no class could hold."""


#  A class body mangles every name of two leading underscores it mentions,
#  so the function is reached through this plain name.
_loose = __loose


class TestBaseDescriptorCallbacks(DescTest):
  """
  The seven decorators record a method by name, and the hooks find it
  on the class of the instance at each access and call it by its kind,
  so a subclass overrides a callback by defining the name again. The
  tests pin the six access hooks in order with three kinds of method
  and a mangled private name, the overrides, the wrapped kinds the
  decorators return, the placement callback in every kind, a callback
  the class holds as something else, the refusals of what cannot be
  found by name, and the cache of wrappers.
  """

  def test_hooks_in_order_by_kind(self) -> None:
    Watched.log.clear()
    watched = Watched()
    self.assertEqual(watched.value, 0)
    self.assertEqual(Watched.log, [('preGet', 'Watched'), ('onGet', 0)])
    Watched.log.clear()
    watched.value = 5
    self.assertEqual(Watched.log, [('preSet', 'Watched', 5), ('onSet', 5)])
    Watched.log.clear()
    del watched.value
    self.assertEqual(Watched.log, [('preDelete',), ('onDelete',)])
    with self.assertRaises(MissingVariable) as context:
      _ = watched.value
    self.assertEqual(context.exception.varName, 'value')
    self.assertIs(context.exception.instance, watched)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Watched.value: object'", str(context.exception))

  def test_overrides_found_on_subclass(self) -> None:
    Watched.log.clear()
    listener = Listener()
    self.assertEqual(listener.value, 0)
    self.assertEqual(Watched.log, [('preGet', 'Listener'), ('sub-onGet', 0)])
    Watched.log.clear()
    listener.value = 7
    self.assertEqual(Watched.log, [('sub-preSet', 7), ('onSet', 7)])

  def test_decorators_return_wrapped_kind(self) -> None:
    held = Watched.__dict__
    self.assertIsInstance(held['_afterRead'], FunctionType)
    self.assertTrue(isFlex(held['_afterRead']))
    self.assertIsInstance(held['_beforeWrite'], classmethod)
    self.assertTrue(isFlex(held['_beforeWrite'].__func__))
    self.assertIsInstance(held['_afterWrite'], staticmethod)
    self.assertTrue(isFlex(held['_afterWrite'].__func__))
    self.assertIn('_Watched__beforeDelete', held)
    box = held['value']
    self.assertEqual(box._getPreGetKeys(), ('_beforeRead',))
    self.assertEqual(box._getOnGetKeys(), ('_afterRead',))
    self.assertEqual(box._getPreSetKeys(), ('_beforeWrite',))
    self.assertEqual(box._getOnSetKeys(), ('_afterWrite',))
    self.assertEqual(box._getPreDeleteKeys(), ('_Watched__beforeDelete',))
    self.assertEqual(box._getOnDeleteKeys(), ('_afterDelete',))
    self.assertEqual(box._getSetNameKeys(), ())

  def test_set_name_callback_kinds(self) -> None:
    log = []

    class Owner:
      n = AttriBox[int](0)

      @n.setName
      def _plain(cls, desc: AttriBox) -> None:
        log.append(('plain', cls.__name__, desc.getFieldName()))

      @n.setName
      @classmethod
      def _classy(cls, desc: AttriBox) -> None:
        log.append(('classy', cls.__name__, desc.getFieldName()))

      @n.setName
      @staticmethod
      def _static(desc: AttriBox) -> None:
        log.append(('static', desc.getFieldName()))

    self.assertEqual(log, [
      ('plain', 'Owner', 'n'), ('classy', 'Owner', 'n'), ('static', 'n'),
    ])
    self.assertEqual(Owner.__dict__['n']._getSetNameKeys(),
                     ('_plain', '_classy', '_static'))

  def test_set_name_callback_held_as_something_else(self) -> None:
    log = []

    class Caller:
      def __call__(self, desc: AttriBox) -> None:
        log.append(('called', desc.getFieldName()))

    class Binder:
      def __get__(self, instance: object, owner: type) -> object:
        return lambda desc: log.append(('bound', owner.__name__))

    class Owner:
      n = AttriBox[int](0)

      @n.setName
      def _react(cls, desc: AttriBox) -> None:
        log.append(('function',))

    class Calling(Owner):
      _react = Caller()

    class Binding(Owner):
      _react = Binder()

    box = Owner.__dict__['n']
    log.clear()
    box.hookSetName(Calling, 'n')
    box.hookSetName(Binding, 'n')
    self.assertEqual(log, [('called', 'n'), ('bound', 'Binding')])

  def test_access_callback_held_as_something_else(self) -> None:
    log = []

    class Caller:
      def __call__(self, value: int) -> None:
        log.append(('called', value))

    class Binder:
      def __get__(self, instance: object, owner: type) -> object:
        name = type(instance).__name__
        return lambda value: log.append(('bound', name, value))

    class Owner:
      n = AttriBox[int](0)

      @n.onSet
      def _react(self, value: int) -> None:
        log.append(('method', value))

    class Calling(Owner):
      _react = Caller()

    class Binding(Owner):
      _react = Binder()

    Owner().n = 1
    Calling().n = 2
    Binding().n = 3
    self.assertEqual(log, [
      ('method', 1), ('called', 2), ('bound', 'Binding', 3),
    ])

  def test_deleted_callback_is_pythons_refusal(self) -> None:
    class Owner:
      n = AttriBox[int](0)

      @n.onGet
      def _react(self, value: int) -> None:
        """Deleted below."""

    del Owner._react
    with self.assertRaises(AttributeError):
      _ = Owner().n

  def test_nameless_callbacks_refused(self) -> None:
    box = AttriBox[int](0)
    with self.assertRaises(NamelessCallback) as context:
      box.onGet(lambda self, value: None)
    self.assertIs(context.exception.desc, box)
    self.assertEqual(context.exception.role, 'onGet')
    self.assertEqual(context.exception.callback.__name__, '<lambda>')
    self.assertIsInstance(context.exception, SyntaxError)
    self.assertIn("The 'onGet' decorator of the 'AttriBox' descriptor",
                  str(context.exception))
    self.assertIn("received '<lambda>'", str(context.exception))

    def __inner(self: object) -> None:
      """A private function inside a function has no class to mangle."""

    with self.assertRaises(NamelessCallback) as context:
      box.preGet(__inner)
    self.assertIs(context.exception.desc, box)
    self.assertEqual(context.exception.role, 'preGet')
    self.assertIs(context.exception.callback, __inner)
    self.assertIn("The 'preGet' decorator", str(context.exception))
    with self.assertRaises(NamelessCallback) as context:
      box.preSet(_loose)
    self.assertIs(context.exception.desc, box)
    self.assertEqual(context.exception.role, 'preSet')
    self.assertIs(context.exception.callback, _loose)
    self.assertIn("The 'preSet' decorator", str(context.exception))
    self.assertEqual(box._getOnGetKeys(), ())
    self.assertEqual(box._getPreGetKeys(), ())

  def test_private_name_mangled_unless_class_is_underscores(self) -> None:
    log = []

    class __(object):
      n = AttriBox[int](0)

      @n.preGet
      def __peek(self) -> None:
        log.append('peek')

    self.assertEqual(__.__dict__['n']._getPreGetKeys(), ('__peek',))
    self.assertEqual(__().n, 0)
    self.assertEqual(log, ['peek'])

  def test_not_a_function_refused(self) -> None:
    box = AttriBox[int](0)
    for callback in (partial(print, 1), classmethod(5), 5, print):
      with self.subTest(callback=callback):
        with self.assertRaises(TypeException) as context:
          box.onSet(callback)
        self.assertEqual(context.exception.varName, 'callback')
        self.assertIs(context.exception.actualObject, callback)
        self.assertIs(context.exception.actualType, type(callback))
        self.assertEqual(context.exception.expectedTypes,
                         (FunctionType, classmethod, staticmethod))
        self.assertIn("'callback'", str(context.exception))

  def test_peel_and_wrap(self) -> None:
    def func(self: object) -> None:
      """A plain function."""

    self.assertEqual(BaseDescriptor._peelCallback(func), (None, func))
    self.assertEqual(BaseDescriptor._peelCallback(classmethod(func)),
                     (classmethod, func))
    self.assertEqual(BaseDescriptor._peelCallback(staticmethod(func)),
                     (staticmethod, func))
    wrapped = BaseDescriptor._wrapCallback(staticmethod(func))
    self.assertIsInstance(wrapped, staticmethod)
    self.assertTrue(isFlex(wrapped.__func__))
    self.assertTrue(isFlex(BaseDescriptor._wrapCallback(func)))

  def test_wrapper_cached(self) -> None:
    def func(self: object) -> None:
      """A plain function."""

    box = AttriBox[int](0)
    first = box._getWrapper(func)
    self.assertIs(box._getWrapper(func), first)
    self.assertIs(box._getWrapper(first), first)
    self.assertTrue(isFlex(first))

  def test_fewer_parameters_than_passed(self) -> None:
    log = []

    class Owner:
      n = AttriBox[int](0)

      @n.onSet
      def _react(self) -> None:
        log.append('set')

      @n.onGet
      @staticmethod
      def _peek() -> None:
        log.append('get')

    owner = Owner()
    owner.n = 1
    _ = owner.n
    self.assertEqual(log, ['set', 'get'])

  def test_set_name_callbacks_in_every_order(self) -> None:
    log = []

    class Owner:
      n = AttriBox[int](0)

      @n.setName
      @staticmethod
      def _static(desc: AttriBox) -> None:
        log.append('static')

      @n.setName
      @classmethod
      def _classy(cls, desc: AttriBox) -> None:
        log.append('classy')

      @n.setName
      def _plain(cls, desc: AttriBox) -> None:
        log.append('plain')

    self.assertEqual(log, ['static', 'classy', 'plain'])
