from typing import Callable

class ExerciseParts:
    """
    練習問題に使用する部品クラス
    計算式を作成する際に使う値を管理する
    """
    def __init__(
        self,
        lefts: list[int],
        rights: list[int],
        operater: str
        ) -> None:
        self.lefts = lefts
        self.rights = rights
        self.operater = operater