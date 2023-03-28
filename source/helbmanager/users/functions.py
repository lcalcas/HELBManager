from unidecode import unidecode
from .models import User


def create_username(first_name: str, last_name: str) -> str:
    result = format_username(first_name, last_name)
    other_users = User.objects.filter(username__startswith=result)
    return result + (str(len(other_users)) if len(other_users) else "")


def format_username(first_name: str, last_name: str) -> str:
    first_half = format_to_size(last_name, 4)
    second_half = format_to_size(first_name, 3)
    return unidecode(first_half + second_half).lower()


def format_to_size(string: str, size: int) -> str:
    return (string + "".join(["x" for _ in range(size - len(string))]))[:size]


if __name__ == '__main__':
    pass
