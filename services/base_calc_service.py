from abc import ABCMeta, abstractmethod
from models.formula import Formula
from services.common_service import CommonService
from models.exercise_parts import ExerciseParts

class BaseCalcService(metaclass=ABCMeta):
    """計算サービスが継承しなければならない基底クラス

    継承先のサービスに柔軟性を持たせるため、abstractmethodの実装以外は特に縛りを設けない
    """

    @abstractmethod
    def get_exercise_parts(self) -> ExerciseParts:
        """計算サービスで使用するExercisePartsを取得する関数

        Returns:
            ExerciseParts: 計算サービスで使用するExerciseParts
        """
        pass

    @abstractmethod
    def validater(self, left_num: int, right_num: int) -> bool:
        """計算サービスで使用するvalidater

        渡された値の組み合わせで作ってはいけない計算式をここで弾く

        Args:
            left_num (int): 計算式の左の値
            right_num (int): 計算式の左の値

        Returns:
            bool: 値の組み合わせが許容される場合True, 許容されない場合False
        """
        pass
