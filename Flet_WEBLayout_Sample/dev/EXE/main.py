import flet as ft
from components.Views.routes import Router
from components.user_controles.nav_bar import NavBar
from components.user_controles.nav_side import NavMenu

def main(page: ft.Page):

    # Page定義
    page.theme_mode = "dark"
    # Appbar(上部メニューバー：./components/user_controles/nav_bar.py)のPage追加
    page.appbar = NavBar(page)

    # 画面遷移処理(./components/Views/routes.py)定義
    routes = Router(page)
    page.on_route_change = routes.route_change

    # 画面構成定義
    page.add(
        ft.Row(
            [
                ft.Column([NavMenu(page),]),
                ft.VerticalDivider(width=1),
                ft.Column([ routes.body ], alignment=ft.MainAxisAlignment.START, expand=True,auto_scroll=True),
            ],
            alignment=ft.MainAxisAlignment.START, expand=True
        ),
    )
    # index.py(/)を初期画面にして起動
    page.go('/')

ft.app(target=main)