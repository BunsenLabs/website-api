from dataclasses import dataclass, field

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
    if (self.verb == "PUT" or self.verb == "CLEAR"):
      if not isinstance(self.payload, dict):
        raise ValueError("Verb PUT requires Dict as payload")
      if not "endpoint" in self.payload:
        raise ValueError("Missing <endpoint> key from payload")
