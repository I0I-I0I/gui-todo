import sqlite3 as db
from typing import Any


class Db():
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = db.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_all(self, table: str) -> Any:
        query = f"select * from {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_by_id(self, table: str, id: str) -> Any:
        query = f"select * from {table} where id={id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert(self, table: str, data: dict) -> None:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        values = tuple(data.values())
        query = f"insert into {table} ({cols}) values ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, table: str, id: str) -> None:
        query = f"delete from {table} where id={id}"
        self.cursor.execute(query)
        self.conn.commit()

    def update(self, table: str, id: str, data: dict) -> None:
        cols = ", ".join(f"{key} =?" for key in data.keys())
        values = tuple(data.values()) + (id,)
        query = f"UPDATE {table} SET {cols} WHERE id =?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def create_db(self) -> None:
        try:
            with open(self.db_name, "x") as file:
                file.write("File created successfully!")
            print(f"{self.db_name} has been created.")
        except FileExistsError: pass

        query = """
            create table if not exists todos (
                id integer primary key autoincrement,
                ordering int not null,
                state text not null,
                title text not null,
                date timestamp default current_timestamp not null
            )
        """
        self.cursor.execute(query)
        self.conn.commit()
