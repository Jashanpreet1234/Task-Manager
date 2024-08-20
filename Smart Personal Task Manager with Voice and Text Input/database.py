# import sqlite3

# class Database:
#     def __init__(self, db_name='tasks.db'):
#         self.conn = sqlite3.connect(db_name)
#         self.create_table()

#     def create_table(self):
#         with self.conn:
#             self.conn.execute('''
#                 CREATE TABLE IF NOT EXISTS tasks (
#                     id INTEGER PRIMARY KEY,
#                     title TEXT NOT NULL,
#                     due_date TEXT,
#                     priority TEXT,
#                     completed BOOLEAN
#                 )
#             ''')

#     def execute_query(self, query, params=()):
#         with self.conn:
#             self.conn.execute(query, params)

#     def fetch_all(self, query, params=()):
#         with self.conn:
#             return self.conn.execute(query, params).fetchall()
