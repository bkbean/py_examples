import sqlite3
import textwrap
from pathlib import Path


# 数据库文件路径
DB_PATH = Path('data/tutorial.db')

# 类型定义：电影元组 (标题, 年份, 评分)
Movie = tuple[str, int, float]

# 初始化数据库，创建 movie 表 (如果不存在)
def init_db(conn: sqlite3.Connection):
    sql = textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS movie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            year INTEGER,
            score REAL
        );
    """).strip()
    with conn:
        conn.execute(sql)

# 如果数据库文件存在，先删除
def reset_database(db_path: Path):
    if db_path.exists():
        db_path.unlink()
        print(f'已删除旧数据库文件: {db_path}')

# 批量插入电影数据
def insert_movies(conn: sqlite3.Connection, movies: list[Movie]):
    with conn:
        conn.executemany('INSERT INTO movie (title, year, score) VALUES (?, ?, ?)', movies)

def query_movies(
    conn: sqlite3.Connection,
    columns: list[str] = None,
    where: dict[str, any] = None,
    order_by: str = None,
    descending: bool = False,
) -> list[tuple]:
    """
    通用查询
    """
    columns_clause = ', '.join(columns) if columns else '*'
    sql = f'SELECT {columns_clause} FROM movie'

    params = []
    if where:
        conditions = [f'{key}=?' for key in where]
        sql += ' WHERE ' + ' AND '.join(conditions)
        params = list(where.values())

    if order_by:
        order = 'DESC' if descending else 'ASC'
        sql += f' ORDER BY {order_by} {order}'

    cur = conn.execute(sql, params)
    return cur.fetchall()  # always a list: [], [()], [(), (), ...]

def query_movie_one(
    conn: sqlite3.Connection,
    columns: list[str],
    where: dict[str, any],
    ) -> tuple | None:
    """
    单条查询
    """
    results = query_movies(conn, columns=columns, where=where)
    return results[0] if results else None


# 主执行逻辑
def main():
    initial_movies: list[Movie] = [
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5),
    ]

    additional_movies: list[Movie] = [
        ('Monty Python Live at the Hollywood Bowl', 1982, 7.9),
        ("Monty Python's The Meaning of Life", 1983, 7.5),
        ("Monty Python's Life of Brian", 1979, 8.0),
    ]

    # 确保目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    reset_database(DB_PATH)  # ⚠️ 先删除旧数据库（如果存在）

    try:
        # 每个打开的 SQLite 数据库均以 Connection 对象来表示, 这种对象是使用 sqlite3.connect() 创建的
        # 它们的主要目的是创建 Cursor 对象, 以及 事务控制
        with sqlite3.connect(DB_PATH) as conn:
            init_db(conn)
            insert_movies(conn, initial_movies)
            insert_movies(conn, additional_movies)

            movies_by_year = query_movies(conn, columns=['id', 'year', 'title', 'score'], order_by='year')
            for id, year, title, score in movies_by_year:
                print(f'{id:03d} | {year} | {score:.1f} | {title}')
    except sqlite3.Error as e:
        print(f'数据库错误：{e}')

# 脚本入口
if __name__ == "__main__":
    main()