"""n00bGuards - Who are you gonna call!?"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import time

from icecream import ic

ic.configureOutput(includeContext=True)

here = os.path.abspath(__file__)
dirName = os.path.dirname(here)
fileNameBanner = 'nooberror.txt'
fileNameLyrics = 'lyrics.txt'
fidBanner = os.path.join(dirName, fileNameBanner)
fidLyrics = os.path.join(dirName, fileNameLyrics)

with open(fidBanner, 'r', encoding='utf-8') as f:
  bannerMsg = f.read()

with open(fidLyrics, 'r', encoding='utf-8') as f:
  lyricsMsg = f.read().split('\n')


class n00bError(Exception):
  """n00bGuards - Who are you gonna call!?
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, message="Importing * is not allowed!"):
    """n00bGuards - Who are you gonna call!?
    #  Copyright (c) 2023 Asger Jon Vistisen
    #  MIT Licence"""
    super().__init__(message)

  def __str__(self) -> str:
    """n00bGuards - Who are you gonna call!?
    #  Copyright (c) 2023 Asger Jon Vistisen
    #  MIT Licence"""
    print(bannerMsg)
    time.sleep(5)
    for line in lyricsMsg:
      time.sleep(0.5)
      print(line)
    return '%s\n%s' % ('\n'.join(lyricsMsg), bannerMsg,)
