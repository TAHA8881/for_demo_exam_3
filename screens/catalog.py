import flet as ft
from styles import *
from screens.common import header

def product_card(product):
    quantity = product.quantity

    bgcolor = LOW_STOCK if quantity <= 3 else WHITE

    photo = ft.Image(
        src = product.image or "picture.png",
        width = 110,
        height = 110,
        error_content = ft.Image(
            src = product.image or "picture.png",
            width = 110,
            height = 110
        ),
    )
    info = ft.Column(
        controls =  [
            ft.Container(
                content = ft.Text(
                    f'{product.manufacturer} | {product.name}',
                    text_align = ft.TextAlign.CENTER,
                    weight = ft.FontWeight.BOLD
                ),
                alignment=ft.Alignment.TOP_CENTER
            ),
            ft.Text(f"Категория: {product.category}"),
            ft.Text(f"Количество: {product.quantity}"),
            ft.Text(f"Состав: {product.content}")
        ],
        expand = True
    )

    price_elements = []
    if product.has_discount:
        price_elements.append(
            ft.Text(
                f'{product.final_price:.2f} P',
                size = 14,
                color = "grey",
                style = ft.TextStyle(
                    decoration = ft.TextDecoration.LINE_THROUGH
                )
            )
        )

    price_elements.append(
        ft.Text(
            f'{product.price:.2f} P',
                size = 20,
                weight = ft.FontWeight.W_900
            )

    )

    price = ft.Container(
        content = ft.Column(
            controls = price_elements,
            spacing = 4,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=125,
        height=110,
    )

    return ft.Container(
        content = ft.Row(
            controls = [photo, info, price]
        ),
        bgcolor =bgcolor,
        border= ft.Border.all(1, LIGHT_GREEN),
        padding = 15
    )

def catalog_screen(app):
    cards = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand =True)
    cards.controls = [product_card(product) for product in app.products]

    if not app.products:
        cards.controls.append(ft.Text("Товары не найдены"))

    return ft.Column([
        header("Каталог обуви", app),
        cards
    ])