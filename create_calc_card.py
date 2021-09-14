import random   
from datetime import datetime as dt
from models.formula import Formula
from models.exercise_parts import ExerciseParts
import jinja2
import numpy as np
from itertools import product
from typing import Callable
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from selenium.webdriver.support import expected_conditions as EC
import os

# TODO: 肥大化気味なのでServiceクラスを作り移動する
# TODO: docstringをちゃんと書いて不要なコメントを消す
# TODO: 今後のことを考えコントローラークラスにする

def create_formulas(
    exercise_parts: ExerciseParts,
    validater: Callable,
    needs_shuffle: bool = True
    ) ->list[Formula]:
    """
    計算式リストを作成する
    """

    formulas: list[str] = []
    for left_num, right_num in product(exercise_parts.lefts, exercise_parts.rights):
        if (not validater(left_num, right_num)): continue
        formula = Formula(left_num, right_num, exercise_parts.operater).to_string()
        formulas.append(formula)

    if (needs_shuffle): random.shuffle(formulas)
    return formulas

# 計算リストをPDFで出力する関数
def export_exercise(
    title: str,
    formulas: list[str]
    ) -> None:

    # Chrome の印刷機能でPDFとして保存
    # pdfkitだと表示崩れがおきるためseleniumで印刷処理を行う
    options = webdriver.ChromeOptions()
    # PDF印刷設定
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "pageSize": 'A4'
    }
    # ドライバへのPDF印刷設定の適用
    # TODO: 任意のフォルダに出力できるようにする
    dir = os.path.dirname(os.path.abspath('__file__'))
    options.add_experimental_option("prefs", {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        "safebrowsing.enabled": True,
    })
    options.add_argument('--kiosk-printing')
    options.add_argument('--headless')

    # jinja2でtemplateを読み込む
    # TODO: template.html周りははModel化する？
    fsloader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=fsloader)
    template = env.get_template('template.html')
    MAX_COL = 4 # A4印刷だと4列がいい感じになる
    html = template.render({
	    'title': title
	    ,'MAX_COL': MAX_COL
	    ,'formula_columns': np.array_split(formulas, MAX_COL) 
    })

    # TODO: chromedriverの存在チェック処理を入れる

    with webdriver.Chrome("./chromedriver", options=options) as driver:
        wait = WebDriverWait(driver, 15)
        driver.implicitly_wait(10)
        
        driver.get("data:text/html;charset=utf-8," + html)
        # ページ上のすべての要素が読み込まれるまで待機
        wait.until(EC.presence_of_all_elements_located)
        # PDFとして印刷
        driver.execute_script('window.print()')
        driver.quit()

# 足し算式を作る
def add_validater(left_num: int, right_num: int) -> bool:
    # まだ学校で習っていないので合計が１０を超える式はだめ
    if(left_num + right_num > 10): return False
    # 0+0の式はやる意味がないのでだめ
    if(left_num == 0 and right_num == 0): return False
    return True

add_exercise_parts = ExerciseParts(list(range(0,10)), list(range(0,10)), "+")
add_formulas = create_formulas(add_exercise_parts, add_validater)

# 引き算式を作る
def sub_validater(left_num: int, right_num: int) -> bool:
    # 答えがマイナスになる式はだめ
    if(left_num - right_num < 0): return False
    # x - 0の引き算はやる意味がないのでだめ
    if(right_num == 0): return False
    return True
sub_exercises = ExerciseParts(list(range(0,11)), list(range(0,11)), "-")
sub_formulas = create_formulas(sub_exercises, sub_validater)

# 出力
export_exercise('たしざんのもんだい', add_formulas)
export_exercise('ひきざんのもんだい', sub_formulas)
