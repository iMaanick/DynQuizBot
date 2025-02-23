from dataclasses import dataclass, field


@dataclass
class Button:
    text: str
    target_message_id: int


@dataclass
class TextHandler:
    key: str
    target_message_id: int


@dataclass
class Message:
    message_id: int
    text: str
    command: str | None = None
    buttons: list[Button] = field(default_factory=list)
    input_handler: TextHandler | None = None


class Messages:
    def __init__(self, message_data: dict[int, Message]):
        self.messages = message_data

    def get_message(self, message_id: int) -> Message:
        print(self.messages.keys())
        return self.messages[message_id]
