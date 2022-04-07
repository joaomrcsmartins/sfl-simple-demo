# pylint: disable=C0111,consider-using-f-string,dangerous-default-value,line-too-long,fixme
import json
import os
from typing import List, Set, Tuple

from services.pets import Pet
from services.users import User

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def load_pets(filename: str) -> Set[Pet]:
    try:
        with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as file:
            pets_info = json.load(file)
            pets = {}
            for pet_info in pets_info:
                pets[pet_info['name']] = Pet(**pet_info)
            print('Loaded pets. There are {} pets!'.format(len(pets)))
            return pets

    except OSError as err:
        print('Failed to open pets DB file. Error - {}'.format(str(err)))
        return None


def load_users(filename: str) -> Set[User]:
    try:
        with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as file:
            users_info = json.load(file)
            users = {}
            for user_info in users_info:
                users[user_info['name']] = User(**user_info)
            print('Loaded users. There are {} users!'.format(len(users)))
            return users
    except OSError as err:
        print('Failed to open users DB file. Error - {}'.format(str(err)))
    return None


def load_script(filename: str) -> Set[dict]:
    try:
        with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as file:
            script = json.load(file)
            print('Loaded script. There are {} requests!'.format(len(script)))
            return script
    except OSError as err:
        print('Failed to open pets DB file. Error - {}'.format(str(err)))
    return None


def load() -> Tuple[Set[Pet], Set[User], List[dict]]:
    pets = load_pets('databases/pets.json')
    users = load_users('databases/users.json')
    script = load_script('scripts/load_script.json')
    return pets, users, script
