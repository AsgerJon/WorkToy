#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
#
# import os
# from io import TextIOWrapper, BufferedIOBase
# from unittest import TestCase
#
# from test_work_io import BaseTest
# from worktoy.attr import Field
# from worktoy.mcls import BaseObject
# from worktoy.parse import maybe
# from worktoy.static import overload
# from worktoy.text import monoSpace, stringList
#
# from worktoy.waitaminute import PathSyntaxException, TypeException, \
#   VariableNotNone
# from worktoy.work_io import FidGen
#
# try:
#   from typing import TYPE_CHECKING
# except ImportError:
#   try:
#     from typing_extensions import TYPE_CHECKING
#   except ImportError:
#     TYPE_CHECKING = False
#
# if TYPE_CHECKING:
#   from typing import Any, Optional, Union, Self, Callable, TypeAlias
#
#
# class BMP(BaseObject):
#   """
#   BMP is a class that provides a method to generate a bitmap file using
#   the FidGen class to provide the filename.
#   """
#
#   #  Fallback variables
#   __fallback_width__ = 128
#   __fallback_height__ = 128
#
#   __fallback_min_x__ = -2
#   __fallback_max_x__ = 1
#   __fallback_min_y__ = -1
#   __fallback_max_y__ = 1
#
#   #  Private variables
#   __img_width__ = None
#   __img_height__ = None
#   __math_min_x__ = None
#   __math_max_x__ = None
#   __math_min_y__ = None
#   __math_max_y__ = None
#
#   #  Public variables
#   width = Field()
#   height = Field()
#   xMin = Field()
#   xMax = Field()
#   yMin = Field()
#   yMax = Field()
#
#   fidGen = FidGen('test_fid_gen', '*.bmp', BaseTest.tempDir)
#
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   @width.GET
#   def _getWidth(self, ) -> int:
#     """
#     Returns the width of the image.
#     """
#     return maybe(self.__img_width__, self.__fallback_width__)
#
#   @height.GET
#   def _getHeight(self, ) -> int:
#     """
#     Returns the height of the image.
#     """
#     return maybe(self.__img_height__, self.__fallback_height__)
#
#   @xMin.GET
#   def _getXMin(self, ) -> float:
#     """
#     Returns the minimum x value of the image.
#     """
#     return maybe(self.__math_min_x__, self.__fallback_min_x__)
#
#   @xMax.GET
#   def _getXMax(self, ) -> float:
#     """
#     Returns the maximum x value of the image.
#     """
#     return maybe(self.__math_max_x__, self.__fallback_max_x__)
#
#   @yMin.GET
#   def _getYMin(self, ) -> float:
#     """
#     Returns the minimum y value of the image.
#     """
#     return maybe(self.__math_min_y__, self.__fallback_min_y__)
#
#   @yMax.GET
#   def _getYMax(self, ) -> float:
#     """
#     Returns the maximum y value of the image.
#     """
#     return maybe(self.__math_max_y__, self.__fallback_max_y__)
#
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   @width.SET
#   def _setWidth(self, value: int) -> None:
#     """
#     Sets the width of the image.
#     """
#     if self.__img_width__ is not None:
#       raise VariableNotNone('__img_width__', )
#     if not isinstance(value, int):
#       raise TypeException('__img_width__', value, int)
#     if value <= 0:
#       infoSpec = """'__img_width__' must be a positive integer,
#       but received: '%s'!"""
#       info = monoSpace(infoSpec % value)
#       raise ValueError(info)
#
#   @height.SET
#   def _setHeight(self, value: int) -> None:
#     """
#     Sets the height of the image.
#     """
#     if self.__img_height__ is not None:
#       raise VariableNotNone('__img_height__', )
#     if not isinstance(value, int):
#       raise TypeException('__img_height__', value, int)
#     if value <= 0:
#       infoSpec = """'__img_height__' must be a positive integer,
#       but received: '%s'!"""
#       info = monoSpace(infoSpec % value)
#       raise ValueError(info)
#
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #
#
#   @overload(int, int)
#   def __init__(self, *args, **kwargs) -> None:
#     self.width, self.height = args
#     self.__init__(**kwargs)
#
#   @overload(int)
#   def __init__(self, *args, **kwargs) -> None:
#     self.width, self.height = [*args, *args]
#     self.__init__(**kwargs)
#
#   @overload()
#   def __init__(self, **kwargs) -> None:
#     widthKeys = stringList("""width, w, imgWidth, img_w""")
#     heightKeys = stringList("""height, h, imgHeight, img_h""")
#     TYPES = dict(width=int, height=int)
#     VALUES = dict()
#     KEYS = [widthKeys, heightKeys]
#     for (keys, (name, type_)) in zip(KEYS, TYPES.items()):
#       for key in keys:
#         if key in kwargs:
#           value = kwargs[key]
#           if isinstance(value, type_):
#             VALUES[name] = value
#             break
#           raise TypeException(key, value, type_)
#     if 'width' in VALUES:
#       self.width = VALUES['width']
#     if 'height' in VALUES:
#       self.height = VALUES['height']
#
#   def pixelMap(self, horizontal: int, vertical: int) -> tuple[int, int,
#   int]:
#     """
#     The horizontal and vertical integers represent the pixel to be colored.
#     """
#     xr, yr = (horizontal + 0.5) / self.width, (vertical + 0.5) /
#     self.height
#     dx, dy = self.xMax - self.xMin, self.yMax - self.yMin
#     x = self.xMin + xr * dx
#     y = self.yMin + yr * dy
#     #  Mandelbrot iteration
#     z = x + y * 1j
#     c = x + y * 1j
#     i = 0
#     for i in range(32):
#       if abs(z) > 2:
#         break
#       z = z * z + c
#     else:
#       r = int(i * abs(z) ** 2)
#       g = int(i * z.real ** 2)
#       b = int(i * z.imag ** 2)
#       r = max(0, min(255, r))
#       g = max(0, min(255, g))
#       b = max(0, min(255, b))
#       if min(r, g, b) < 0 or max(r, g, b) > 255:
#         infoSpec = """Expected color channels to be in the range [0, 255],
#         but received: <br><tab>red: %02d<br><tab>green: %02d<br><tab>blue:
#         %02d"""
#         info = monoSpace(infoSpec % (r, g, b))
#         raise ValueError(info)
#       return r, g, b
#       #  Color mapping
#     r = int(255 * (4 - abs(z) ** 2))
#     g = int(255 * (4 - z.real ** 2))
#     b = int(255 * (4 - z.imag ** 2))
#
#     r = max(0, min(255, r))
#     g = max(0, min(255, g))
#     b = max(0, min(255, b))
#     if min(r, g, b) < 0 or max(r, g, b) > 255:
#       infoSpec = """Expected color channels to be in the range [0, 255],
#       but received: <br><tab>red: %02d<br><tab>green: %02d<br><tab>blue:
#       %02d"""
#       info = monoSpace(infoSpec % (r, g, b))
#       raise ValueError(info)
#
#     return r, g, b
#
#   def render(self, ioWrapper: BufferedIOBase) -> None:
#     """
#     Render the bitmap file using the FidGen class to provide the filename.
#     """
#     rowSize = ((self.width * 3 + 3) // 4) * 4
#     pixelArraySize = self.height * rowSize
#     fileSize = 14 + 40 + pixelArraySize
#     #  BMP header (14 bytes)
#     ioWrapper.write(b'BM')
#     ioWrapper.write(fileSize.to_bytes(4, 'little'))
#     ioWrapper.write((0).to_bytes(4, 'little'))
#     ioWrapper.write((54).to_bytes(4, 'little'))
#
#     #  DIB header (40 bytes)
#     ioWrapper.write((40).to_bytes(4, 'little'))
#     ioWrapper.write(self.width.to_bytes(4, 'little'))
#     ioWrapper.write(self.height.to_bytes(4, 'little'))
#     ioWrapper.write((1).to_bytes(2, 'little'))
#     ioWrapper.write((24).to_bytes(2, 'little'))
#     ioWrapper.write((0).to_bytes(4, 'little'))
#     ioWrapper.write(pixelArraySize.to_bytes(4, 'little'))
#     ioWrapper.write((2835).to_bytes(4, 'little'))
#     ioWrapper.write((2835).to_bytes(4, 'little'))
#     ioWrapper.write((0).to_bytes(4, 'little'))
#     ioWrapper.write((0).to_bytes(4, 'little'))
#
#     #  Pixel data
#     for y in range(self.height):
#       for x in range(self.width):
#         r, g, b = self.pixelMap(x, y)
#         ioWrapper.write(bytes([b, g, r]))
#       #  Padding
#       ioWrapper.write(b'\x00' * (rowSize - self.width * 3))
#
#   def save(self, ) -> None:
#     """
#     Render the bitmap file using the FidGen class to provide the filename.
#     """
#     ioWrapper = None
#     try:
#       ioWrapper = open(self.fidGen.filePath, 'wb')
#     except Exception as exception:
#       infoSpec = """The file at '%s' could not be created, encountering:
#       %s"""
#       info = monoSpace(infoSpec % (self.fidGen.filePath, exception))
#       raise OSError(info) from exception
#     else:
#       if TYPE_CHECKING:
#         assert isinstance(ioWrapper, TextIOWrapper)
#       self.render(ioWrapper)
#     finally:
#       ioWrapper.close()
#
#
# class TestFidGen(BaseTest):
#   """
#   TestFidGen tests the FidGen class.
#   """
#
#   def test_fid_gen(self, ) -> None:
#     """
#     Test the FidGen class.
#     """
#     mandelbrot = BMP(128, 128)
#     self.assertEqual(mandelbrot.fidGen.fileExtension, 'bmp')
#     self.assertEqual(mandelbrot.fidGen.baseName, 'test_fid_gen')
#     expectedPath = self.tempDir
#     actualPath = mandelbrot.fidGen.fileDirectory
#     self.assertEqual(expectedPath, actualPath)
#     filePath = mandelbrot.fidGen.filePath
#     #  Before saving
#     self.assertFalse(os.path.exists(filePath))
#     mandelbrot.save()
#     #  After saving
#     self.assertTrue(os.path.exists(filePath))
#     self.assertTrue(os.path.isfile(filePath))
