import sqlite3


# 每个打开的 SQLite 数据库均以 Connection 对象来表示，这种对象是使用 sqlite3.connect() 创建的。 
# 它们的主要目的是创建 Cursor 对象，以及 事务控制。
con = sqlite3.connect('ex_data/tutorial.db')
cur = con.cursor()

# execute(sql, parameters=(), /)
# 创建一个新的 Cursor 对象，并在其上使用给出的 sql 和 parameters 调用 execute()。返回新的游标对象。
cur.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")
# 通过查询 SQLite 内置的 sqlite_matser 表以验证新表是否已经创建。
# res = cur.execute("SELECT name FROM sqlite_master")
# fetchone()，将下一行查询结果作为 tuple 返回，如果没有更多可用数据则返回 None。
# print(res.fetchone())

cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")
# 向数据库提交待处理事务。如果 autocommit 为 True，或者没有已开启的事务，则此方法不会做任何操作。
# 如果 autocommit 为 False，则如果有一个待处理事务被此方法提交则会隐式地开启一个新事务。
con.commit()

res = cur.execute("SELECT score FROM movie")
# fetchall(), 将全部（剩余的）查询结果行作为 list 返回。如果没有可用的行则返回空列表。
print(res.fetchall())

data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
# executemany(sql, parameters, /)
# 创建一个新的 Cursor 对象，并在其上使用给出的 sql 和 parameters 调用 executemany()。 返回新的游标对象。
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
con.commit()

for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
    print(row)

# 关闭数据库连接。如果 autocommit 为 False，则任何待处理事务都会被隐式地回滚。
# 如果 autocommit 为 True 或 LEGACY_TRANSACTION_CONTROL，则不会执行隐式的事务控制。
# 请确保在关闭之前 commit() 以避免丢失待处理的更改。
con.close()