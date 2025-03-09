from dataclasses import dataclass


@dataclass
class TextHandler:
    key: str
    target_message_id: int
