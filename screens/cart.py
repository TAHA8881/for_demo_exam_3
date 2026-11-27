import flet as ft
from styles import *
from screens.common import header
from db import create_order
from alerts import alert

def cart_screen(app):
    def update_ui():
        app.render()

    def remove_item(index):
        app.cart.pop(index)
        update_ui()

    def confirm_order(e):
        if not app.cart:
            alert(app.page, "warning", "Корзина пуста")
            return
            
        try:
            # Если пользователь - гость, укажите ID, например 1 (или создайте гостевую логику)
            user_id = app.user.id if app.user else 1 
            create_order(user_id, app.cart)
            
            alert(app.page, "success", "Заказ успешно оформлен!")
            app.cart = []
            app.load_catalog() # Пересчет остатков (п. 13 ТЗ)
            app.screen = "catalog"
            app.render()
        except Exception as ex:
            alert(app.page, "error", f"Ошибка при оформлении: {str(ex)}")

    items_controls = []
    total_sum = 0

    for i, item in enumerate(app.cart):
        total_sum += item['price'] * item['quantity']
        items_controls.append(
            ft.Row([
                ft.Text(f"{item['product'].name} | Размер: {item['size']} | Кол-во: {item['quantity']} | Цена: {item['price']:.2f} P"),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, idx=i: remove_item(idx))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    return ft.Column([
        header("Оформление заказа", app),
        ft.Text("Ваш заказ:", size=20, weight=ft.FontWeight.BOLD),
        ft.Column(items_controls, spacing=10),
        ft.Divider(),
        ft.Text(f"Итого: {total_sum:.2f} P", size=22, weight=ft.FontWeight.W_900),
        ft.Row([
            ft.Button("Подтвердить заказ", on_click=confirm_order),
            ft.TextButton("Вернуться в каталог", on_click=lambda e: (setattr(app, 'screen', 'catalog'), app.render()))
        ])
    ], expand=True)