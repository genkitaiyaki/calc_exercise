from services.common_service import CommonService
from models.exercise_parts import ExerciseParts

# TODO: docstringをちゃんと書いて不要なコメントを消す
# TODO: 今後のことを考えコントローラークラスにする

common_service = CommonService()

# 足し算式を作る
def add_validater(left_num: int, right_num: int) -> bool:
    # まだ学校で習っていないので合計が１０を超える式はだめ
    if(left_num + right_num > 10): return False
    # 0+0の式はやる意味がないのでだめ
    if(left_num == 0 and right_num == 0): return False
    return True

add_exercise_parts = ExerciseParts(list(range(0,10)), list(range(0,10)), "+")
add_formulas = common_service.create_formulas(add_exercise_parts, add_validater)

# 引き算式を作る
def sub_validater(left_num: int, right_num: int) -> bool:
    # 答えがマイナスになる式はだめ
    if(left_num - right_num < 0): return False
    # x - 0の引き算はやる意味がないのでだめ
    if(right_num == 0): return False
    return True
sub_exercises = ExerciseParts(list(range(0,11)), list(range(0,11)), "-")
sub_formulas = common_service.create_formulas(sub_exercises, sub_validater)

# 出力
common_service.export_exercise('たしざんのもんだい', add_formulas)
common_service.export_exercise('ひきざんのもんだい', sub_formulas)
