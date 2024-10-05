import sqlite3


def initiate_db():
    connection = sqlite3.connect('Product.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    Products = [
        ('Вишня', 'Гейнер со вкусом вишни', 100),
        ('Клубника', 'Гейнер со вкусом клубники', 200),
        ('Персик-Маракуйя', 'Гейнер со вкусом персик-маракуйя', 300),
        ('Шоколад', 'Гейнер со вкусом шоколада', 400)
    ]
    # cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', Products)
    # cursor.execute('DELETE FROM Products')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('Product.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price FROM Products')
    prods = cursor.fetchall()
    return prods


# print(get_all_products()[0][1]) '''Поверка метода извлечения значений из функции'''
# initiate_db()
# get_all_products()