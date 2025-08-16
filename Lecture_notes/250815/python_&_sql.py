import sqlite3

t = sqlite3.Connection('test.sql')
t.execute('drop table if exists num;')
t.execute('create table num as select 2 union select 3;')
t.execute('insert into num values (?), (?), (?)', range(4, 7))

print(t.execute('select * from num;').fetchall())

t.commit()