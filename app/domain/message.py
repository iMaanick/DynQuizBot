from dataclasses import dataclass, field


@dataclass
class Button:
    text: str
    target_message_id: int

    def to_dict(self) -> dict:
        return {"text": self.text, "target_message_id": self.target_message_id}


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
    button_width: int | None = None
    input_handler: TextHandler | None = None


class Messages:
    def __init__(self, message_data: dict[int, Message]) -> None:
        self.messages = message_data
        self.command_to_message: dict[str, Message] = {
            msg.command: msg for msg in message_data.values() if msg.command
        }

    def update(self, messages: list[Message]) -> None:
        message_data: dict[int, Message] = {}
        command_to_message: dict[str, Message] = {}

        for message in messages:
            message_data[message.message_id] = message
            if message.command:
                command_to_message[message.command] = message

        self.messages = message_data
        self.command_to_message = command_to_message

    def get_message(self, message_id: int) -> Message:
        print(self.messages.keys())
        return self.messages[message_id]

    def get_start_message(self) -> Message | None:
        for message in self.messages.values():
            if message.command == "start":
                return message
        return None
