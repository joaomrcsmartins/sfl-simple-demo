# pylint: disable=C0111,consider-using-f-string,dangerous-default-value,line-too-long,fixme
from enum import Enum
from logging import Logger
from random import randint
from typing import Dict

from tools.logger import get_logger


class PetType(str, Enum):
    DOG = 'DOG'
    CAT = 'CAT'
    HAMSTER = 'HAMSTER'
    CANARY = 'CANARY'
    SNAKE = 'SNAKE'
    FERRET = 'FERRET'
    GUINEA_PIG = 'GUINEA_PIG'


FAV_HUMAN_PETS = 10
GOOD_PET_PETTINGS = 100
GOOD_PET_BONUS_SNACKS = 2
HAPPINESS_PETTING = 2
HAPPINESS_PETTING_FAV_HUMAN = 5
HAPPINESS_BITING = 1
SNACK_FACTOR = 30
SNACK_THRESHOLD = 20
PETTINGS_FACTOR = 50
PETTINGS_THRESHOLD = 100
PETTING_SNACK_COST = 2  # buggy


class Pet():
    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get('name', 'ghost')
        self.age: int = kwargs.get('age', 0)
        self.pet_type: PetType = kwargs.get('pet_type', PetType.DOG)
        self.happiness: int = kwargs.get('happiness', 0)
        self.pettings_received: int = kwargs.get('pettings_received', 0)
        self.snacks_received: int = kwargs.get('snacks_received', 0)
        self.humans_petted: Dict[str, int] = kwargs.get('humans_petted', {})
        self.bitting_chance: int = kwargs.get(
            'bitting_chance', randint(0, 100))
        self.logger: Logger = get_logger('Pets', '')

    def set_logger(self, request_id: str) -> None:
        self.logger = get_logger('Pets', request_id)

    def receive_petting(self, human_name: str) -> bool:
        if self.does_bite(human_name):
            self.decrease_happiness(HAPPINESS_BITING)
            self.logger.info('In pets.py/Pet/receive_petting():50 - %s "%s" bit human "%s". Happiness after petting: %d',
                             self.pet_type, self.name, human_name, self.happiness)
            return False

        if human_name in self.humans_petted:
            self.humans_petted[human_name] += 1

            if self.is_human_favorite(human_name):
                self.increase_happiness(HAPPINESS_PETTING_FAV_HUMAN)
                self.logger.info('In pets.py/Pet/receive_petting():60 - %s "%s" was petted by favorite human "%s". Happiness after petting: %d',
                                 self.pet_type, self.name, human_name, self.happiness)
            else:
                self.increase_happiness(HAPPINESS_PETTING)
                self.logger.info('In pets.py/Pet/receive_petting():64 - %s "%s" was petted by human "%s". Happiness after petting: %d',
                                 self.pet_type, self.name, human_name, self.happiness)
        else:
            self.humans_petted[human_name] = 1
            self.increase_happiness(HAPPINESS_PETTING)
            self.logger.info('In pets.py/Pet/receive_petting():69 - %s "%s" was petted by human "%s". Happiness after petting: %d',
                             self.pet_type, self.name, human_name, self.happiness)

        self.is_totally_happy()
        self.pettings_received += 1
        self.check_good_pet_bonus()
        self.snacks_received += PETTING_SNACK_COST
        self.logger.info('In pets.py/Pet/receive_petting():76 - %s "%s" has received %d snacks in total',
                         self.pet_type, self.name, self.snacks_received)
        return True

    def increase_happiness(self, value: int) -> None:
        self.happiness += value  # TODO fix bug - happiness shouldn't go over 100
        self.logger.info('In pets.py/Pet/increase_happiness():82 - %s "%s" happiness increased by %d',
                         self.pet_type, self.name, value)

    def decrease_happiness(self, value: int) -> None:
        self.happiness -= value  # TODO fix bug - happiness shouldn't drop 0
        self.logger.info('In pets.py/Pet/decrease_happiness():87 - %s "%s" happiness decreased by %d',
                         self.pet_type, self.name, value)

    def is_human_favorite(self, human_name: str) -> bool:
        # TODO fix bug - human is favorite when it gives at least FAV_HUMAN_PETS
        return human_name in self.humans_petted and self.humans_petted[human_name] > FAV_HUMAN_PETS

    def does_bite(self, human_name: str) -> bool:
        if self.is_human_favorite(human_name):
            return False
        biting_rand = randint(0, 100)
        snack_value = SNACK_FACTOR if self.snacks_received > SNACK_THRESHOLD else 0
        petting_value = PETTINGS_FACTOR if self.pettings_received > PETTINGS_THRESHOLD else 0
        # TODO fix bug - bitting chance is inclusive -> [0,biting_chance]
        return biting_rand < max(0, (self.bitting_chance - snack_value - petting_value))

    def is_good_pet(self) -> bool:
        return self.pettings_received >= GOOD_PET_PETTINGS

    def is_totally_happy(self) -> bool:
        if self.happiness == 100:
            self.logger.info(
                'In pets.py/Pet/is_totally_happy():108 - %s "%s" is totally happy!', self.pet_type, self.name)
            return True
        return False

    def check_good_pet_bonus(self) -> None:
        if self.is_good_pet():
            self.snacks_received += GOOD_PET_BONUS_SNACKS
            self.logger.info('In pets.py/Pet/check_good_pet_bonus():116 - %s "%s" is a good pet and got %d extra snacks. Good boy/girl!',
                             self.pet_type, self.name, GOOD_PET_BONUS_SNACKS)
