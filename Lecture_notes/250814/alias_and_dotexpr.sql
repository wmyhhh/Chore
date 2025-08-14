sqlite> SELECT a.child AS first, b.child AS second FROM parents AS a, parents AS b WHERE a.parent = b.parent AND a.child < b.child;
first   second
------  ------
johnny  kathy
johnny  plato
kathy   plato
ace     hank

sqlite> CREATE TABLE grandparents AS
   ...>     SELECT a.parent AS granddog, b.child AS grandpup
   ...>     FROM parents AS a, parents AS b
   ...>     WHERE a.child = b.parent;
sqlite> SELECT * FROM grandparents;
granddog  grandpup
--------  --------
ace       cesar
charlie   ace
charlie   hank
daisy     johnny
daisy     kathy
daisy     plato
daisy     shelly

sqlite> SELECT * FROM grandparents, dogs AS c, dogs AS d WHERE c.fur = d.fur AND c.name = granddog AND d.name = grandpup;
granddog  grandpup  name   fur   name    fur
--------  --------  -----  ----  ------  ----
daisy     johnny    daisy  long  johnny  long
daisy     plato     daisy  long  plato   long
sqlite> SELECT granddog, c.fur, grandpup, d.fur FROM grandparents, dogs AS c, dogs AS d WHERE c.fur = d.fur AND c.name = granddog AND d.name = grandpup;
granddog  fur   grandpup  fur
--------  ----  --------  ----
daisy     long  johnny    long
daisy     long  plato     long
sqlite>