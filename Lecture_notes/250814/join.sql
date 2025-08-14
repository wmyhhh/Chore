CREATE TABLE parents AS
    SELECT 'daisy' AS parent, 'hank' AS child UNION
    SELECT 'charlie'        , 'daisy'         UNION
    SELECT 'daisy'          , 'ace'           UNION
    SELECT 'ace'            , 'kathy'         UNION
    SELECT 'ace'            , 'johnny'        UNION
    SELECT 'johnny'         , 'cesar'         UNION
    SELECT 'hank'           , 'shelly'        UNION
    SELECT 'ace'            , 'plato';

CREATE TABLE dogs AS
    SELECT 'daisy' AS name, 'long' AS fur UNION
    SELECT 'hank'         , 'short'       UNION
    SELECT 'ace'          , 'short'       UNION
    SELECT 'kathy'        , 'curly'       UNION
    SELECT 'johnny'       , 'long'        UNION
    SELECT 'ace'          , 'short'       UNION
    SELECT 'cesar'        , 'curly'       UNION
    SELECT 'shelly'       , 'curly'       UNION
    SELECT 'plato'        , 'long';

CREATE TABLE grandparents AS
    SELECT a.parent AS granddog, b.child AS grandpup 
    FROM parents AS a, parents AS b
    WHERE a.child = b.parent;