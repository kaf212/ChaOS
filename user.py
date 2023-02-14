from dataclasses import dataclass


@dataclass
class User:
    name: str
    password: str
    # more coming soon


def create_user_object(username, password):
    user = User(username, password)
    return user
