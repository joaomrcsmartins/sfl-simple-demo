# pylint: disable=C0111
from typing import List
from load_script import load
from services.pets import Pet
from services.users import User


def run(pets: dict[str, Pet], users: dict[str, User], script: List[dict]) -> None:
    for request in script:
        user_id = request['user']
        request_id = str(request['request_id'])
        action_name = request['action']
        value = request['value']

        user = users[user_id]
        user.set_logger(request_id)

        action = getattr(user, action_name)
        if action_name == 'pet_a_pet':
            pet = pets[value]
            pet.set_logger(request_id)
            action(pet)
        else:
            action(value)


if __name__ == '__main__':
    p, u, s = load()
    run(p, u, s)
