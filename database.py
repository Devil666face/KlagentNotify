import sqlite3

class Database:
    def __init__(self, db_file_name='database.db') -> None:
        self.db = db_file_name
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def save_dict(self, sorted_dict):
        self.drop_table()
        with self.connection:
            for key in sorted_dict:
                self.cursor.execute(f"INSERT INTO Data (hostname, status) VALUES (?, ?)", (key, sorted_dict[key],))
            self.connection.commit()

    def drop_table(self):
        with self.connection:
            self.cursor.execute(f"DELETE FROM Data")
        self.connection.commit()

    def get_dict(self):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM Data")
        return {row[0]:row[1] for row in self.cursor.fetchall()}

    def create_user(self, id, name) -> bool:
        with self.connection:
            try:
                # Пишу запросы через жопу и мне пох
                self.cursor.execute(f"INSERT INTO User (id, name) VALUES ({id}, '{name}');")
                return True
            except Exception as error:
                print(f'[Ошибка добавления пользователя в БД] {error}')
                return False
            finally:
                self.connection.commit()

    def get_user_list(self):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM User")
            # return self.cursor.fetchall()
            return [id[0] for id in self.cursor.fetchall()]