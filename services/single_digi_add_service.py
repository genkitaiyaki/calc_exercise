from services.base_calc_service import BaseCalcService
from models.exercise_parts import ExerciseParts

# TODO: docstringをちゃんと書いて不要なコメントを消す

class SingleDigiAddService(BaseCalcService):

    def get_exercise_parts(self) -> ExerciseParts:
        return ExerciseParts(list(range(0,10)), list(range(0,10)), "+")

    def validater(self, left_num: int, right_num: int) -> bool:
        # まだ学校で習っていないので合計が１０を超える式はだめ
        if(left_num + right_num > 10): return False
        # 0+0の式はやる意味がないのでだめ
        if(left_num == 0 and right_num == 0): return False
        return True