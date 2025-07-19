import sqlite3

class Burse_Info_Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        # self.create_tables()

    def create_tables_Burse(self, name):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS burse_{name}_coin_info(Монета VARCHAR(20), Цена VARCHAR(100))")
        self.conn.commit()

    def insert_price(self, coin_name, price):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO coin_prices (coin_name, price) VALUES (?, ?)', (coin_name, price))
        self.conn.commit()

    def insert_coin_info_for_burse(self, name_burse, coin_name, price):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM burse_{name_burse}_coin_info WHERE Монета = ?', (coin_name,))
        result = cursor.fetchone()
        count = result[0]

        if count > 0:
            # Монета существует, обновляем цену
            cursor.execute(f'UPDATE burse_{name_burse}_coin_info SET Цена = ? WHERE Монета = ?', (price, coin_name))
        else:
            # Монета не существует, выполняем вставку
            cursor.execute(f'INSERT INTO burse_{name_burse}_coin_info (Монета, Цена) VALUES (?, ?)', (coin_name, price))

        self.conn.commit()

    def get_allInfo_for_byrse(self,name_burse):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Монета, Цена FROM burse_{name_burse}_coin_info")
        rows = cursor.fetchall()               
        return dict(rows)
    # def get_latest_price(self, coin_name):
    #     cursor = self.conn.cursor()
    #     cursor.execute('SELECT price FROM coin_prices WHERE coin_name = ? ORDER BY timestamp DESC LIMIT 1', (coin_name,))
    #     result = cursor.fetchone()
    #     if result:
    #         return result[0]
    #     else:
    #         return None

    def close(self):
        self.conn.close()

# Пример использования класса:
# db = Burse_Info_Db('burseInfo.db')


# db.close()