CREATE TABLE parents AS
    SELECT 'daisy' AS parent, 'hank' AS child UNION
    SELECT 'ace'     , 'bella'    UNION
    SELECT 'ace'      , 'charlie'    UNION
    SELECT 'finne'    , 'ace'     UNION
    SELECT 'finne'     , 'daisy'     ;