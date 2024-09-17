import flet as ft
import os
from time import sleep
import difflib

def FileDiffView(page):
    title = "FILE_OPEN"

    # 変数定義 #########################
    # ファイル読込内容格納用ListView定義
    #lv = ft.ListView(res,expand=True, spacing=10, padding=20)
    #mat_lv = ft.ListView(mat_res,expand=True, spacing=10, padding=20)
    # プログレスバー表示
    pb = ft.ProgressRing(width=16, height=16, stroke_width = 2, visible=False)

    # 内部ファンクション定義 #########################
    # 比較先ファイル選択結果詳細定義
    def src_pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            src_file_path_display.value = e.files[0].path
            page.update()
        else:
            pass

    # 比較先ファイル選択結果詳細定義
    def dst_pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            dst_file_path_display.value = e.files[0].path
            read_btn.visible = True
            page.update()
        else:
            pass

    # Diff実行ボタン処理
    def read_btn_clicked(e):
        res=[]
        mat_res=[]
        pb.visible=True
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()
        ck1 = open(src_file_path_display.value,encoding = 'utf-8')
        ck2 = open(dst_file_path_display.value,encoding = 'utf-8')
        diff = difflib.Differ()
        output_diff = diff.compare(ck1.readlines(), ck2.readlines())
        for data in output_diff :
            if data[0:1] in ['+', '-'] :
                res.append(data)
        #一致箇所を表示する場合
            elif data[0:1] not in ['+', '-', '?'] :
                mat_res.append(data)
        ck1.close
        ck2.close
        pb.visible=False
        result_field.value=res
        m_result_field.value=mat_res
        page.update()

    # 起動時実工処理 #########################
    # 比較元ファイルパス表示用定義
    src_file_path_display = ft.TextField(hint_text="ファイルを指定", read_only=True)

    # 比較先ファイルパス表示用定義
    dst_file_path_display = ft.TextField(hint_text="ファイルを指定", read_only=True)

    # 比較元ファイル選択ダイアログ定義
    pick_src_files_dialog = ft.FilePicker(on_result=src_pick_files_result)
    page.overlay.append(pick_src_files_dialog)

    # 比較先ファイル選択ダイアログ定義
    pick_dst_files_dialog = ft.FilePicker(on_result=dst_pick_files_result)
    page.overlay.append(pick_dst_files_dialog)

    # [Flet_UI]比較元ファイル選択ダイアログボタン定義
    src_select_btn = ft.ElevatedButton(
        "比較元ファイルを選択",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: pick_src_files_dialog.pick_files(allow_multiple=False),
    )

    # [Flet_UI]比較先ファイル選択ダイアログボタン定義
    dst_select_btn = ft.ElevatedButton(
        "比較先ファイルを選択",
        icon=ft.icons.FILE_OPEN,
        on_click=lambda _: pick_dst_files_dialog.pick_files(allow_multiple=False),
    )

    # [Flet_UI]Diff実行ボタン定義
    read_btn = ft.ElevatedButton(
        "ファイル比較実施", icon=ft.icons.FIND_IN_PAGE, visible=False, on_click=read_btn_clicked
    )

    # [Flet_UI]Diff結果フィールド定義_1
    result_field = ft.TextField(
        label="比較結果",
        multiline=True,
        disabled=True,
    )

    # [Flet_UI]Diff結果フィールド定義_2
    m_result_field = ft.TextField(
        label="一致結果",
        multiline=True,
        disabled=True,
    )

    # View定義 #########################
    # Bodyコンテンツ定義
    contents = ft.Column([
                ft.Card(
                    ft.Container(
                        ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.INFO, size=48),
                                title=ft.Text("ファイル比較", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                subtitle=ft.Text("UTF-8のみ対応"),
                            ),
                        ]),
                    padding=10,
                    ),
                margin=10,
                elevation=5,
                ),
                ft.Text("比較させるファイルを選択してください"),
                ft.Row([src_file_path_display, src_select_btn]),
                ft.Row([dst_file_path_display, dst_select_btn]),
                ft.Row([read_btn,pb]),
                ft.Divider(),
                ft.Container(
                    ft.Row([
                        ft.Container(
                            content=result_field,
                            margin=10,
                            padding=10,
                            border=ft.border.all(1),
                            border_radius=10,
                            width=800,
                            height=350,
                        ),
                        ft.VerticalDivider(),
                        ft.Container(
                            content=m_result_field,
                            margin=10,
                            padding=10,
                            border=ft.border.all(1),
                            border_radius=10,
                            width=800,
                            height=350,
                        ),
                        ],scroll=ft.ScrollMode.AUTO,expand=True)
                    )
            ])


    return {
        "view": contents,
        "title": title
        }