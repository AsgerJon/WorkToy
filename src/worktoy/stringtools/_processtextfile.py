"""The processTextFile function updates a text file with the process
defined by string to string mapping function."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import re
import shutil
import os

from worktoy.core import CallMeMaybe, readTextFile
from worktoy.waitaminute import typeGuard, typeGuardFunction


def apply_function_to_file(file_path, function: CallMeMaybe):
  """
  Reads the content of a text file, applies the given function to the
  content,
  and replaces the original content with the modified content. It also
  creates
  a backup of the original file with "_backup" appended to its file name
  before
  the file extension, and increments the number if the backup file already
  exists.

  Args:
      file_path (str): The path to the text file.
      function (callable): A function that takes a string and returns a
      string.

  Returns:
      bool: True if the file processing was successful, False otherwise.
  """
  typeGuardFunction(function, str, str)
  typeGuard(function, CallMeMaybe)
  typeGuard(function('sample-str'), str)
  typeGuard(file_path, str)
  content = readTextFile(file_path)
  try:  # Create a backup of the original file
    backupResult = create_backup_file(file_path)
    if isinstance(backupResult, Exception):
      raise backupResult
    else:
      # Apply the function to the content
      modified_content = function(content)
      # Write the modified content back to the file
      with open(file_path, 'w') as file:
        file.write(modified_content)
      return True
      # print('When trying to create backup of the file, encountered:')
  except IOError:
    # Handle file-related errors
    print(f"Error: Failed to process file '{file_path}'")

  # Restore the original file if an error occurred
  restore_original_file(file_path, get_unique_backup_file_path(file_path))
  return False


def create_backup_file(file_path) -> bool | Exception:
  """
  Creates a backup file with "_backup" appended to its file name before
  the file extension.
  If the backup file already exists, it increments the number until a
  unique name is found.

  Args:
      file_path (str): The path to the original file.

  Returns:
      str: The path to the backup file if successfully created,
      None otherwise.
  """
  try:
    shutil.copy2(file_path,
                 get_unique_backup_file_path(file_path))  # Create a copy
    # of the original file
    return True

  except IOError as e:
    # Handle file-related errors
    print(f"Error: Failed to create backup file for '{file_path}'")
    return e


def get_unique_backup_file_path(file_path):
  """
  Generates a unique backup file path by appending "_backup" or "_backupN"
  to the file name.
  If the backup file already exists, it increments the number until a
  unique name is found.

  Args:
      file_path (str): The path to the original file.

  Returns:
      str: The backup file path.
  """
  backup_file_name = os.path.basename(file_path)
  backup_file_dir = os.path.dirname(file_path)
  backup_file_base, backup_file_ext = os.path.splitext(backup_file_name)
  backup_file_path = os.path.join(backup_file_dir,
                                  backup_file_base + "_backup" +
                                  backup_file_ext)

  index = 1
  while os.path.exists(backup_file_path):
    backup_file_path = os.path.join(backup_file_dir,
                                    backup_file_base + f"_backup{index}" +
                                    backup_file_ext)
    index += 1

  return backup_file_path


def restore_original_file(file_path, backup_file_path):
  """
  Restores the original file from the backup file.

  Args:
      file_path (str): The path to the original file.
      backup_file_path (str): The path to the backup file.
  """
  if backup_file_path:
    try:
      shutil.move(backup_file_path, file_path)  # Restore the original file

    except IOError:
      # Handle file-related errors
      print(f"Error: Failed to restore original file for '{file_path}'")
