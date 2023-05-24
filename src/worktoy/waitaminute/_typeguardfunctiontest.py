"""The typeGuardFunctionTest function invokes on arguments sampled from
given types and compares result with expected return type. Please note,
that using this function will invoke the tested function. Further,
the tested function may raise an error despite receiving the correct
types. In this case, this error is returned as a warning and the result
should be considered inconclusive.
If the function behaves as expected, the function itself is returned.
Otherwise, an appropriate WrongTypeError is raised."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from random import random
from typing import Any

from icecream import ic

from worktoy.core import CallMeMaybe, empty, plenty, maybeType, TypeBag
from worktoy.waitaminute import typeGuard, UnexpectedStateError, \
  TypeGuardError
from worktoy.waitaminute import valueGuard

Numerical = TypeBag(int, float, complex)

ic.configureOutput(includeContext=True)


def typeGuardFunctionTest(
    func: CallMeMaybe, invArgs: Any, expRes: type = None) -> CallMeMaybe:
  """The typeGuardFunctionTest function invokes on arguments sampled from
  given types and compares result with expected return type. Please note,
  that using this function will invoke the tested function. Further,
  the tested function may raise an error despite receiving the correct
  types. In this case, this error is returned as a warning and the result
  should be considered inconclusive.
  If the function behaves as expected, the function itself is returned.
  Otherwise, an appropriate WrongTypeError is raised.
  Invoking this test function has the following signature:

    typeGuardFunctionTest(func, invArgs, expRes)
    :param func: This is the function being tested
    :param invArgs: This describes how the tested functions is called
    :param expRes: This describes the expected results
    :return: If the function passes the test, the function itself is
    returned. Otherwise, a WrongTypeError is raised.

  The function is invoked on some positional arguments of a value and
  type, each represented as an entry in the invArgs. All entries are
  parsed to the following schema:
    {'type': str, 'value': 'a string'}
  Such can be included directly as an entry in the list or sample may be
  provided, which is then parsed, for example:
    entry = 777
    {'type': int, 'value': 777}
  If the entry is a numerical type, a random number of that type will be
  used, for example:
    entry = complex
    {'type': complex, 'value': 7 + 7 * 1j}
  For other types, the recommendation is to choose a sample manually and
  let the function infer the type.
  If the entry is a type with the following intention, a manual scheme is
  required:
    entry = str
    {'type': type, 'value': str}
  The function will not infer that schema when encountering a type.
  """
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence
  if not isinstance(invArgs, list):
    return typeGuardFunctionTest(func, [invArgs], expRes)
  typeGuard(invArgs, list)
  if expRes is not None:
    typeGuard(expRes, type)
  else:
    expRes = type(None)
  if expRes in Numerical:
    expRes = Numerical
  else:
    expRes = TypeBag(expRes)

  realArgs = []
  for arg in invArgs:
    entry = {'type_': None, 'value': None, }
    if isinstance(arg, dict):
      type_ = arg.get('type', None)
      value = arg.get('value', None)
      if empty(type_, value):
        entry = {'type_': dict, 'value': {}, }
      if plenty(type_, value):
        if not isinstance(type_, type):
          type_ = type(value)
        else:
          if type_ in Numerical:
            type_ = Numerical
          if not isinstance(value, type_):
            msg = """Given value %s is not an instance of given type: %s. 
            Instead, the type of value is: %s!"""
            from worktoy.stringtools import justify
            raise TypeError(justify(msg % (value, type_, type(value))))
          entry = {'type_': type_, 'value': value, }
      if type_ is None:
        entry = {'type_': type(value), 'value': value}
      if value is None:
        if type_ is str:
          value = 'random string'
          entry = {'type_': type_, 'value': value}
        if type_ in [int, complex, float]:
          value = _sampleNumerical(type_)
          entry = {'type_': type_, 'value': value}
        if type_ is dict:
          entry = {'type_': dict, 'value': {}, }
        if type_ is list:
          entry = {'type_': list, 'value': [], }
        if type_ is tuple:
          entry = {'type_': tuple, 'value': (), }
        if type_.__module__ != 'builtins':
          entry = {'type_': type_, 'value': type_(), }
    if isinstance(arg, (list or tuple)):
      arg = [*arg, None]
      type_ = maybeType(type, *arg)
      if type_ is not None:
        if isinstance(type_, type):
          value = maybeType(type_, *arg)
          if value is not None:
            entry = {'type_': type_, 'value': value, }
    if isinstance(arg, type):
      if arg in [int, float, complex]:
        entry = {'type_': arg, 'value': _sampleNumerical(arg)}
      if arg in [dict, list, tuple, set]:
        typeName = arg.__name__
        containers = {'dict': dict(), 'list': [], 'tuple': (), 'set': {}}
        value = containers.get(typeName, None)
        entry = {'type_': arg, 'value': value}
      if callable(arg) and empty([v for v in entry.values()]):
        f = getattr(arg, '__call__', None)
        if f is not None and callable(f):
          try:
            instance = f()
          except TypeError as e:
            from worktoy.stringtools import justify
            m = """Whatever %s is, don't call! When trying to create 
            an instance of %s by calling it, %s was encountered!"""
            msg = justify(m % (arg, arg, e))
            raise TypeError(msg)
          except AttributeError as e:
            from worktoy.stringtools import justify
            m = """Callables requiring arguments are not supported! When 
            trying to instantiate %s, %s was encountered!"""
            raise AttributeError(justify(m % (arg, e)))
          except Exception as e:
            from worktoy.stringtools import justify
            msg = """When attempting to instantiate %s, %s was 
            encountered!""" % (arg, e)
            raise Exception(justify(msg))
          entry = {'type_': arg, 'value': instance}
      if empty([v for v in entry.values()]):
        raise ValueError('Unrecognized type: %s' % arg)
    if isinstance(arg, (int, float, complex)):
      entry = {'type_': type(arg), 'value': arg}
    if empty([v for v in entry.values()]):
      raise NotImplementedError()
    realArgs.append(entry)
  args = [entry['value'] for entry in realArgs]
  testRes = func(*args)
  if expRes is float:
    expRes = Numerical
  if expRes is None and testRes is None:
    return func
  if not isinstance(testRes, expRes):
    try:
      raise TypeGuardError(testRes, expRes)
    except Exception as e:
      raise e
  return func


def _sampleNumerical(type_: type) -> Numerical:
  """Returns a numerical sample of the type indicated"""
  typeGuard(type_, type)
  valueGuard(type_, lambda item: item in [int, float, complex])
  if type_ is complex:
    return _sampleNumerical(float) + _sampleNumerical(float) * 1j
  if type_ is int:
    return int(round(_sampleNumerical(float) * (2 ** 16 - 1)))
  if type_ is float:
    return random()
  raise UnexpectedStateError(type_)
