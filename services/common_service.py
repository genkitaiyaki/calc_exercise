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
    def create_formulas(
        self,
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
        self,
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

        # TODO: chromedriverの存在チェック処理を入れる
        with webdriver.Chrome(f'{services_path}/../chromedriver', options=options) as driver:
            wait = WebDriverWait(driver, 15)
            driver.implicitly_wait(10)

            driver.get("data:text/html;charset=utf-8," + html)
            # ページ上のすべての要素が読み込まれるまで待機
            wait.until(EC.presence_of_all_elements_located)
            # PDFとして印刷
            driver.execute_script('window.print()')
            driver.quit()