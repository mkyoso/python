import os
import flet as ft
import simpledt
import sqlite3

def DBView(page):
    title = "DATA_TABLE"

    # 変数定義 #########################
    # DB関連変数定義
    db_res=[]
    db_path= r"d:/Desktop/vscode/WinPy/py_Flet_WEBLayout_v2/dev/EXE/components/Views/db/data.db"

    # 内部ファンクション定義 #########################
    # DB接続処理
    def connect_db(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.OperationalError as e:
            if "unable to open database file" in str(e):
                print(f"データベースファイル '{db_file}' を開けません。")
            else:
                raise e

    # [Flet_UI]実行ボタン処理
    def read_btn_clicked(e):
        db_res.clear()
        sql = simpledt.SQLDataTable('sqlite', f'{db_path}', f'{tbl_nm.value}')
        dt = sql.datatable
        db_res.append(dt)
        page.update()

    # 起動時実工処理 #########################
    # DB接続
    con=connect_db(db_path)
    cur = con.cursor()
    # DBテーブル生成※存在する場合はスキップ
    cur.execute('CREATE TABLE IF NOT EXISTS dummy(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')
    con.commit()
    #テーブル名取得
    cur.execute("SELECT name from sqlite_master where type='table';")
    #テーブル名配列格納
    tbl_res=[row[0] for row in cur.fetchall()]
    #DBクローズ
    con.close()

    # DBデータ格納用ListView定義
    lv = ft.ListView(db_res, expand=1, auto_scroll=True)

    # テーブルリスト表示定義
    tbl_nm=ft.Dropdown()
    for tbl in tbl_res:
        tbl_nm.options.append(ft.dropdown.Option(tbl))

    # [Flet_UI]読み込みボタン定義
    read_btn = ft.ElevatedButton(
        "テーブル読込実施", icon=ft.icons.FIND_IN_PAGE, visible=True, on_click=read_btn_clicked
    )

    # View定義 #########################
    # Bodyコンテンツ定義
    contents = ft.Column([
                ft.Card(
                    ft.Container(
                        ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.INFO, size=48),
                                title=ft.Text("SQLiteテーブル表示", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                subtitle=ft.Text("DB表示サンプル"),
                            ),
                        ]),
                    padding=10,
                    ),
                    margin=10,
                    elevation=5,
                ),
                ft.Row([tbl_nm, read_btn]),
                ft.Divider(),
                ft.Container(
                    ft.Row([
                            ft.Container(
                                content=lv,
                                border=ft.border.all(1),
                                height=200,
                                width=800
                            ),
                    ],height=200, scroll=ft.ScrollMode.AUTO)
                )
            ])

    return {
        "view": contents,
        "title": title
        }