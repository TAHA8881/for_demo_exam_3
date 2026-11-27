import psycopg2
from psycopg2.extras import RealDictCursor
from models import Product
from models import User
from contextlib import closing
from datetime import date, timedelta

def get_connection():
    return psycopg2.connect(
        dbname= "shoe_shop",
        user= "postgres",
        password = "postgres",
        host = "localhost",
        port = 5432
    )

def previous_month():
    first_day_this_month = date.today().replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
    return first_day_this_month, first_day_last_month

def get_products():
    first_day_last_month, first_day_this_month = previous_month()
    with closing(get_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    p.id,
                    p.product_name,
                    p.category,
                    p.manufacturer,
                    p.content,
                    p.image,
                    p.price,
                    SUM(s.quantity) AS quantity,
                    EXISTS (
                        SELECT 1
                        FROM order_items oi
                        JOIN stock_items s ON oi.stock_item_id = s.id
                        JOIN orders o ON oi.order_number_id = o.order_number_id
                        WHERE s.product_id = p.id
                        AND o.date >= %s AND o.date < %s
                    ) as had_orders_last_month
                    FROM products p
                LEFT JOIN stock_items s ON p.id = s.product_id
                GROUP BY p.id
                """,
                (first_day_last_month, first_day_this_month)
            )

            return [
                Product(
                    product_id = row["id"],
                    name = row["product_name"],
                    category = row["category"],
                    manufacturer = row["manufacturer"],
                    content = row["content"],
                    image = row["image"],
                    price = row["price"],
                    quantity = row["quantity"],
                    had_orders_last_month = row["had_orders_last_month"],
                )
                for row in cursor.fetchall()
            ]

def get_user_by_login(login):
    with closing(get_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT u.id, u.last_name, u.name, u.middel_name, u.login, r.role
                FROM users u
                JOIN roles r ON r.id = u.role_id
                WHERE u.login = %s
                """, (login,))
            row = cursor.fetchone()
            return User(**row) if row else None



def get_product_sizes(product_id):
    with closing(get_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT s.id, s.size, st.quantity 
                FROM stock_items st
                JOIN sizes s ON st.size_id = s.id
                WHERE st.product_id = %s AND st.quantity > 0
                ORDER BY s.size
                """, (product_id,))
            return cursor.fetchall()

def create_order(user_id, cart_items):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            # 1. Создаем заказ
            cursor.execute(
                "INSERT INTO orders (user_id, order_date) VALUES (%s, CURRENT_DATE) RETURNING order_number",
                (user_id,)
            )
            order_number = cursor.fetchone()[0]

            # 2. Добавляем позиции и списываем со склада
            for item in cart_items:
                cursor.execute(
                    "INSERT INTO order_items (order_number, stock_item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_number, item['stock_item_id'], item['quantity'], item['price'])
                )
                cursor.execute(
                    "UPDATE stock_items SET quantity = quantity - %s WHERE id = %s",
                    (item['quantity'], item['stock_item_id'])
                )
            conn.commit()


# products = get_products()
# print(products)