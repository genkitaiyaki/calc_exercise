class Formula:
    """
    計算式を管理するためのクラス
    """
    def __init__(
        self,
        _left: int,
        _right: int,
        _operator: str
        ) -> None:
        self._left = _left
        self._right = _right
        self._operator = _operator

    def to_string(self) -> str:
        return f'{str(self._left)} {self._operator} {str(self._right)}  ='
