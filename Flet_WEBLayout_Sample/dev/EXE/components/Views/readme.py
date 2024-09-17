import os
import flet as ft

def ReadView(page):
    title = "ツール概要"

    lines=[]
    str = ''
    lv = ft.ListView(expand=1, auto_scroll=True)

    with open(r'./WinPy/py_Flet_WEBLayout_v2/dev/EXE/README.txt', encoding='utf-8', newline='\r\n') as f:
        for lines in f:
            lv.controls.append(ft.Text(f"{lines}"))
    #str = ''.join(lines)

    # View定義 #########################
    # Bodyコンテンツ定義
    contents = ft.Column([
        ft.Card(
            ft.Container(
                ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INFO, size=48),
                        title=ft.Text("Flet 画面遷移サンプル", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                        subtitle=ft.Text("WEBレイアウトサンプル"),
                    ),
                    ft.Row([
                        ft.Text("作成日："),
                        ft.Text("更新日："),
                        ft.Text("作成者：")
                    ])
                ]),
                padding=10,
            ),
            margin=10,
            elevation=5,
        ),
        ft.Divider(),
        ft.Column([ lv ],
        alignment=ft.MainAxisAlignment.START,
        expand=True,auto_scroll=True
        )
    ])

    return {
        "view":contents,
        "title": title
        }