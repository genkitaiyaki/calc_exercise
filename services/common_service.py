from typing import Callable
from models.formula import Formula
from models.exercise_parts import ExerciseParts
from itertools import product
from typing import Callable
import random
import jinja2
from os import path
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from selenium.webdriver.support import expected_conditions as EC
import os

class CommonService():
    """汎用的な関数をまとめたサービスクラス

    現状特に縛りは設けていない
    """

    def create_formulas(
        self,
        exercise_parts: ExerciseParts,
        validater: Callable,
        needs_shuffle: bool = True
        ) ->list[Formula]:

        """計算式リストを作成する関数

        演算子の左と右の数字の全ての組み合わせをexercise_partsから生成し、
        validaterで不要な組み合わせを除外することで計算式リストを生成する

        計算式リストはデフォルトで順番がランダムになるが、
        引数を指定することでランダムにしないことも可能

        Args:
            exercise_parts (ExerciseParts): 計算式を作成する際に必要な部品達
            validater (Callable): 不要な計算式の組み合わせを除外するためのvalidater
            needs_shuffle (bool, optional): 順序をランダムにするかどうか. デフォルトはTrue.

        Returns:
            list[Formula]: 計算式
        """

        formulas: list[str] = []
        for left_num, right_num in product(exercise_parts.lefts, exercise_parts.rights):
            if (not validater(left_num, right_num)): continue
            formula = Formula(left_num, right_num, exercise_parts.operater).to_string()
            formulas.append(formula)
    
        if (needs_shuffle): random.shuffle(formulas)
        return formulas

    def export_exercise(
        self,
        title: str,
        formulas: list[str]
        ) -> None:
        """計算式リストをPDF出力する関数

        Chromeの印刷機能を使用してpdf出力を行う
        出力先はChromeにて設定しているダウンロードディレクトリとなる

        Args:
            title (str): 出力するPDFファイルのタイトル
            formulas (list[str]): 出力する計算式リスト
        """

        # TODO: 関数内が肥大化気味なので関数に切り出すことを検討する。webdriverの設定部分とか切り出せそう？

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
        
        # TODO: headlessで実行する場合kiosk-printing設定が有効にならないため実行方法を再検討する必要がある
        # options.add_argument('--headless')

        # TODO: pathの指定周りはもう少し綺麗に書けそう。。
        services_path = path.dirname(__file__)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(f'{services_path}/../templates/'))
        template = env.get_template('template.html')
        MAX_COL = 4 # A4印刷だと4列がいい感じになる
        html = template.render({
    	    'title': title
    	    ,'MAX_COL': MAX_COL
    	    ,'formula_columns': np.array_split(formulas, MAX_COL) 
        })

        chromedriver_path = f'{services_path}/../chromedriver'
        if(not os.path.isfile(chromedriver_path)) :
            print('ERROR! Unable to print. Because chromedriver not found.')
            return
        with webdriver.Chrome(chromedriver_path, options=options) as driver:
            wait = WebDriverWait(driver, 15)
            driver.implicitly_wait(10)
            driver.get("data:text/html;charset=utf-8," + html) # htmlの文字列をchrome上に表示する
            wait.until(EC.presence_of_all_elements_located) # ページ上のすべての要素が読み込まれるまで待機
            driver.execute_script('window.print()')
            driver.quit()