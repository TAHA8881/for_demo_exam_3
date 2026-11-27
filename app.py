import flet as ft
import psycopg2
from db import get_products
from alerts import alert 
from styles import *
from screens.login import login_screen
from screens.catalog import product_card
from screens.common import header

class ShopApp:
    def __init__(self, page):
        self.page = page
        self.user= None
        self.screen="login"
        self.products = []

    def load_catalog(self):
        self.products = get_products()

    def enter(self, user=None):
        self.load_catalog()
        self.user=user
        self.screen = "catalog"
        self.render()

    def logout(self):
        self.user=None
        self.screen  ="login"
        self.render()

    def render(self):
        title = "Авторизация" if self.screen == "login" else "Каталог обуви"
        self.page.title = "Чудо обувь - " + title

        try:
            if self.screen == "login":
                content = login_screen(self)
            else:
                content = ft.Column(
                    controls=[header(title, self,back =False),
                    ft.Column(
                        controls=[product_card(p) for p in self.products],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )], expand=True
                )
        except psycopg2.Error as error:
            alert(self.page, "error", str(error).strip() or "Ошибка базы данных")
            return

        self.page.controls = [content]
        self.page.update()

def main(page: ft.Page):
    page.title= "Чудо обувь"
    page.bgcolor = WHITE
    page.theme = ft.Theme(font_family = "Calibri")
    page.padding = 25
    ShopApp(page).render()