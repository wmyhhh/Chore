sqlite> SELECT * FROM parents, dogs WHERE parent = name;
parent  child   name    fur
------  ------  ------  -----
ace     johnny  ace     short
ace     kathy   ace     short
ace     plato   ace     short
daisy   ace     daisy   long
daisy   hank    daisy   long
hank    shelly  hank    short
johnny  cesar   johnny  long

sqlite> SELECT p.parent, dp.fur AS parent_fur, p.child, dc.fur AS child_fur FROM parents AS p JOIN dogs AS dp ON p.parent = dp.name JOIN dogs as dc ON p.child = dc.name;
parent  parent_fur  child   child_fur
------  ----------  ------  ---------
ace     short       johnny  long
ace     short       kathy   curly
ace     short       plato   long
daisy   long        ace     short
daisy   long        hank    short
hank    short       shelly  curly
johnny  long        cesar   curly

sqlite> SELECT *
   ...> FROM parents AS p
   ...> JOIN dogs AS dp ON p.parent = dp.name
   ...> JOIN dogs AS dc ON p.child = dc.name;
parent  child   name    fur    name    fur
------  ------  ------  -----  ------  -----
ace     johnny  ace     short  johnny  long
ace     kathy   ace     short  kathy   curly
ace     plato   ace     short  plato   long
daisy   ace     daisy   long   ace     short
daisy   hank    daisy   long   hank    short
hank    shelly  hank    short  shelly  curly
johnny  cesar   johnny  long   cesar   curly

sqlite> SELECT parent FROM parents, dogs WHERE child = name AND fur = 'curly';
parent
------
johnny
ace
hank
sqlite> SELECT parent FROM parents JOIN dogs ON child = name WHERE fur = 'curly';
parent
------
johnny
ace
hank
sqlite> SELECT parent FROM parents JOIN dogs ON fur = 'curly' WHERE child = name;
parent
------
johnny
ace
hank

sqlite> select * from cities;
latitude  longtitude  name
--------  ----------  -----------
26        80          Miami
33        117         San Diego
38        122         Berkeley
42        71          Cambrige
45        93          Minneapolis
sqlite> select * from cold union select 'north pole';
name
-----------
Minneapolis
north pole
sqlite> select * from distances;
first        second       distance
-----------  -----------  --------
Miami        Miami        0
Miami        San Diego    420
Miami        Berkeley     720
Miami        Cambrige     960
Miami        Minneapolis  1140
San Diego    Miami        -420
San Diego    San Diego    0
San Diego    Berkeley     300
San Diego    Cambrige     540
San Diego    Minneapolis  720
Berkeley     Miami        -720
Berkeley     San Diego    -300
Berkeley     Berkeley     0
Berkeley     Cambrige     240
Berkeley     Minneapolis  420
Cambrige     Miami        -960
Cambrige     San Diego    -540
Cambrige     Berkeley     -240
Cambrige     Cambrige     0
Cambrige     Minneapolis  180
Minneapolis  Miami        -1140
Minneapolis  San Diego    -720
Minneapolis  Berkeley     -420
Minneapolis  Cambrige     -180
Minneapolis  Minneapolis  0

sqlite> select second from distances where first = 'Berkeley' order by distance;
second
-----------
Miami
San Diego
Berkeley
Cambrige
Minneapolis