from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class Product:
    product_id: int
    name: str
    category: str
    manufacturer: str
    content: str
    image: str | None
    price: Decimal
    quantity: int
    had_orders_last_month: bool
# Если были заказы, то True, иначе False  

    @property
    def has_discount(self):
        return not self.had_orders_last_month

    @property
    def final_price(self):
        if self.had_orders_last_month:
            return self.price

        return(self.price * Decimal("0.75")).quantize(Decimal("0.01"), rounding= ROUND_HALF_UP)

@dataclass
class User:
    id: str
    last_name: str
    name: str
    middel_name: str
    login: str
    role: str

    @property
    def full_name(self):
        return f"{self.last_name} {self.name} {self.middel_name}"

 