from abc import ABCMeta, abstractmethod
from models.formula import Formula
from services.common_service import CommonService
from models.exercise_parts import ExerciseParts

class BaseCalcService(metaclass=ABCMeta):

    @abstractmethod
    def get_exercise_parts(self) -> ExerciseParts:
        pass

    @abstractmethod
    def validater(self, left_num: int, right_num: int) -> bool:
        pass
