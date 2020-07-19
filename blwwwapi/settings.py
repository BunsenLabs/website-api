from typing import List

from pydantic import (
  BaseSettings,
  AnyHttpUrl,
  IPvAnyAddress,
  validator,
)

class Settings(BaseSettings):
  BIND_IP: IPvAnyAddress = "127.0.0.1"
  BIND_PORT: int = 10000
  FORUM_URL: AnyHttpUrl = "https://forums.bunsenlabs.org"
  TRACKER_URL: AnyHttpUrl = "http://127.0.0.1:6969"
  NEWS_UPDATE_INTERVAL: int = 900
  TRACKER_UPDATE_INTERVAL: int = 5
  WORKERS: List[str] = [ "feed" ]

  @validator("BIND_PORT")
  def is_tcp_port(cls, port):
    assert 1 <= port <= 65535
