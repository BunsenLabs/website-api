from blwwwapi import __SCHEMAPATH__
from cerberus import Validator
from dataclasses import dataclass, field
import os
import yaml

SCHEMA = {}

for obj in os.scandir(__SCHEMAPATH__):
  if obj.is_file():
    with open(obj.path, "r") as FILE:
      verb = obj.name.split(".")[0]
      SCHEMA[verb] = yaml.safe_load(FILE)

@dataclass(frozen=True)
class Message:
  sender: str
  verb: str
  payload: dict = field(default_factory=dict)

  __verbs = [ "PUT", "CLEAR" ]

  def __post_init__(self):
    self.__validate()

  def __validate(self):
    if not isinstance(self.sender, str):
      raise ValueError("Sender must be a string")

    if len(self.sender)==0:
      raise Value("Sender must not be a zero-length string")

    if not self.verb in self.__verbs:
      raise ValueError(f"Unknown value for attribute <verb>: {self.verb}")

    v = Validator(SCHEMA[verb])
    if not v.validate(self.payload):
      raise ValueError(f"Schema validation failed: {self}")
