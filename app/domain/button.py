from dataclasses import dataclass


@dataclass
class Button:
    text: str
    target_message_id: int

    def to_dict(self) -> dict:
        return {"text": self.text, "target_message_id": self.target_message_id}
