CREATE TABLE numbers (n, note)
CREATE TABLE numbers (n UNIQUE, note)
CREATE TABLE numbers (n, note DEFAULT 'No comment')

sqlite> create table primes (n, prime);
sqlite> drop table if exists primes;
sqlite> select * from primes;
Parse error: no such table: primes
sqlite> create table primes (n unique, prime default 1);
sqlite> select * from primes;
sqlite>

sqlite> insert into primes values (2, 1), (3, 1);
sqlite> select * from primes;
n  prime
-  -----
2  1
3  1
sqlite> insert into primes(n) values (4), (5), (6), (7);
sqlite> select * from primes;
n  prime
-  -----
2  1
3  1
4  1
5  1
6  1
7  1

sqlite> insert into primes(n) select n + 6 from primes;
sqlite> select * from primes;
n   prime
--  -----
2   1
3   1
4   1
5   1
6   1
7   1
8   1
9   1
10  1
11  1
12  1
13  1
sqlite> insert into primes(n) select n + 12 from primes;
sqlite> select * from primes;
n   prime
--  -----
2   1
3   1
4   1
5   1
6   1
7   1
8   1
9   1
10  1
11  1
12  1
13  1
14  1
15  1
16  1
17  1
18  1
19  1
20  1
21  1
22  1
23  1
24  1
25  1

sqlite> update primes set prime = 0 where n > 2 and n % 2 = 0;
sqlite> select * from primes;
n   prime
--  -----
2   1
3   1
4   0
5   1
6   0
7   1
8   0
9   1
10  0
11  1
12  0
13  1
14  0
15  1
16  0
17  1
18  0
19  1
20  0
21  1
22  0
23  1
24  0
25  1
sqlite> update primes set prime = 0 where n > 3 and n % 3 = 0;
sqlite> update primes set prime = 0 where n > 5 and n % 5 = 0;
sqlite> update primes set prime = 0 where n > 7 and n % 7 = 0;
sqlite> select * from primes;
n   prime
--  -----
2   1
3   1
4   0
5   1
6   0
7   1
8   0
9   0
10  0
11  1
12  0
13  1
14  0
15  0
16  0
17  1
18  0
19  1
20  0
21  0
22  0
23  1
24  0
25  0

sqlite> delete from primes where prime = 0;
sqlite> select * from primes;
n   prime
--  -----
2   1
3   1
5   1
7   1
11  1
13  1
17  1
19  1
23  1
sqlite>
