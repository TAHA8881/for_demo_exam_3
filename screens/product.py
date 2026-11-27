import flet as ft
from styles import *
from screens.common import header
from db import get_product_sizes
from alerts import alert

def product_screen(app):
    p = app.selected_product
    sizes_data = get_product_sizes(p.product_id)
    
    # Выбор размера
    size_options = [ft.dropdown.Option(str(s['id']), f"{s['size']} (в наличии: {s['quantity']})") for s in sizes_data]
    size_dropdown = ft.Dropdown(label="Размер", options=size_options, width=250)
    
    qty_field = ft.TextField(label="Количество", value="1", width=150, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]*", replacement_string=""))
    
    def add_to_cart(e):
        if not size_dropdown.value:
            alert(app.page, "warning", "Выберите размер")
            return
        
        try:
            qty = int(qty_field.value)
        except ValueError:
            alert(app.page, "warning", "Введите корректное количество")
            return
            
        selected_stock = next((s for s in sizes_data if str(s['id']) == size_dropdown.value), None)
        
        if qty <= 0:
            alert(app.page, "warning", "Количество должно быть больше нуля")
            return
        if qty > selected_stock['quantity']:
            alert(app.page, "warning", f"Максимум доступно: {selected_stock['quantity']} пар")
            return

        app.cart.append({
            "product": p,
            "stock_item_id": selected_stock['id'],
            "size": selected_stock['size'],
            "quantity": qty,
            "price": float(p.final_price)
        })
        alert(app.page, "success", "Добавлено в корзину")
        app.screen = "cart"
        app.render()

    def go_back(e):
        app.screen = "catalog"
        app.render()

    # Интерфейс (п. 9 ТЗ)
    price_display = f"{p.price} P" if p.has_discount else f"{p.final_price} P"
    if p.has_discount:
        price_display = f"Старая цена: {p.price} P\nНовая цена: {p.final_price} P"

    content = ft.Column([
        header("Просмотр товара", app, back=True),
        ft.Row([
            ft.Image(src=p.image or "picture.png", width=300, height=300),
            ft.Column([
                ft.Text(f"{p.manufacturer} | {p.name}", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Категория: {p.category}"),
                ft.Text(f"Описание: {p.content}"),
                ft.Text(f"Цена: {price_display}", size=20, color="green"),
                ft.Divider(),
                ft.Text("Доступные размеры:", weight=ft.FontWeight.BOLD),
                ft.Row([size_dropdown, qty_field]),
                ft.Button("Добавить в заказ", on_click=add_to_cart),
                ft.TextButton("Назад в каталог", on_click=go_back)
            ], expand=True)
        ])
    ], expand=True)
    return content