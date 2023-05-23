"""The wordForWord function takes string and a string to string functions
as its arguments. It splits the string into words, and returns a new
string where every string is replaced by the function return value on that
string."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from re import Match, sub


def wordForWord(inputString, function):
  """Applies a given string-to-string function to each word in the input
  string.
  Args:
      inputString (str): The input string.
      function (callable): A function that takes a string and returns a
      string.
  Returns:
      str: The modified string with the function applied to each word."""
  wordPattern = r"\b\w+\b"  # Regex pattern to match words

  def replaceWord(match: Match) -> str:
    """Apply the function to the matched word"""
    return function(match.group(0))

  # Use regex to find and replace words using the function
  modifiedString = sub(wordPattern, replaceWord, inputString)

  return modifiedString
