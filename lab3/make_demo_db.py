import sqlite3
from pathlib import Path

path = Path(__file__).resolve().parent / "demo.sqlite"
with sqlite3.connect(path) as con:
    con.executescript("""
    DROP TABLE IF EXISTS students;
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        score REAL NOT NULL CHECK(score >= 2.0 AND score <= 5.0)
    );
    INSERT INTO students(name, group_name, score) VALUES
      ('Анна Петрова', '6107', 4.75),
      ('Илья Смирнов', '6108', 3.80),
      ('Мария Орлова', '6109', 5.00),
      ('Денис Волков', '6110', 2.65),
      ('Елена Кузнецова', '6107', 4.20),
      ('Артём Соколов', '6108', 3.45),
      ('Ольга Морозова', '6109', 4.90),
      ('Никита Фёдоров', '6110', 2.95);
    """)
print(path)
