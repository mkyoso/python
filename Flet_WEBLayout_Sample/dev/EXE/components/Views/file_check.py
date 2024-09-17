import os
from time import sleep
import datetime
import flet as ft
import pandas as pd
import simpledt

def FileCheckView(page):
    title = "FILE_CHECK"

    # 変数定義 #########################
    fs_res=[]
    fv_res=[]

    # プログレスバー表示
    pb = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)

    # DataFrame格納用ListView定義
    fs_lv=ft.ListView(fs_res,expand=True, spacing=10, padding=20)
    fv_lv=ft.ListView(fv_res,expand=True, spacing=10, padding=20)

    # 内部ファンクション定義 #########################
    # ディレクトリ指定ダイアログ（検索先の指定）
    def get_directry_result(e: ft.FilePickerResultEvent):
        if e.path:
            pb.visible=True
            selected_directry.value = e.path
            for i in range(0, 101):
                pb.value = i * 0.01
                sleep(0.1)
                page.update()
            read_btn.visible = True
            pb.visible=False
            page.update()
        else:
            selected_directry.value = "キャンセルされました。"

    ## [Flet表示]ファイル読み込みボタンクリック処理
    # 指定ディレクトリ配下のファイル/サブディレクトリ検索処理
    def read_btn_clicked(e):
        pb.visible=True
        data=list()
        for root, dirs, files in os.walk(selected_directry.value):
            for filename in files:
                nm, ext = os.path.splitext(filename)
                fullpath = os.path.join(os.path.abspath(root), filename)
                ct=os.path.getctime(fullpath)
                mt=os.path.getmtime(fullpath)
                gdt=datetime.datetime.fromtimestamp(ct)
                mdt=datetime.datetime.fromtimestamp(mt)
                data.append((filename, gdt ,mdt, fullpath,))
        df1 = pd.DataFrame(data, columns=['ファイル名', '作成日付', '更新日付', 'ファイルパス',])
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()
        simpledt_df = simpledt.DataFrame(df1)
        fs_res.append(simpledt_df.datatable)
        pb.visible=False
        page.update()

    # 起動時実工処理 #########################
    # タブ_1：アクション定義

    ## [Flet_UI]ディレクトリ選択ボタン定義
    selected_directry = ft.TextField(
        hint_text="ディレクトリが指定されていません。",
        expand=True,
        read_only=True
    )
    ## 選択ダイアログ表示処理
    get_directry_dialog = ft.FilePicker(on_result=get_directry_result)
    page.overlay.append(get_directry_dialog)

    ## [Flet_UI]検索対象ディレクトリ選択ボタン定義
    directory_select_btn=ft.ElevatedButton(
        "ディレクトリを指定",
        icon=ft.icons.CONTENT_PASTE_SEARCH,
        on_click=lambda _: get_directry_dialog.get_directory_path(),
    )

    ## [Flet_UI]ファイル/サブディレクトリ検索ボタン定義
    read_btn = ft.ElevatedButton(
        "検索",
        icon=ft.icons.FIND_IN_PAGE,
        visible=False,
        on_click=read_btn_clicked
    )

    # タブ_2：アクション定義


    # View定義 #########################
    # Bodyコンテンツ定義
    contents = ft.Tabs(
        selected_index=1,
        tabs=[
            ft.Tab(
                text="ファイル検索",
                content=ft.Column([
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.INFO, size=48),
                                    title=ft.Text("ディレクトリ内ファイル抽出", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                ),
                            ]),
                        padding=10,
                        ),
                    margin=10,
                    elevation=5,
                    ),
                    ft.Divider(),
                    ft.Text("ファイルリストを抽出するディレクトリを選択してください"),
                    ft.Row([directory_select_btn, selected_directry,pb]),
                    ft.Row([read_btn,pb]),
                    ft.Divider(),
                    ## Rowで横スクロール(scroll=ft.ScrollMode.AUTO)、Container内のListViewで縦方向スクロール
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                content=fs_lv,
                                margin=10,
                                padding=10,
                                border=ft.border.all(1),
                                border_radius=10,
                                width=1800,
                                height=350,
                            )
                        ],scroll=ft.ScrollMode.AUTO,expand=True)
                    )
                ])
            ),
        ],expand=1,
    )

    return {
        "view": contents,
        "title": title
        }