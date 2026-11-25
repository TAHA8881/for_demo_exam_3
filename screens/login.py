import flet as ft
import psycopg2
from db import get_user_by_login
from alerts import alert
from screens.common import header
from styles import LIGHT_GREEN

def login_screen(app):
    login = ft.TextField(label ="Логин", width=330, autofocus=True)

    def enter(e):
        name = (login.value or "").strip()
        if not name:
            alert(app.page, "warning", "Введите логин")
            return
        try:
            user = get_user_by_login(name)
            if user is None:
                alert(app.page, "error", "Логин не найден. Проверьте ввод")
                return
            app.enter(user)
        except psycopg2.Error as error:
            alert(app.page, "error", str (error).strip() or "Не удалось подключится к базе")
            return
        alert(app.page, "success", f"Вход выполнен: {user.full_name}")

    def guest(e):
        try:
            app.enter()
        except psycopg2.Error as error:    
            alert(app.page, "error", str (error).strip() or "Не удалось загрузить каталог")

    login.on_submit = enter
    return ft.Column([
        header("Авторизация", app),
        ft.Row([
            ft.Container(content=ft.Column([
                ft.Text("Вход в систему", size=20),
                login,
                ft.Button("Войти", on_click=enter),
                ft.TextButton("Войти как гость", on_click=guest),
            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding =25, width=400, border_radius=10, border=ft.Border.all(1, LIGHT_GREEN),)
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, expand=True)

