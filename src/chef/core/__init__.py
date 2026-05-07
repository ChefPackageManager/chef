import dataclasses

@dataclasses.dataclass
class Result:
    message: str
    error: bool