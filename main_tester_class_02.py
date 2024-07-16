"""External script class"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

from worktoy.parse import maybe


class Talker:
  """Talker class pokes at the server"""

  def __init__(self, *args, **kwargs) -> None:
    self.clientSocket = socket(AF_INET, SOCK_STREAM)
    self.clientSocket.connect(('localhost', 8080))

  def talk(self, *args) -> None:
    """LMAO"""
    msg, num = None, None
    for arg in args:
      if isinstance(arg, str) and msg is None:
        msg = arg
      if isinstance(arg, int) and num is None:
        num = arg
      if msg is not None and num is not None:
        break
    msg = maybe(msg, 'Hello, world!')
    num = maybe(num, -1) + 1
    data = '%s - %04d' % (msg, num)
    data = data.encode('utf-8')
    print(data)
    self.clientSocket.sendall(data)
    sleep(1)
    return self.talk(msg, num)
