CREATE TABLE animals AS 
    SELECT 'dog' AS name, 4 AS leg, 20 AS weight UNION
    SELECT 'cat'        , 4       , 10           UNION
    SELECT 'horse'      , 4       , 100          UNION
    SELECT 'elephant'   , 4       , 1000         UNION
    SELECT 'parrot'     , 2       , 6            UNION
    SELECT 'falon'      , 2       , 15           UNION
    SELECT 'spider'     , 8       , 0.1;