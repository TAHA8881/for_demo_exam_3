import flet as ft

def alert(page, alert_type, message):
    title, icon, color ={
        "error": ("Ошибка", ft.Icons.ERROR_OUTLINE, "#C62828"),
        "warning": ("Предупреждение", ft.Icons.WARNING_AMBER_ROUNDED, "#FF9204"),
        "success": ("Успешно", ft.Icons.CHECK_CIRCLE_OUTLINE, "#2E7D32"),
    } [alert_type]

    page.show_dialog(ft.AlertDialog(
        modal=True,
        icon =ft.Icon(icon, color = color),
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[ft.TextButton("Закрыть", on_click= lambda e: page.pop_dialog())],
    ))

def confirm(page, message, action):
    def accept(e):
        page.pop_dialog()
        action()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        icon=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color= "#FF9204"),
        title=ft.Text("Предупреждение"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Отмена", on_click=lambda e:page.pop_dialog()),
            ft.TextButton("Продолжить", on_click=accept),
        ],
    ))