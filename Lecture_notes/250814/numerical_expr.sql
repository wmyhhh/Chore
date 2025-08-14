CREATE TABLE cities AS
    SELECT 38 AS 'latitude', 122 AS 'longtitude', 'Berkeley' AS name UNION
    SELECT 42              , 71                 , 'Cambrige'         UNION
    SELECT 45              , 93                 , 'Minneapolis'      UNION
    SELECT 33              , 117                , 'San Diego'        UNION
    SELECT 26              , 80                 , 'Miami';

CREATE TABLE cold AS
    SELECT name FROM cities WHERE latitude > 43;

CREATE TABLE distances AS
    SELECT a.name AS first, b.name AS second, 60 * (b.latitude - a.latitude) AS distance
    FROM cities AS a, cities AS b;