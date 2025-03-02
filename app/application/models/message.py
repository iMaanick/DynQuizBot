from pydantic import BaseModel


class Button(BaseModel):
    text: str
    target_message_id: int

    def to_dict(self) -> dict:
        return self.model_dump()


class TextHandler(BaseModel):
    key: str
    target_message_id: int


class Message(BaseModel):
    message_id: int
    text: str
    command: str | None = None
    buttons: list[Button] = []
    button_width: int | None = None
    input_handler: TextHandler | None = None
