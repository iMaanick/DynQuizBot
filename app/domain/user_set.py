from aiogram.types import User


class UserSet:
    def __init__(self):
        self._user_ids = set()

    def add(self, user: User) -> None:
        self._user_ids.add(user.id)

    def remove(self, user: User) -> None:
        self._user_ids.discard(user.id)

    def get_all_user_id(self) -> set[int]:
        return self._user_ids.copy()
