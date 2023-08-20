"""The monoSpace transfers a string to have new lines at <br> or at a
customized newLine indicator. Python strings defined with triple quotes
across multiple line receive what seems like arbitrarily placed new-line
characters. This function removes these new-line characters."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def monoSpace(text: str, newLine: str = None, ) -> str:
  """Removes the stupid new lines symbols placed inside the triple
  quotes."""
  newLine = '<br>' if newLine is None else newLine
  text = text.replace('\n', ' ').replace('\r', ' ')
  text = text.replace(newLine, '\n')
  while '  ' in text:
    text = text.replace('  ', ' ')
  return text
