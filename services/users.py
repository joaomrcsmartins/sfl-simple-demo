# pylint: disable=C0111,consider-using-f-string,dangerous-default-value,line-too-long,fixme
from logging import Logger
from typing import List

import services.pets as p
from tools.logger import get_logger

SNACK_BONUS = 10
HAPPINESS_FAV_PET = 1  # buggy
HAPPINESS_PET = 1
PETTINGS_BONUS_MILESTONE = 100


class User:

    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get('name', 'Jamie Doe')
        self.age: int = kwargs.get('age', '0')
        self.favorite_pets: List[p.PetType] = kwargs.get('favorite_pets', [])
        self.snack_balance: int = kwargs.get('snack_balance', 0)
        self.pettings_given: int = kwargs.get('pettings_given', 0)
        self.happiness: int = kwargs.get('happiness', 0)
        self.logger: Logger = get_logger('Users', '')

    def set_logger(self, request_id: str) -> None:
        self.logger = get_logger('Users', request_id)

    def increase_snack_balance(self, snacks_added: int) -> None:
        if snacks_added > 0:  # TODO fix bug - adding snacks when the value is negative
            self.snack_balance += snacks_added
            self.logger.info('In users.py/User/increase_snack_balance():25 - "%s" added %d snacks. Snack balance is %d',
                             self.name, snacks_added, self.snack_balance)
        else:
            self.logger.error(
                'In users.py/User/increase_snack_balance():29 - "%s" trying to add snacks with non-positive value %d', self.name, snacks_added)

    def decrease_snack_balance(self) -> bool:
        if self.snack_balance <= 0:  # TODO fix bug - petting a pet with 0 snack balance
            self.logger.error(
                'In users.py/User/decrease_snack_balance():38 - "%s" has snack balance of %d, cannot pet a pet without snacks', self.name, self.snack_balance)
            return False

        # TODO fix bug - balance should decrease 1 snack in each pet
        self.snack_balance -= p.PETTING_SNACK_COST
        self.logger.info(
            'In users.py/User/decrease_snack_balance():44 - "%s"\'s snack balance after petting: %d', self.name, self.snack_balance)
        return True

    def increase_pettings_given(self) -> None:
        self.pettings_given += 1
        self.logger.info('In users.py/User/increase_pettings_given():50 - "%s" has %d pettings given',
                         self.name, self.pettings_given)

    def change_happiness(self, was_petted: bool, pet_type: p.PetType, pet_name: str) -> None:
        if was_petted:
            if pet_type in self.favorite_pets:
                # TODO fix bug - petting favorite pet increases happiness by 2
                self.happiness = max(100, self.happiness + HAPPINESS_FAV_PET)
            else:
                self.happiness = max(100, self.happiness + HAPPINESS_PET)

            self.logger.info('In users.py/User/change_happiness():55 - "%s" pet "%s". Happiness after petting: %d',
                             self.name, pet_name, self.happiness)
            self.check_full_happiness()
        else:
            self.happiness = max(0, self.happiness-1)
            self.logger.info('In users.py/User/change_happiness():66 - "%s" was bit by "%s". Happiness after bite: %d',
                             self.name, pet_name, self.happiness)

    def pet_a_pet(self, pet: p.Pet) -> None:
        if self.decrease_snack_balance():
            pet_type = pet.pet_type
            pet_name = pet.name
            was_petted = pet.receive_petting(self.name)
            self.change_happiness(was_petted, pet_type, pet_name)
            if was_petted:
                self.increase_pettings_given()
                self.check_good_client_bonus()

    def check_full_happiness(self) -> None:
        if self.happiness == 100:
            self.logger.info(
                'In users.py/User/check_full_happiness():81 - "%s" is totally happy!', self.name)

    def is_good_client(self) -> bool:
        # TODO fix bug - good client give 100 or more pettings
        if self.pettings_given >= 100:
            self.logger.info('In users.py/User/is_good_client():87 - "%s" is a good client with %d pettings given!',
                             self.name, self.pettings_given)
            return True
        return False

    def check_good_client_bonus(self) -> None:
        if self.is_good_client() and self.pettings_given % 100 == 0:
            self.snack_balance += SNACK_BONUS
            self.logger.info('In users.py/User/check_good_client_bonus():94 - "%s" receives bonus snacks for %d pettings given!',
                             self.name, self.pettings_given)
