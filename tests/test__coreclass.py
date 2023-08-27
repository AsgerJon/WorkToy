"""Testing CoreClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from random import shuffle, choice, randint
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

import string
from types import NoneType
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

import unittest

from worktoy.core import CoreClass


class CoreClassTests(unittest.TestCase):
  """Testing CoreClass"""

  def getBaseTypes(self) -> list[type]:
    """Getter-function for base types"""
    chars = enumerate([i for i in string.ascii_uppercase])
    return [type('%s' % c, (), {'__value_id__': i}) for (i, c) in chars]

  def createInstance(self, type_: type) -> object:
    """Creates an instance of the given type"""
    out = type_()
    if hasattr(out, '__value_id__', ):
      out.__value_id__ = randint(0, 255)
    return out

  def getRandomType(self) -> type:
    """Getter-function for random type"""
    return choice(self.getBaseTypes())

  def getRandomInstance(self, ) -> object:
    """Creates an instance of the given type"""
    return self.createInstance(self.getRandomType())

  def getArgSample(self, *args) -> list:
    """Creates a list of random arguments. Provide types and integers."""
    sampleTypes = []
    sampleNumbers = []

    for arg in args:
      if isinstance(arg, type):
        sampleTypes.append(arg)
      if isinstance(arg, int):
        sampleNumbers.append(arg)
    if len(sampleNumbers) - len(sampleTypes):
      raise TypeError
    out = []
    for (n, cls) in zip(sampleNumbers, sampleTypes):
      for i in range(n):
        out.append(self.createInstance(cls))
    return out

  def getRandomKey(self, n: int = 8) -> str:
    """Creates a list of keys"""
    return choice([
      'keyLimePie',
      'jediMaster',
      'tangoMango',
      'keytastrophe',
      'quirkyKey',
      'keymeleon',
    ])

  def setUp(self):
    """Setting up each test"""

    self.core = CoreClass()
    self.testTypes = [self.getRandomType() for _ in range(16)]
    self.testInstances = [self.createInstance(t) for t in self.testTypes]
    self.testKwargs = {
      cls.__name__: obj for (cls, obj) in
      zip(self.testTypes, self.testInstances)}

  def test_maybe(self):
    """Test for the maybe method"""
    args = self.getArgSample(self.getRandomType(), 7, NoneType, 38, int, 3)
    result = self.core.maybe(*args)
    self.assertIsNotNone(result, )

    result = self.core.maybe(None, None, None)
    self.assertIsNone(result)

  def test_maybeType(self):
    """Test for the maybeType method"""
    result = self.core.maybeType(int, 'a', 'b', 1, 'c')
    self.assertEqual(result, 1)

    result = self.core.maybeType(str, 1, 2, 3)
    self.assertIsNone(result)

  def test_maybeTypes(self):
    """Test for the maybeTypes method"""
    result = self.core.maybeTypes(int, 'a', 'b', 1, 'c')
    self.assertEqual(result, [1])

    result = self.core.maybeTypes(str, 1, 2, 3)
    self.assertIsNone(result)

  def test_maybeKey(self):
    """Test for the maybeKey method"""
    result = self.core.maybeKey('key1', 'key2', key1='value1', key2='value2')
    self.assertEqual(result, 'value1')

    result = self.core.maybeKey('key1', 'key2', key2='value2')
    self.assertEqual(result, 'value2')

  def test_maybeKeys(self):
    """Test for the maybeKeys method"""
    result = self.core.maybeKeys('key1',
                                 'key2',
                                 key1='value1',
                                 key2='value2')
    self.assertEqual(result, ['value1', 'value2'])

    result = self.core.maybeKeys('key1', 'key2', key2='value2')
    self.assertEqual(result, [None, 'value2'])

  def test_empty(self):
    """Test for the empty method"""
    result = self.core.empty(None, None, None)
    self.assertTrue(result)

    result = self.core.empty(None, 1, None)
    self.assertFalse(result)

  def test_plenty(self):
    """Test for the plenty method"""
    result = self.core.plenty(1, 2, 3)
    self.assertTrue(result)

    result = self.core.plenty(1, None, 3)
    self.assertFalse(result)

  def test_pad(self):
    """Test for the pad method"""
    result = self.core.pad([1, 2, 3], [4, 5, 6])
    self.assertEqual(result, [1, 2, 3])

    result = self.core.pad([1, 2, 3], [4, 5])
    self.assertEqual(result, [1, 2, 3])

    result = self.core.pad(
      self.core.maybeTypes(int, [])
    )

  def test_parseFactory(self):
    """Test for the parseFactory method"""
    parse_func = self.core.parseFactory(int, 'key1', 'key2')
    result = parse_func(self.core, 'value1', 'value2', key1=1, key2=2)
    self.assertEqual(result, [1, 2])

    result = parse_func(self.core, 'value1', 'value2', key2=2)
    self.assertEqual(result, [None, 2])
