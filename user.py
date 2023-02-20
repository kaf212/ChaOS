from dataclasses import dataclass


@dataclass
class User:
    name: str
    password: str
    account_type: str
    # more coming soon


def create_user_object(username, password, account_type):
    user = User(username, password, account_type)
    return user
