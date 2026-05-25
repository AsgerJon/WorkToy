"""
SubTest subclasses 'unittest.TestCase' and provides a per-instance
accumulator for sub-tests. 'BaseTest' embeds one as the 'subTest'
descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest import TestCase

from ..desc import Field
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional, TypeAlias, Type, Self
  from . import BaseTest

  TestType: TypeAlias = Type[BaseTest]
  TestRun: TypeAlias = Optional[BaseTest]


class SubTest(TestCase):
  """
  SubTest subclasses 'unittest.TestCase' (for its assertion methods),
  not 'BaseTest'. It is a per-instance accumulator and context manager:
  'BaseTest' hosts it as the 'subTest' descriptor, '__get__' lazily
  builds one per instance, and using it as a context manager records
  each block as passed, failed (AssertionError), or errored (any other
  Exception). 'BaseTest.tearDown' then fails the test if any sub-test
  failed or errored. It is not itself a runnable, discovered test class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __private_name__: str = '__sub_test__'

  #  Fallback Variables
  __fallback_current__: str = '<sub test>'

  #  Private Variables
  __field_name__: Optional[str] = None  # should be '_subTest'
  __field_owner__: Optional[Type[BaseTest]] = None  # should be 'BaseTest'
  __current_tests__: Optional[tuple[str, ...]] = None
  __test_fails__: Optional[tuple[AssertionError, ...]] = None
  __test_errors__: Optional[tuple[Exception, ...]] = None
  __test_passed__: Optional[tuple[str, ...]] = None
  __owning_test__: Optional[Type[BaseTest]] = None
  __owning_instance__: Optional[BaseTest] = None

  #  Public Variables
  fails: Field[tuple[AssertionError, ...]] = Field()
  errors: Field[tuple[Exception, ...]] = Field()
  passed: Field[tuple[str, ...]] = Field()
  current: Field[str] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createFails(self) -> None:
    self.__test_fails__ = ()

  @fails.GET
  def _getFails(self, **kwargs) -> tuple[AssertionError, ...]:
    if self.__test_fails__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createFails()
      return self._getFails(_recursion=True)
    if isinstance(self.__test_fails__, tuple):
      for fail in self.__test_fails__:
        if not isinstance(fail, AssertionError):
          break
      else:
        return self.__test_fails__
      raise TypeException('fail', fail, AssertionError)
    raise TypeException('__test_fails__', self.__test_fails__, tuple)

  def _createErrors(self) -> None:
    self.__test_errors__ = ()

  @errors.GET
  def _getErrors(self, **kwargs) -> tuple[Exception, ...]:
    if self.__test_errors__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createErrors()
      return self._getErrors(_recursion=True)
    if isinstance(self.__test_errors__, tuple):
      for error in self.__test_errors__:
        if not isinstance(error, Exception):
          break
      else:
        return self.__test_errors__
      raise TypeException('error', error, Exception)
    raise TypeException('__test_errors__', self.__test_errors__, tuple)

  def _createPassed(self) -> None:
    self.__test_passed__ = ()

  @passed.GET
  def _getPassed(self, **kwargs) -> tuple[str, ...]:
    if self.__test_passed__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createPassed()
      return self._getPassed(_recursion=True)
    if isinstance(self.__test_passed__, tuple):
      for passed in self.__test_passed__:
        if not isinstance(passed, str):
          break
      else:
        return self.__test_passed__
      raise TypeException('passed', passed, str)
    raise TypeException('__test_passed__', self.__test_passed__, tuple)

  def _popCurrent(self, ) -> None:
    if self.__current_tests__ is None:
      raise RuntimeError
    if len(self.__current_tests__) == 1:
      self.__current_tests__ = None
    else:
      self.__current_tests__ = self.__current_tests__[:-1]

  @current.GET
  def _getCurrent(self, ) -> str:
    if self.__current_tests__ is None:
      return self.__fallback_current__
    return str.join(' -> ', self.__current_tests__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addFail(self, fail: AssertionError) -> None:
    self.__test_fails__ = (*self.fails, fail)

  def _addError(self, error: Exception) -> None:
    self.__test_errors__ = (*self.errors, error)

  def _addPassed(self, passed: str) -> None:
    self.__test_passed__ = (*self.passed, passed)

  @current.SET
  def _setCurrent(self, value: str, ) -> None:
    if not isinstance(value, str):
      raise TypeException('current', value, str)
    if self.__current_tests__ is None:
      self.__current_tests__ = (value,)
    else:
      self.__current_tests__ = (*self.__current_tests__, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: TestType, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: TestRun, owner: TestType, **kwargs) -> Any:
    if instance is None:
      return self
    cls = type(self)
    try:
      sub = getattr(instance, self.__private_name__)
    except AttributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      sub = cls()
      sub.__field_name__ = self.__private_name__
      sub.__field_owner__ = owner
      sub.__owning_instance__ = instance
      sub.__owning_test__ = owner
      setattr(instance, self.__private_name__, sub)
      return self.__get__(instance, owner, _recursion=True)
    else:
      if isinstance(sub, cls):
        return sub
      raise TypeException(self.__private_name__, sub, cls)

  def __call__(self, *args, **kwargs) -> Self:
    argStr = str.join(', ', (str(arg) for arg in args))
    kwargStr = str.join(', ', ('%s=%s' % (k, v) for k, v in kwargs.items()))
    info = str.join(', ', (a for a in (argStr, kwargStr) if a))
    self.current = info
    return self

  def __enter__(self, ) -> Self:
    return self

  def __exit__(self, _, exception: BaseException, __) -> bool:
    try:
      if exception is None:
        self._addPassed(self.current)
        return True
      if isinstance(exception, AssertionError):
        self._addFail(exception)
        return True
      if isinstance(exception, Exception):
        self._addError(exception)
        return True
      raise exception
    finally:
      self._popCurrent()

  def __bool__(self, ) -> bool:
    return True if self.fails or self.errors else False

  def __repr__(self, ) -> str:
    """
    Framed status report. Self-indulgent ASCII art and proud of it.
    """
    owner = self.__owning_test__
    if owner is not None:
      ownerName = owner.__name__
    else:
      ownerName = getattr(self, '_testMethodName', '<unbound>')
    nPass = len(self.passed)
    nFail = len(self.fails)
    nErr = len(self.errors)
    if nFail or nErr:
      status = 'FAILED'
      glyph = 'x'
    elif nPass:
      status = 'PASSED'
      glyph = '+'
    else:
      status = 'IDLE'
      glyph = '.'

    if self.__current_tests__ is None:
      active = '<none>'
    else:
      active = self.current

    width = 64
    inner = width - 4

    def row(text: str) -> str:
      """Pad or truncate to one inner-width row."""
      if len(text) > inner:
        text = '%s...' % text[:inner - 3]
      return '| %s |' % text.ljust(inner)

    top = '+%s+' % ('=' * (width - 2))
    mid = '+%s+' % ('=' * (width - 2))
    thin = '+%s+' % ('-' * (width - 2))
    bot = '+%s+' % ('=' * (width - 2))

    className = type(self).__name__
    title = '%s  %s  %s   %s' % (glyph, className, glyph, ownerName)
    totals = '%d passed   %d failed   %d errored' % (nPass, nFail, nErr)

    lines = [top, row(title.center(inner)), mid]
    lines.append(row('status   :  %s' % status))
    lines.append(row('active   :  %s' % active))
    lines.append(row('totals   :  %s' % totals))

    if self.passed:
      lines.append(thin)
      lines.append(row('passes:'))
      for tag in self.passed[:8]:
        lines.append(row('   +  %s' % tag))
      if len(self.passed) > 8:
        extra = len(self.passed) - 8
        lines.append(row('   .. and %d more' % extra))

    if self.fails:
      lines.append(thin)
      lines.append(row('fails:'))
      for fail in self.fails[:8]:
        lines.append(row('   x  %s' % fail))
      if len(self.fails) > 8:
        extra = len(self.fails) - 8
        lines.append(row('   .. and %d more' % extra))

    if self.errors:
      lines.append(thin)
      lines.append(row('errors:'))
      for error in self.errors[:8]:
        lines.append(row('   !  %r' % error))
      if len(self.errors) > 8:
        extra = len(self.errors) - 8
        lines.append(row('   .. and %d more' % extra))

    lines.append(bot)
    return str.join('\n', lines)

  __str__ = __repr__
