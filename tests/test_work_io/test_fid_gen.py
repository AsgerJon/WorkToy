"""
TestFidGen tests the FidGen class and its functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import os

from . import WorkIOTest
from worktoy.waitaminute import TypeException
from worktoy.work_io import FidGen, validateExistingFile

if TYPE_CHECKING:  # pragma: no cover
  pass

here_ = os.path.abspath(os.path.dirname(__file__))


class FooBar:
  """
  FooBar is a simple class used for testing purposes.
  """
  fidGen = FidGen(dir=here_, ext='tmp', name='t3st')


class TestFidGen(WorkIOTest):
  """
  TestFidGen tests the FidGen class and its functionality. Since this
  class is not used by the rest of the code, the test will explicitly test
  it thoroughly.

  FidGen is a class that generates file names based on a format
  specification and a particular directory. The specification must contain
  space for an integer. The lowest integer resulting in a path not already
  occupied is return by the 'nextName' property.
  """

  @staticmethod
  def touch(filePath: str, ) -> None:
    """
    This static methods  creates an empty file at the given path.
    """
    f = None
    try:
      f = open(filePath, 'w')
    except Exception as exception:
      raise exception
    else:
      f.write('\n')
      f.close()
    finally:
      if hasattr(f, 'close'):  # pragma: no cover
        f.close()  # pragma: no cover

  @staticmethod
  def yeet(filePath: str, ) -> None:
    """
    This static method deletes the file at the given path.
    """
    if validateExistingFile(filePath, strict=False):
      os.remove(filePath)

  def test_base(self) -> None:
    """
    Test the basic functionality of FidGen.
    """
    iniName = FooBar.fidGen.nextName
    self.touch(FooBar.fidGen.nextName)
    iniName2 = FooBar.fidGen.nextName
    self.assertNotEqual(iniName, iniName2)

  def test_touch(self) -> None:
    """
    Covering the touch defined here
    """
    with self.assertRaises(Exception):
      self.touch('')

  def tearDown(self) -> None:
    """
    Tear down the test by deleting the file created during the test.
    """
    for name in FooBar.fidGen._getGeneratedNames():
      try:
        validateExistingFile(name)
      except FileNotFoundError:
        continue
      else:
        self.yeet(name)

  def test_recursion(self) -> None:
    """
    Test the recursion of FidGen.
    """

    class Foo:
      fidGen = FidGen(dir=here_, ext='tmp', name='t3st')

    with self.assertRaises(RecursionError) as context:
      Foo.fidGen._getFileSpec(_recursion=True)

    foo = Foo()
    setattr(foo.fidGen, '__file_spec__', 69420)

    with self.assertRaises(TypeException) as context:
      foo.fidGen._getFileSpec()

  def test_recursion2(self) -> None:
    """
    Test the recursion of FidGen with a different class.
    """

    class Bar:
      fidGen = FidGen(dir=here_, ext='tmp', name='t3st')

    bar = Bar()
    filePath = bar.fidGen.fileSpec % 100
    try:
      self.touch(filePath)
      with self.assertRaises(RecursionError) as context:
        bar.fidGen._getNextName(100)
    finally:
      self.yeet(filePath)

  def test_next_name(self) -> None:
    """
    Test the nextName property of FidGen.
    """
    for i in range(5):
      name = FooBar.fidGen.nextName
      self.touch(name)
    for file in FooBar.fidGen._getGeneratedNames():
      self.yeet(file)

  def test_good_set_ext_field(self) -> None:
    """
    Test the fileExtension field of FidGen.
    """
    FooBar.fidGen.fileExtension = 'txt'

  def test_bad_type_set_ext_field(self) -> None:
    """
    Test the fileExtension field of FidGen with a bad value.
    """
    with self.assertRaises(TypeException) as context:
      FooBar.fidGen.fileExtension = 69420
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, '__file_extension__')
    self.assertEqual(e.actualObject, 69420)
    self.assertEqual(e.actualType, int)
    self.assertEqual(e.expectedTypes, (str,))

  def test_bad_value_set_ext_field(self) -> None:
    """
    Test the fileExtension field of FidGen with a bad value.
    """
    with self.assertRaises(ValueError) as context:
      FooBar.fidGen.fileExtension = ''
    e = context.exception
    expected = """__file_extension__ must be a non-empty string"""
    self.assertIn(expected, str(e))

  def test_init(self) -> None:
    """
    Test the initialization of FidGen with a file name.
    """

    class Foo:
      """
      Testing different init calls for FidGen.
      """
      fid0 = FidGen()
      fidStr = FidGen('breh', )
      fidStrKwarg = FidGen('breh', lmao=True)
      fidStr2 = FidGen('breh', '*.txt', lmao=True)
      fidStr3 = FidGen('breh', '*.txt', here_, lmao=True)
      fidKwarg3 = FidGen(name='breh', )

    self.assertEqual(Foo.fid0.nextName, Foo.fidKwarg3.nextName)
    self.assertIn('breh', Foo.fidStr.nextName)
    self.assertEqual(Foo.fidStr2.fileExtension, 'txt')
    self.assertEqual(Foo.fidStr3.fileDirectory, here_)

  def test_find(self) -> None:
    """
    Test the _findDirectory and _findFileExtension methods of FidGen.
    """
    foo, bar = FidGen._findDirectory('breh', 69, 420, )
    self.assertIsNone(foo)
    self.assertEqual(bar, ('breh', 69, 420,))
    foo, bar = FidGen._findFileExtension('breh', 69, 420, )
    self.assertIsNone(foo)
    self.assertEqual(bar, ('breh', 69, 420,))

  def test_common_file_extension(self) -> None:
    """
    Test the common file extension of FidGen.
    """
    foo, bar = FidGen._findFileExtension('breh', 69, 420, 'mp4')
    self.assertEqual(foo, 'mp4')
