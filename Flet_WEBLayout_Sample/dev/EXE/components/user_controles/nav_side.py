import flet as ft


def NavMenu(page):
    def tap_nav_icon(e):
        if e.control.selected_index == 0:
            page.go('/')
        elif e.control.selected_index == 1:
            page.go('/FILE_CHECK')
        elif e.control.selected_index == 2:
            page.go('/FILE_OPEN')
        elif e.control.selected_index == 3:
            page.go('/FILE_COMPARE')
        elif e.control.selected_index == 4:
            page.go('/DATA_TABLE')
        elif e.control.selected_index == 5:
            page.go('/README_VIEW')
        elif e.control.selected_index == 6:
            page.go('/SETTING_VIEW')
        else:
            page.go('/')

    NavMenu = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=76,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.HOME),
                    selected_icon_content=ft.Icon(ft.icons.HOME),
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.ATTACH_FILE),
                    selected_icon_content=ft.Icon(ft.icons.ATTACH_FILE),
                    label="FILE_CHECK",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.FILE_OPEN),
                    selected_icon_content=ft.Icon(ft.icons.FILE_OPEN),
                    label="FILE_OPEN",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.COMPARE_ARROWS),
                    selected_icon_content=ft.Icon(ft.icons.COMPARE_ARROWS),
                    label_content=ft.Text("FILE_COMPARE"),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.TABLE_VIEW),
                    selected_icon_content=ft.Icon(ft.icons.TABLE_VIEW),
                    label_content=ft.Text("TABLE_VIEW"),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.READ_MORE),
                    selected_icon_content=ft.Icon(ft.icons.READ_MORE),
                    label_content=ft.Text("README_VIEW"),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.SETTINGS),
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("SETTING_VIEW"),
                )
        ],
        on_change=tap_nav_icon,
        expand=True
    )

    return NavMenu