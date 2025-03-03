from aiogram.types import User


class UserSet:
    def __init__(self):
        self._users = set()

    def add(self, user: User) -> None:
        self._users.add(user)

    def remove(self, user: User) -> None:
        self._users.discard(user)

    def get_all_users(self) -> set[User]:
        return self._users.copy()
