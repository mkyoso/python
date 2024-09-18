## 本スクリプトについて

<!-- プロジェクト概要 -->

本スクリプトは Pandas ＋ SQLite を用いた CSV ファイルのデータベース取り込み用サンプルとなります。  
CSV 取り込み後のテーブルに対して実装している操作は以下になります。

■ テーブル操作

1. データ追加(insert)
2. 文字列連結(concut)
3. テーブルマージ(merge)

ディレクトリ構成は以下となります。  
📦Pandas_sqlite  
 ┣ 📂data  
 ┃ ┣ 📂INSERT_FS ※データ追加用  
 ┃ ┃ ┗ 📂※サブディレクト内に対象CSVを格納して下さい。  
 ┣ 📂db  
 ┃ ┗ 📜Pandas_sqlite.db ※DBが生成されていない場合は新規生成  
 ┣ 📂logs  
 ┃ ┗ 📜*.log ※ログ出力先  
 ┣ 📂settings  
 ┃ ┗ 📜settings.yml ※設定ファイル  
 ┗ 📜pandas‗sqlite.py  

<!-- 機能概要 -->
