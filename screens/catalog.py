import flet as ft
from styles import *
from screens.common import header

def product_card(product):
    quantity = product.quantity
    bgcolor = LOW_STOCK if quantity <= 3 else WHITE

    photo = ft.Image(
        src=product.image or "picture.png",
        width=110,
        height=110,
        error_content=ft.Image(src="picture.png", width=110, height=110),
    )

    info = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    f'{product.manufacturer} | {product.name}',
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ),
                alignment=ft.Alignment.TOP_CENTER
            ),
            ft.Text(f"Категория: {product.category}"),
            ft.Text(f"Количество: {product.quantity}"),
            ft.Text(f"Состав: {product.content}")
        ],
        expand=True
    )

    price_elements = []
    if product.has_discount:
        price_elements.append(
            ft.Text(
                f'{product.price:.2f} P',
                size=14,
                color="grey",
                style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
            )
        )
        price_elements.append(
            ft.Text(f'{product.final_price:.2f} P', size=20, weight=ft.FontWeight.W_900)
        )
    else:
        price_elements.append(
            ft.Text(f'{product.price:.2f} P', size=20, weight=ft.FontWeight.W_900)
        )

    price = ft.Container(
        content=ft.Column(
            controls=price_elements,
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=125,
        height=110,
    )

    return ft.Container(
        content=ft.Row(controls=[photo, info, price]),
        bgcolor=bgcolor,
        border=ft.Border.all(1, LIGHT_GREEN),
        padding=15
    )

def catalog_screen(app):
    categories = sorted(list(set(p.category for p in app.products)))
    categories.insert(0, "Все категории")

    cards = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    def update_cards():
        filtered_products = app.products

        if app.category_filter != "Все категории":
            filtered_products = [p for p in filtered_products if p.category == app.category_filter]

        if app.search_query:
            filtered_products = [
                p for p in filtered_products 
                if app.search_query in p.name.lower() or app.search_query in p.content.lower()
            ]

        if app.sort_order == "По возрастанию":
            filtered_products = sorted(filtered_products, key=lambda p: p.price)
        elif app.sort_order == "По убыванию":
            filtered_products = sorted(filtered_products, key=lambda p: p.price, reverse=True)

        cards.controls.clear()
        cards.controls.extend([product_card(product) for product in filtered_products])
        
        if not filtered_products:
            cards.controls.append(ft.Text("Товары не найдены", size=16))
            
        app.page.update()

    def on_sort_change(e):
        app.sort_order = e.control.value
        app.update_filters()

    def on_category_change(e):
        app.category_filter = e.control.value
        app.update_filters()

    def on_search_change(e):
        app.search_query = e.control.value.lower()
        update_cards()

    sort_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("none", "Без сортировки"),
            ft.dropdown.Option("По возрастанию", "Цена: по возрастанию"),
            ft.dropdown.Option("По убыванию", "Цена: по убыванию"),
        ],
        value=app.sort_order,
        width=200,
        on_select=on_sort_change
    )

    category_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(c) for c in categories],
        value=app.category_filter,
        width=200,
        on_select=on_category_change
    )

    search_field = ft.TextField(
        hint_text="Поиск по названию или описанию...",
        value=app.search_query,
        width=300,
        on_change=on_search_change,
        prefix_icon=ft.Icons.SEARCH
    )

    controls_panel = ft.Row(
        controls=[sort_dropdown, category_dropdown, search_field],
        spacing=15,
        wrap=True
    )

    update_cards()

    return ft.Column([
        header("Каталог обуви", app),
        controls_panel,
        cards
    ], expand=True)