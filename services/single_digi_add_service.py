from services.base_calc_service import BaseCalcService
from models.exercise_parts import ExerciseParts

class SingleDigiAddService(BaseCalcService):
    """１桁の足し算サービス
    小学1年生向けの、繰り上がりが発生しない足し算を提供するためのサービス

    Args:
        BaseCalcService 
    """

    def get_exercise_parts(self) -> ExerciseParts:
        return ExerciseParts(list(range(0,10)), list(range(0,10)), "+")

    def validater(self, left_num: int, right_num: int) -> bool:
        # 合計が１０を超える式は 1年生前半で習っていないためだめ
        if(left_num + right_num > 10): return False
        # 0+0の式はやる意味がないのでだめ
        if(left_num == 0 and right_num == 0): return False
        return True