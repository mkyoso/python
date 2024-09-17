import flet as ft

# View
from components.Views.index import IndexView
from components.Views.file_open import FileOpenView
from components.Views.file_check import FileCheckView
from components.Views.file_diffs import FileDiffView
from components.Views.db_tables import DBView
from components.Views.readme import ReadView
from components.Views.settings import SettingsView

class Router:
    # 内部ファンクション定義 #########################
    #以下設定にてpage.routeの変数を設定
    #画面追加される場合は"#------#"以降に以下形式で追加して下さい。
    #
    # ■追加形式
    # "/{URL名}": {importしたView名}(page)

    def __init__(self, page):
        self.page = page
        self.routes = {
            "/": IndexView(page),
            "/FILE_OPEN": FileOpenView(page),
            "/FILE_CHECK": FileCheckView(page),
            "/FILE_COMPARE": FileDiffView(page),
            "/DATA_TABLE": DBView(page),
            "/README_VIEW": ReadView(page),
            "/SETTING_VIEW": SettingsView(page),
            #------#
        }
        #初期表示View
        self.body = ft.Container(content=self.routes['/']["view"])

    #画面遷移処理
    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        self.page.update()