"""External script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
there = os.path.join(here, 'src')
print(there)
sys.path.append(there)

if __name__ == '__main__':
  from main_tester_class_02 import Talker

  talker = Talker()
  talker.talk('Hello, world!', )
