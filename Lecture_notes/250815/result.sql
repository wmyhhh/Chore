sqlite> select min(leg) from animals;
2
sqlite> .mode column
sqlite> select name, leg, weight from animals where leg = min(leg) or weight = max(weight);
Parse error: misuse of aggregate function min()
  select name, leg, weight from animals where leg = min(leg) or weight = max(wei
                                      error here ---^
sqlite> select name, leg, weight from animals where leg = (select min(leg) from animals) or weight = (select max(weight) from animals);
name      leg  weight
--------  ---  ------
elephant  4    1000
falon     2    15
parrot    2    6
sqlite>

sqlite> select avg(weight), sum(weight) from animals;
avg(weight)       sum(weight)
----------------  -----------
164.442857142857  1151.1
sqlite>

sqlite> select min(name), leg from animals union select name, max(weight) from animals;
min(name)  leg
---------  ----
cat        4
elephant   1000

sqlite> select count(name), count(distinct leg), count(distinct weight) from animals;
count(name)  count(distinct leg)  count(distinct weight)
-----------  -------------------  ----------------------
7            3                    7

sqlite> select leg from animals group by leg;
leg
---
2
4
8
sqlite> select leg, count(*) from animals group by leg;
leg  count(*)
---  --------
2    2
4    4
8    1
sqlite> select leg, max(weight) from animals group by leg;
leg  max(weight)
---  -----------
2    15
4    1000
8    0.1
sqlite> select leg, weight from animals group by leg, weight;
leg  weight
---  ------
2    6
2    15
4    10
4    20
4    100
4    1000
8    0.1

sqlite> select name, weight, leg from animals group by weight having leg = min(leg);
name      weight  leg
--------  ------  ---
spider    0.1     8
parrot    6       2
cat       10      4
falon     15      2
dog       20      4
horse     100     4
elephant  1000    4
sqlite> select name, weight, leg from animals group by leg having weight = max(weight);
name      weight  leg
--------  ------  ---
falon     15      2
elephant  1000    4
spider    0.1     8
sqlite>
sqlite> select weight/leg, count(*) from animals group by weight/leg;
weight/leg  count(*)
----------  --------
0.0125      1
2           1
3           1
5           1
7           1
25          1
250         1