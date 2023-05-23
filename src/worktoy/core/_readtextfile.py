"""The readTextFile function provides functionality for reading text files
along with comprehensive error handling"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations


def readTextFile(file_path: str) -> str:
  """The readTextFile function provides functionality for reading text files
  along with comprehensive error handling
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
  try:
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    except FileNotFoundError as noFile:
      print('Unable to locate file!')
      raise noFile
    except PermissionError as noAccess:
      print('Access to file denied!')
      raise noAccess
    except IsADirectoryError as isDir:
      print('The path: %s specifies a directory, not a file!' % file_path)
      raise isDir
    except UnicodeDecodeError as decodeError:
      print('While reading the file encountered decoding error!')
      raise decodeError
    except IOError as other:
      print('Encountered general input/output error!')
      raise other
    return content
  except Exception as e:
    print('Failed during read file')
    raise e
