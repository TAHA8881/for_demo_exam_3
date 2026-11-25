import flet as ft
from styles import LIGHT_GREEN

def header(title, app, back=False):
    controls = [
        ft.Image(src="icon.png", width=70, height=70),
        ft.Text(title, size=26, weight=ft.FontWeight.W_700),
        ft.Container(expand=True),

    ]
    user_info = ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END)

    if app.user:
        user_info.controls.append(ft.Column(
            controls=[
                ft.Text(app.user.full_name, weight=ft.FontWeight.W_700),
                ft.Text(app.user.role, size=12),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END,
        ))
        user_info.controls.append(ft.TextButton(
            "Выйти",
            on_click=lambda e: app.logout()
        ))
    elif app.screen != "login":
        user_info.controls.append(ft.Text("Гость"))
        user_info.controls.append(ft.TextButton(
            "Выйти",
            on_click=lambda e: app.logout()
        ))

    controls.append(user_info)
    return ft.Column([
        ft.Container(
            content=ft.Row(controls),
            bgcolor=LIGHT_GREEN,
            border_radius=10,
            padding = 15
        )
    ], spacing=5)