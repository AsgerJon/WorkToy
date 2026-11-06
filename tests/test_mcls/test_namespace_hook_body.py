"""
TestNamespaceHookBody tests the screening of class-body bindings by
'NamespaceHook' from 'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import METACALL
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import AbstractNamespace, BaseMeta, BaseSpace, BaseObject
from worktoy.mcls import AbstractMetaclass
from worktoy.mcls.space_hooks import NamespaceHook
from worktoy.waitaminute.meta import SlotsRefused, DelException
from worktoy.waitaminute.meta import QuestionableSyntax, UnboundClassHook
from worktoy.waitaminute.meta import ShadowedClassHook
from . import MclsTest, SizedMeta, LoudMeta


class TestNamespaceHookBody(MclsTest):
  """
  'NamespaceHook' fails a class body at the line making one of the
  mistakes Python ignores: '__slots__', a '__del__' not vouched for, a
  misspelled dunder, a class hook that is no classmethod, and a class
  hook whose operation the metaclass takes over. The tests pin each
  refusal with its attributes, the bindings that pass, and the helpers
  the hook decides by.
  """

  def test_slots_refused(self) -> None:
    with self.assertRaises(SlotsRefused) as context:
      class A(BaseObject):
        __slots__ = ('x',)

    self.assertEqual(context.exception.className, 'A')
    self.assertIn("'A'", str(context.exception))
    space = BaseSpace(BaseMeta, 'B', ())
    with self.assertRaises(SlotsRefused) as context:
      space[str.join('', ['__slo', 'ts__'])] = ()
    self.assertEqual(context.exception.className, 'B')
    self.assertIn("The class body of 'B' binds '__slots__'",
                  str(context.exception))
    with self.assertRaises(DelException) as context:
      space[str.join('', ['__d', 'el__'])] = None
    self.assertIs(context.exception.mcls, BaseMeta)
    self.assertEqual(context.exception.name, 'B')
    self.assertEqual(context.exception.bases, ())
    self.assertIs(context.exception.space, space)
    self.assertIn("named 'B'", str(context.exception))

  def test_del_refused_unless_vouched_for(self) -> None:
    with self.assertRaises(DelException) as context:
      class A(BaseObject):
        def __del__(self) -> None:
          """Almost always a typo for '__delete__'."""

    exception = context.exception
    self.assertIs(exception.mcls, BaseMeta)
    self.assertEqual(exception.name, 'A')
    self.assertEqual(exception.bases, (BaseObject,))
    self.assertIsInstance(exception.space, BaseSpace)
    self.assertEqual(exception.space.getClassName(), 'A')
    self.assertIn('with bases: (BaseObject)', str(exception))

    class B(BaseObject, trustMeBro=True):
      def __del__(self) -> None:
        """Meant."""

    self.assertIn('__del__', B.__dict__)
    self.assertEqual(B.__keyword_arguments__, {'trustMeBro': True})

  def test_del_refused_without_bases(self) -> None:
    with self.assertRaises(DelException) as context:
      class A(metaclass=BaseMeta):
        def __del__(self) -> None:
          """Unvouched."""

    self.assertEqual(context.exception.bases, ())
    self.assertNotIn('with bases', str(context.exception))

  def test_near_misses_refused(self) -> None:
    pairs = (
      ('__set_name__', '__setname__'),
      ('__getitem__', '__get_item__'),
      ('__setitem__', '__set_item__'),
      ('__delitem__', '__del_item__'),
    )
    self.assertEqual(NamespaceHook._getNearMisses(), [*pairs])
    space = BaseSpace(BaseMeta, 'A', ())
    for real, derp in pairs:
      with self.subTest(derp=derp):
        with self.assertRaises(QuestionableSyntax) as context:
          space[derp] = 1
        self.assertEqual(context.exception.realName, real)
        self.assertEqual(context.exception.derpName, derp)
        self.assertIn("Received name '%s'" % derp, str(context.exception))
        self.assertNotIn(derp, dict.keys(space))
    with self.assertRaises(QuestionableSyntax) as context:
      class A(BaseObject):
        def __get_item__(self, key: str) -> None:
          """Misspelled."""

    self.assertEqual(context.exception.realName, '__getitem__')
    self.assertEqual(context.exception.derpName, '__get_item__')
    self.assertIn("'__getitem__'", str(context.exception))
    with self.assertRaises(QuestionableSyntax) as context:
      space[str.join('', ['__set', 'name__'])] = 1
    self.assertEqual(context.exception.realName, '__set_name__')
    self.assertEqual(context.exception.derpName, '__setname__')
    self.assertIn("'__setname__'", str(context.exception))

  def test_hook_bound_to_function_refused(self) -> None:
    with self.assertRaises(UnboundClassHook) as context:
      class A(BaseObject):
        def __class_len__(cls) -> None:
          """Refused: no classmethod."""

    self.assertEqual(context.exception.className, 'A')
    self.assertEqual(context.exception.hookName, '__class_len__')
    self.assertIsNone(context.exception.baseName)
    self.assertIn("'A'", str(context.exception))

  def test_hook_bound_to_other_values_refused(self) -> None:
    space = BaseSpace(BaseMeta, 'A', ())

    def plain(cls) -> None:
      """A function that is no classmethod."""

    values = (staticmethod(plain), 3, overload(int)(plain))
    for value in values:
      with self.subTest(value=type(value).__name__):
        with self.assertRaises(UnboundClassHook) as context:
          space['__class_len__'] = value
        self.assertEqual(context.exception.hookName, '__class_len__')
        self.assertEqual(context.exception.className, 'A')
        self.assertIsNone(context.exception.baseName)
        self.assertIn("binds '__class_len__'", str(context.exception))

  def test_hook_bound_as_classmethod_passes(self) -> None:
    class A(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 3

    self.assertEqual(len(A), 3)
    self.assertIsInstance(A.__dict__['__class_len__'], classmethod)

  def test_hook_bound_to_metacall_passes(self) -> None:
    class A(BaseObject):
      __class_len__ = METACALL

    self.assertIs(A.__dict__['__class_len__'], METACALL)
    with self.assertRaises(TypeError) as context:
      len(A)
    self.assertEqual(str(context.exception), "type object 'A' has no len()")

  def test_hook_bound_to_classmethod_overloads_passes(self) -> None:
    class A(BaseObject):
      @classmethod
      @overload()
      def __class_len__(cls) -> int:
        return 4

    class B(BaseObject):
      @overload()
      @classmethod
      def __class_len__(cls) -> int:
        return 5

    for cls, expected in ((A, 4), (B, 5)):
      with self.subTest(cls=cls.__name__):
        self.assertIsInstance(cls.__dict__['__class_len__'], Dispatcher)
        self.assertIs(cls.__dict__['__class_len__'].getMethodKind(),
                      classmethod)
        self.assertEqual(len(cls), expected)

  def test_class_hook_values(self) -> None:
    def plain(cls) -> None:
      """A function that is no classmethod."""

    instanceDispatcher = Dispatcher()
    classDispatcher = Dispatcher()
    classDispatcher.setMethodKind(classmethod)
    accepted = (
      METACALL, classmethod(plain), overload(int)(classmethod(plain)),
      classDispatcher,
    )
    class Agreeing:
      def __eq__(self, other: object) -> bool:
        return True

    self.assertTrue(Agreeing() == METACALL)
    refused = (
      plain, staticmethod(plain), 3, overload(int)(plain),
      overload(int)(staticmethod(plain)), instanceDispatcher, Agreeing(),
    )
    for value in accepted:
      with self.subTest(value=str(value)):
        self.assertTrue(NamespaceHook._isClassHookValue(value))
    for value in refused:
      with self.subTest(value=str(value)):
        self.assertFalse(NamespaceHook._isClassHookValue(value))

  def test_shadowed_hook_refused(self) -> None:
    with self.assertRaises(ShadowedClassHook) as context:
      class A(metaclass=SizedMeta):
        @classmethod
        def __class_len__(cls) -> None:
          """Refused: the metaclass measures its classes itself."""

    exception = context.exception
    self.assertEqual(exception.className, 'A')
    self.assertEqual(exception.hookName, '__class_len__')
    self.assertEqual(exception.metaclassName, 'SizedMeta')
    self.assertEqual(exception.methodName, '__len__')
    self.assertIn("'SizedMeta'", str(exception))

    class B(metaclass=SizedMeta):
      @classmethod
      def __class_iter__(cls) -> iter:
        return iter(())

    self.assertEqual(len(B), 7)
    self.assertEqual(list(B), [])

  def test_chained_hook_never_shadowed(self) -> None:
    seen = []

    class A(metaclass=SizedMeta):
      @classmethod
      def __class_init__(cls, name: str, bases: tuple, space, **kw) -> None:
        seen.append(name)

    self.assertEqual(seen, ['A'])
    self.assertEqual(NamespaceHook._getChainedHooks(), ['__class_init__'])

  def test_metaclass_behind_abstract_shadows_nothing(self) -> None:
    class Both(AbstractMetaclass, LoudMeta):
      pass

    class A(metaclass=Both):
      @classmethod
      def __class_str__(cls) -> str:
        return 'hooked'

    class B(metaclass=Both):
      pass

    self.assertEqual(str(A), 'hooked')
    self.assertEqual(str(B), 'LOUD B')
    self.assertEqual(repr(B), 'LOUD B')

  def test_shadowing_helpers(self) -> None:
    space = AbstractNamespace(SizedMeta, 'A', ())
    hook = AbstractNamespace.__dict__['nameHook'].__get__(space, type(space))
    self.assertIs(hook._getShadowingMetaclass('__class_len__'), SizedMeta)
    self.assertIsNone(hook._getShadowingMetaclass('__class_iter__'))
    self.assertIsNone(hook._getShadowingMetaclass('__class_init__'))
    foreign = AbstractNamespace(type, 'A', ())
    hook = AbstractNamespace.__dict__['nameHook'].__get__(foreign,
                                                          type(foreign))
    self.assertIsNone(hook._getShadowingMetaclass('__class_len__'))
    self.assertEqual(NamespaceHook._getOperation('__class_len__'), '__len__')
    self.assertEqual(NamespaceHook._getOperation('__class_getattr__'),
                     '__getattr__')

  def test_class_dunders_listed(self) -> None:
    names = NamespaceHook._getClassDunders()
    self.assertEqual(len(names), 17)
    self.assertEqual(len(set(names)), 17)
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(name.startswith('__class_'))
        self.assertTrue(name.endswith('__'))
        self.assertIs(BaseObject.__dict__[name], METACALL)
    self.assertNotIn('__class_getitem__', names)
    self.assertNotIn('__class_eq__', names)

  def test_validation_helpers(self) -> None:
    self.assertFalse(NamespaceHook._validateName('ordinary'))
    with self.assertRaises(QuestionableSyntax) as context:
      NamespaceHook._validateName('__setname__')
    self.assertEqual(context.exception.realName, '__set_name__')
    self.assertEqual(context.exception.derpName, '__setname__')
    self.assertIn("'__set_name__'", str(context.exception))
    space = BaseSpace(BaseMeta, 'A', ())
    hook = AbstractNamespace.__dict__['nameHook'].__get__(space, BaseSpace)
    self.assertFalse(hook._validateDel())
    vouched = BaseSpace(BaseMeta, 'A', (), trustMeBro=True)
    hook = AbstractNamespace.__dict__['nameHook'].__get__(vouched, BaseSpace)
    self.assertTrue(hook._validateDel())
    self.assertFalse(hook.setItemPhase('__del__', None))

  def test_random_names_pass(self) -> None:
    space = BaseSpace(BaseMeta, 'A', ())
    hook = AbstractNamespace.__dict__['nameHook'].__get__(space, BaseSpace)
    self.randomWord.size = 8
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertFalse(hook.setItemPhase(word, 1))
        self.assertFalse(hook.setItemPhase('__%s__' % word, 1))
