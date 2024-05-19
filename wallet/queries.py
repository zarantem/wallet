from models import Wallet, Transaction
from django.db import connection
import psycopg2


def create_tables():
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_db_user",
        password="your_db_password",
        host="your_db_host"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Wallet (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES "User" (id) ON DELETE CASCADE,
            balance DECIMAL(10, 2),
            currency VARCHAR(3)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Transaction (
            id SERIAL PRIMARY KEY,
            wallet_id INTEGER REFERENCES Wallet (id) ON DELETE CASCADE,
            amount DECIMAL(10, 2),
            transaction_type VARCHAR(10),
            timestamp TIMESTAMP DEFAULT current_timestamp
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# Запрос для создания нового кошелька
def create_new_wallet(id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO your_wallet_table_name (key) VALUES (%s)", [id])


# Запрос для обновления баланса кошелька
def get_wallet_balance_by_key(key):
    with connection.cursor() as cursor:
        cursor.execute("SELECT balance FROM your_wallet_table_name WHERE key = %s", [key])
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None


# Запрос для получения всех транзакций для определенного кошелька
def transfer_wallet(sender_key, recipient_key, amount):
    sql_query = """
    BEGIN;
    UPDATE wallet SET balance = balance - %s WHERE wallet_key = %s AND balance >= %s;
    UPDATE wallet SET balance = balance + %s WHERE wallet_key = %s;
    COMMIT;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query, [amount, sender_key, amount, amount, recipient_key])


# Запрос для создания новой транзакции
def create_new_transaction(wallet_id, amount):
    sql_query = f"""
    INSERT INTO deposit_wallet_table (wallet_key, amount)
    VALUES ('<%s>', %s);
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query, [wallet_id, amount])
