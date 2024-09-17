import flet as ft
from time import sleep
import pandas as pd
import simpledt

def FileOpenView(page):
    title = "FILE_OPEN"

    # 変数定義 #########################
    xlsx_res=[]
    csv_res=[]

    # プログレスバー表示
    pb = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)

    # DataFrame格納用ListView定義
    xlsx_lv=ft.ListView(xlsx_res,expand=1, spacing=10, padding=20)
    csv_lv=ft.ListView(csv_res,expand=1, spacing=10, padding=20)

    # 内部ファンクション定義 #########################
    ## ファイル選択結果詳細・読み込みボタン表示処理
    def xlsx_pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            xlsx_file_path_display.value = e.files[0].path
            xlsx_read_btn.visible = True
            page.update()
        else:
            pass

    ## ファイル読み込みボタンクリック処理
    # ここでファイルをpandasデータフレームに格納し、Flet SimpleDataTableに変換した内容をListViewに配列格納
    def xlsx_read_btn_clicked(e):
        pb.visible=True
        df = pd.read_excel(xlsx_file_path_display.value)
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()
        simpledt_df = simpledt.DataFrame(df)
        xlsx_res.append(simpledt_df.datatable)
        pb.visible=False
        page.update()

    def csv_pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            csv_file_path_display.value = e.files[0].path
            csv_read_btn.visible = True
            page.update()
        else:
            pass

    def csv_read_btn_clicked(e):
        pb.visible=True
        df = pd.read_csv(csv_file_path_display.value)
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()
        simpledt_df = simpledt.DataFrame(df)
        csv_res.append(simpledt_df.datatable)
        pb.visible=False
        page.update()

    # 起動時実工処理 #########################
    # タブ_1：アクション定義
    ## [Flet_UI]選択ファイル表示
    xlsx_file_path_display = ft.TextField(hint_text="ファイルを指定", read_only=True)

    ## ファイル選択ダイアログ表示処理
    xlsx_pick_files_dialog = ft.FilePicker(on_result=xlsx_pick_files_result)
    page.overlay.append(xlsx_pick_files_dialog)

    ## [Flet_UI]ファイル選択ボタン定義
    xlsx_file_select_btn = ft.ElevatedButton(
        "ファイルを選択",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: xlsx_pick_files_dialog.pick_files(allow_multiple=False),
    )

    ## [Flet_UI]ファイル読込ボタン定義
    xlsx_read_btn = ft.ElevatedButton(
        "ファイル読込",
        icon=ft.icons.FIND_IN_PAGE,
        visible=False,
        on_click=xlsx_read_btn_clicked
    )

    # タブ_2：アクション定義
    ## [Flet_UI]選択ファイル表示
    csv_file_path_display = ft.TextField(hint_text="ファイルを指定", read_only=True)

    ## ファイル選択ダイアログ表示処理
    csv_pick_files_dialog = ft.FilePicker(on_result=csv_pick_files_result)
    page.overlay.append(csv_pick_files_dialog)

    ## [Flet_UI]ファイル選択ボタン定義
    csv_file_select_btn = ft.ElevatedButton(
        "ファイルを選択",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: csv_pick_files_dialog.pick_files(allow_multiple=False),
    )

    ## [Flet_UI]ファイル読込ボタン定義
    csv_read_btn = ft.ElevatedButton(
        "ファイル読込",
        icon=ft.icons.FIND_IN_PAGE,
        visible=False,
        on_click=csv_read_btn_clicked
    )

    # View定義 #########################
    # Bodyコンテンツ定義
    contents = ft.Tabs(
        selected_index=1,
        tabs=[
            ft.Tab(
                text="Excel",
                content=ft.Column([
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.INFO, size=48),
                                    title=ft.Text("Excelファイル データフレーム表示", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                    subtitle=ft.Text("UTF-8形式のみ対応"),
                                ),
                            ]),
                        padding=10,
                        ),
                    margin=10,
                    elevation=5,
                    ),
                    ft.Text("データフレーム表示させるファイルを選択してください"),
                    ft.Row([xlsx_file_path_display, xlsx_file_select_btn]),
                    ft.Divider(),
                    ft.Row([xlsx_read_btn,pb]),
                    ## Rowで横スクロール(scroll=ft.ScrollMode.AUTO)、Container内のListViewで縦方向スクロール
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                content=xlsx_lv,
                                border=ft.border.all(1),
                                height=300,
                                width=1800
                            )
                        ],scroll=ft.ScrollMode.AUTO,expand=True)
                    )
                ])
            ),
            ft.Tab(
                text="CSV",
                content=ft.Column([
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.INFO, size=48),
                                    title=ft.Text("CSVファイル データフレーム表示", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                    subtitle=ft.Text("UTF-8形式のみ対応"),
                                ),
                            ]),
                            padding=10,
                        ),
                        margin=10,
                        elevation=5,
                    ),
                    ft.Text("データフレーム表示させるファイルを選択してください"),
                    ft.Row([csv_file_path_display, csv_file_select_btn]),
                    ft.Divider(),
                    ft.Row([csv_read_btn,pb]),
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                content=csv_lv,
                                border=ft.border.all(1),
                                height=300,
                                width=1800
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