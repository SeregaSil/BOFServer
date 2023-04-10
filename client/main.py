import requests
from testdata import BUILDINGS
import json




# class BOFError(Exception):
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return 'Game Error'


class AuthError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Bad email or password'


class NoGameError(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f'Game with the id {self.id} is not available'


class RegistrationError(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return f'Email {self.email} already used'


def register(email: str, password: str):
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url=f'{URL}/user/register', json=data)
    if response.status_code == requests.codes.conflict:
        raise RegistrationError(email)

    return login(email, password)


def login(email: str, password: str):
    data = {
        'username': email,
        'password': password
    }
    response = requests.post(url=f'{URL}/login', data=data)
    if response.status_code == requests.codes.not_found:
        raise AuthError

    jwt = response.json().get('access_token')

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {jwt}'})
    return session


def get_game_info(game_id, session):
    response = session.get(url=f'{URL}/user/game/{game_id}')
    if response.status_code == requests.codes.not_found:
        raise NoGameError(game_id)
    return response.json()


def get_all_games(session):
    response = session.get(url=f'{URL}/user/game')
    return response.json()


def create_game_save(session: requests.Session, game_id, army: dict | None = None, resources: dict | None = None,
                     houses: dict | None = None):
    data = {
        'army': army,
        'resources': resources,
        'houses': houses,
        'id': game_id,
    }
    response = session.post(url=f'{URL}/user/game', json=data)
    if response.status_code == requests.codes.ok:
        return 'Save'


def main():
    s = login('2', '1')
    print(create_game_save(s, 0, houses=BUILDINGS))


if __name__ == '__main__':
    import secrets
    print(secrets.token_urlsafe(64))
