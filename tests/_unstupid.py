"""Let's unstupid some tests!"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def testExtractSingleArg(self):
  """Test extracting a single argument."""
  # Arrange
  myType: Type[int] = int
  myKeys: Tuple[str] = 'arg'
  args: Tuple[int] = (10,)
  kwargs: dict[str, Any] = {}

  expectedResult = (10, [], {})
  appliedInput = 'extractArg(%s, %s, %s, %s)' % (
    myType, myKeys, args, kwargs)
  actualResult = extractArg(myType, myKeys, *args, **kwargs)
  if expectedResult != actualResult:
    print('testExtractSingleArg')
    print(appliedInput)
    print(expectedResult)
    print(actualResult)
    raise PythonLogicError()
  self.assertEqual(actualResult, expectedResult)
