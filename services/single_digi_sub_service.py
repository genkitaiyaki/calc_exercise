from services.base_calc_service import BaseCalcService
from models.exercise_parts import ExerciseParts

class SingleDigiSubService(BaseCalcService):
    """１桁の引き算サービス
    小学1年生向けの、繰り上がりが発生しない引き算を提供するためのサービス

    Args:
        BaseCalcService 
    """

    def get_exercise_parts(self) -> ExerciseParts:
        return ExerciseParts(list(range(0,11)), list(range(0,11)), "-")

    def validater(self, left_num: int, right_num: int) -> bool:
        # 答えがマイナスになる式は1年生前半で習っていないためだめ
        if(left_num - right_num < 0): return False
        # x - 0の引き算はやる意味がないのでだめ
        if(right_num == 0): return False
        return True