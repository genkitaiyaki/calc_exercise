# calc_exercise

## これは何？

１桁の足し算と引き算の練習問題をPDF出力します。
問題の順番は出力するたびに変わります。

## どう使うの?

### 事前準備

このアプリはchromedriverを必要とします。
以下のサイトから実行環境に合ったchromedriverをダウンロードし、
\_\_main\_\_.pyと同じ階層に配置してください。

### 実行方法

ターミナル上で以下のコマンドを実行してください

```<shellscript>
python3 calc_exercise
```

計算問題を選ぶCLIが表示されます。
任意の計算問題を選択してください。

```<text>
Select calc type.
 add (+)
 sub (-) 
```

chromedriverを使用し、
計算問題のpdfがChromeのダウンロードディレクトリに出力されます。
