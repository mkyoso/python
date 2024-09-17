## スクリプトについて

本スクリプトは Python クロスプラットフォームデスクトップアプリを作成する際に Flet を採用する場合のベース用となります。

<!-- プロジェクトの概要を記載 -->

このスクリプトでは WEB レイアウト(上部ナビゲーション、サイドメニュー、コンテンツ)構築時の画面遷移サンプルとなるよう構築しています。  

各画面サンプルの概要
1. FILE_CHECK(components/Views/file_check.py) … ディレクトリ走査結果のListView格納(縦・横スクロール)  
2. FILE_OPEN(components/Views/file_open.py) … pandasデータフレームのsimpledatatable格納およびdatatableのListView格納(縦・横スクロール)
3. FILE_COMPARE(components/Views/file_diffs.py) … ファイルDiff(Difflib)結果のTextField格納
4. DATA_TABLE(components/Views/db_tables.py) … SQLite DBの新規作成、テーブルデータの読み込みおよびListView格納
5. README_VIEW(components/Views/readme.py) … テキストファイルの読み込みおよびListViewへのテキスト格納

また、Top 画面はダッシュボード風にしています。  

画面遷移は以下ファイルで実施しています。  
1. routes.py
2. nav_side.py



