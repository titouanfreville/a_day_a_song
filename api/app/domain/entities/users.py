from _base import Entity


class User(Entity):
    id: str = ""
    name: str
    email: str
    password: str
    email_verified: bool = False
