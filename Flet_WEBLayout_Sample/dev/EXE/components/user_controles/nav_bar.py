import flet as ft


def NavBar(page):

    # 内部ファンクション定義 #########################
    # Flet_UIテーマ変更処理
    def toggle_icon(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        toggle_dark_light_icon.selected = not toggle_dark_light_icon.selected
        page.update()

    # Flet終了処理
    def exit_app(e):
        page = e.page
        page.window_destroy()

    toggle_dark_light_icon=ft.IconButton(
        icon="light_mode",
        selected_icon = "dark_mode",
        tooltip=f"switch light / dark mode",
        on_click=toggle_icon,
    )

    exit_btn=ft.IconButton(
        icon=ft.icons.EXIT_TO_APP,
        on_click=exit_app, icon_color="red"
    )

    NavBar = ft.AppBar(
        leading=ft.Icon(ft.icons.TRIP_ORIGIN_ROUNDED),
        leading_width=100,
        title=ft.Text(value="Fletサンプルアプリケーション", size=32, text_align="center"),
        center_title=False,
        toolbar_height=75,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row(
                    [ toggle_dark_light_icon, exit_btn],
                    alignment="spaceBetween",
                ),
                margin=ft.margin.only(left=50, right=25)
            )
        ])

    return NavBar