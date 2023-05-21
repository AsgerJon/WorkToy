"""
Code Analysis

Objective:
The objective of the searchTerm function is to search a given text for all
instances of a given term and return their indices.

Inputs:
- text: a string representing the text to be searched
- term: a string representing the term to be searched for in the text

Flow:
- Check if the term is not an empty string, if it is, raise a ValueError
- Initialize an empty list called out
- If the text is an empty string, return the empty list out
- Get the length of the term and initialize a counter variable c to 0
- While the sum of c and the length of the term is less than the length of
the text, do the following:
  - Get a substring of the text starting from index c and with length n (
  the length of the term)
  - If the substring is equal to the term, append a list of the starting
  and ending indices of the term in the text to the out list and increment
  c by n
  - If the substring is not equal to the term, increment c by 1
- Sort the out list and return it

Outputs:
- A list of lists, where each inner list contains two integers
representing the starting and ending indices of a term in the text

Additional aspects:
- The function uses the sorted() function to sort the out list before
returning it
- The function raises a ValueError if the term is an empty string
- The function returns an empty list if the text is an empty string"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
import unittest

from worktoy import searchTerm


class TestSearchterm(unittest.TestCase):
  #  Tests that the function correctly returns the index of a term found
  #  once in the text. Tags: [happy path]
  def test_termFoundOnce(self):
    text = "The quick brown fox jumps over the lazy dog."
    term = "quick"
    expected_output = [[4, 9]]
    self.assertEqual(searchTerm(text, term), expected_output)

  #  Tests that the function correctly returns the indices of a term found
  #  multiple times in the text. Tags: [happy path]
  def test_termFoundMultiple(self):
    text = "She sells seashells by the seashore."
    term = "se"
    expected_output = [[4, 6], [10, 12], [27, 29]]
    self.assertEqual(searchTerm(text, term), expected_output)

  #  Tests that the function raises a ValueError when the term is an empty
  #  string and returns an empty list when the text is an empty string.
  #  Tags: [edge case]
  def test_emptyString(self):
    with self.assertRaises(ValueError):
      searchTerm("The quick brown fox jumps over the lazy dog.", "")
    self.assertEqual(searchTerm("", "quick"), [])

  #  Tests that the function returns an empty list when the term is not
  #  found in the text. Tags: [edge case]
  def test_termNotFound(self):
    text = "The quick brown fox jumps over the lazy dog."
    term = "cat"
    self.assertEqual(searchTerm(text, term), [])

  #  Tests that the function correctly returns the index of a term found
  #  at the beginning of the text. Tags: [happy path]
  def test_termFoundAtBeginning(self):
    text = "The quick brown fox jumps over the lazy dog."
    term = "The"
    expected_output = [[0, 3]]
    self.assertEqual(searchTerm(text, term), expected_output)
